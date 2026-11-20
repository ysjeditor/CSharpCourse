"""기초 8장의 문서형 웹교재를 독립 HTML로 생성합니다."""
from pathlib import Path
import json
import re
from markdown_renderer import inline, render
from reference_renderer import render_reference, normalize_source, PRESENTATION_FIXES
ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))
chapters = []
chapter_files = {Path(row['file']).name: row['number'] for row in config['chapters']}
def document(path):
    source = path.read_text(encoding='utf-8')
    title, body = normalize_source(source, path.name).split('\n', 1)
    return dict(title=title.removeprefix('# ').strip(), body=render_reference(body, chapter_files), search=source)
for row in config['chapters']:
    chapter = document(ROOT / row['file'])
    assert chapter['title'] == row['title']
    supplement = (ROOT / row['supplement']).read_text(encoding='utf-8')
    supplement_body = supplement.split('\n', 1)[1]
    chapter['body'] = ('<section class="reference-content" aria-label="레퍼런스 원문 전체">'
        + chapter['body'] + '</section><section class="supplement-content" aria-label="추가 학습">'
        + '<h2>추가 학습 · 주석 포함 기본 구조와 검증 예제</h2>' + render(supplement_body) + '</section>')
    chapter['search'] += '\n' + supplement
    chapter.update(group=row['group'], file=row['file'])
    chapters.append(chapter)
home = document(ROOT / 'docs/index.md')
home['body'] += '<h2>웹 실행과 채점</h2><p>각 장의 원문 본문·코드·연습문제를 모두 수록했습니다. 장 아래 추가 학습에는 주석 포함 기본 구조와 실행 검증 예제가 있습니다. 실습시작.bat을 실행하면 Python 서버로 코드를 실행·채점할 수 있습니다.</p>'
exercises = json.loads((ROOT / 'exercises.json').read_text(encoding='utf-8'))
assert len(chapters) == len(exercises) == 8
public_exercises = [{k: v for k, v in e.items() if k != 'solution'} for e in exercises]
def encode(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c')
page = (ROOT / 'template.html').read_text(encoding='utf-8')
page = page.replace('__STYLE__', '\n'.join((ROOT / f).read_text(encoding='utf-8') for f in ['site.css', 'reading.css', 'practice.css', 'reference.css']))
script = 'const chapters=' + encode(chapters) + ';\n'
script += 'const home=' + encode(home) + ';\n'
script += 'const groups=' + encode(config['groups']) + ';\n'
script += 'const exercises=' + encode(public_exercises) + ';\n'
script += (ROOT / 'site.js').read_text(encoding='utf-8') + '\n'
script += (ROOT / 'practice.js').read_text(encoding='utf-8')
page = page.replace('__SCRIPT__', script)
(ROOT / 'index.html').write_text(page, encoding='utf-8')
combined = '# C# 프로그래밍 · 기초편\n\n'
for row in config['chapters']:
    source = (ROOT / row['file']).read_text(encoding='utf-8')
    combined += '## ' + source[2:].strip() + '\n\n'
(ROOT / '교재.md').write_text(combined, encoding='utf-8')
(ROOT / 'presentation-fixes.json').write_text(json.dumps(PRESENTATION_FIXES,
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'생성 완료: 기초 {len(chapters)}개 장 / {len(page.encode("utf-8")):,} bytes')
