"""로컬 교재용 Markdown 렌더러."""
import html
import re

def inline(text):
    """HTML을 허용하지 않는 인라인 Markdown. 코드 안의 기호는 그대로 보존."""
    tokens = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', text)
    result = []
    for token in tokens:
        if token.startswith('`') and token.endswith('`'):
            result.append('<code>' + html.escape(token[1:-1]) + '</code>')
        elif token.startswith('**') and token.endswith('**'):
            result.append('<strong>' + inline(token[2:-2]) + '</strong>')
        else:
            result.append(html.escape(token))
    return ''.join(result)

def table_cells(line):
    # 코드 안의 | 기호는 열 구분자로 취급하지 않습니다.
    return [cell.strip().replace('\\|', '|') for cell in
            re.split(r'(?<!\\)\|(?=(?:[^`]*`[^`]*`)*[^`]*$)', line.strip().strip('|'))]

def render(text):
    output, paragraph = [], []
    lines, i, details = text.splitlines(), 0, False
    def flush():
        if paragraph:
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            flush()
            language, code = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError('닫히지 않은 코드 블록: ' + language)
            label = 'C# · 코드 예제' if language in ('cs', 'csharp') else '실행 결과' if language in ('text', 'output') else '코드'
            output.append('<div class="code"><div class="codebar"><span>' + label + '</span><button class="copy">복사</button></div><pre><code>' + html.escape('\n'.join(code)) + '</code></pre></div>')
        elif re.match(r'^#{3,6} ', line):
            flush()
            hashes, heading = line.split(' ', 1)
            if details and len(hashes) == 3:
                output.append('</details>')
                details = False
            if heading == '힌트와 해설':
                output.append('<details><summary>힌트와 해설 보기</summary>')
                details = True
            else:
                level = len(hashes) - 1
                output.append(f'<h{level}>' + inline(heading) + f'</h{level}>')
        elif line.startswith('|') and i + 1 < len(lines) and all(re.fullmatch(r':?-{3,}:?', c) for c in table_cells(lines[i+1])):
            flush()
            headers = table_cells(line)
            output.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + inline(c) + '</th>' for c in headers) + '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = table_cells(lines[i])
                if len(cells) != len(headers):
                    raise ValueError('표의 열 수가 일치하지 않습니다: ' + lines[i])
                output.append('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in cells) + '</tr>')
                i += 1
            output.append('</tbody></table></div>')
            continue
        elif re.match(r'^(?:[-*] |\d+\. )', line):
            flush()
            ordered = bool(re.match(r'^\d+\. ', line))
            tag = 'ol' if ordered else 'ul'
            pattern = r'^\d+\. (.*)' if ordered else r'^[-*] (.*)'
            output.append('<' + tag + '>')
            while i < len(lines):
                match = re.match(pattern, lines[i])
                if not match:
                    break
                output.append('<li>' + inline(match[1]) + '</li>')
                i += 1
            output.append('</' + tag + '>')
            continue
        elif line.startswith('> '):
            flush()
            quote = []
            while i < len(lines) and lines[i].startswith('> '):
                quote.append(lines[i][2:])
                i += 1
            output.append('<blockquote><p>' + inline(' '.join(quote)) + '</p></blockquote>')
            continue
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
        i += 1
    flush()
    if details:
        output.append('</details>')
    return ''.join(output)

