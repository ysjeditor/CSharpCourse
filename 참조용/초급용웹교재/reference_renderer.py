"""기초편 원문을 생략 없이 렌더링합니다. 생성 시에만 markdown-it-py가 필요합니다."""
import html
from pathlib import PurePosixPath
import re
from urllib.parse import urljoin, urlsplit
from markdown_it import MarkdownIt

REFERENCE_URL = 'https://rkttu.github.io/csharp-book/part1-basics/'

# 원본의 본문·코드를 바꾸지 않고 누락·중복된 펜스 표기만 표시 단계에서 보정합니다.
PRESENTATION_FIXES = {
    '01-setup-environment.md': {565: 'remove-extra-fence'},
    '02-csharp-basics.md': {877: 'escape-inline-table-pipes'},
    '05-collections.md': {964: 'open-csharp-fence', 1197: 'open-csharp-fence'},
    '07-methods-basics.md': {897: 'open-csharp-fence', 1191: 'open-csharp-fence', 1558: 'open-csharp-fence'},
}

def normalize_source(source, filename):
    changes = PRESENTATION_FIXES.get(filename, {})
    lines = []
    for number, line in enumerate(source.splitlines(), 1):
        action = changes.get(number)
        if action == 'remove-extra-fence':
            assert line.strip() == '```', (filename, number)
            continue
        if action == 'open-csharp-fence':
            lines.extend(['', '```csharp'])
        if action == 'escape-inline-table-pipes':
            # 표 안의 논리 OR 연산자가 열 구분자로 오인되지 않도록 합니다.
            line = re.sub(r'`[^`]+`', lambda match: re.sub(r'(?<!\\)\|', r'\\|', match[0]), line)
        lines.append(line)
    return '\n'.join(lines) + '\n'

def parser(chapter_files):
    md = MarkdownIt('commonmark', {'html': False}).enable(['table', 'strikethrough'])

    def fence(tokens, index, options, env):
        token = tokens[index]
        language = token.info.strip().split()[0] if token.info.strip() else ''
        label = 'C# · 원문 코드' if language in ('csharp', 'cs') else language or '원문 코드'
        load = '<button class="load-example">실습창에 넣기</button>' if language in ('csharp', 'cs') else ''
        return ('<div class="code reference-code"><div class="codebar"><span>' + html.escape(label)
            + '</span><div>' + load + '<button class="copy">복사</button></div></div><pre><code>'
            + html.escape(token.content.rstrip('\n')) + '</code></pre></div>\n')

    md.renderer.rules['fence'] = fence
    md.renderer.rules['code_block'] = fence
    original_link = md.renderer.rules.get('link_open')

    def link_open(tokens, index, options, env):
        token = tokens[index]
        href = token.attrGet('href') or ''
        parts = urlsplit(href)
        if not parts.scheme and not href.startswith('#'):
            filename = PurePosixPath(parts.path).name
            if filename in chapter_files:
                # 원문 파일을 현재 교재의 장으로 연결합니다.
                token.attrSet('href', '#lesson-' + str(chapter_files[filename]))
            elif filename == 'index.md' and not parts.path.startswith('../'):
                token.attrSet('href', '#home')
            else:
                token.attrSet('href', urljoin(REFERENCE_URL, href.replace('.md', '/')))
        if (token.attrGet('href') or '').startswith(('https://', 'http://')):
            token.attrSet('target', '_blank')
            token.attrSet('rel', 'noopener')
        if original_link:
            return original_link(tokens, index, options, env)
        return md.renderer.renderToken(tokens, index, options, env)

    md.renderer.rules['link_open'] = link_open
    return md

def render_reference(text, chapter_files):
    value = parser(chapter_files).render(text)
    # MkDocs 버튼 속성은 HTML 클래스에 해당하며 본문 내용이 아닙니다.
    value = re.sub(r'(?<=</a>)\{\s*\.md-button(?:\s+\.md-button--primary)?\s*\}', '', value)
    return value
