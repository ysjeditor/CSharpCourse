"""기존 입문웹교재의 스타일과 Markdown 변환을 재사용. python build.py"""
from pathlib import Path
import ast
import html
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / '입문웹교재'
tree = ast.parse((BASE / 'build.py').read_text(encoding='utf-8'))
# 원본 생성기를 실행하거나 입문웹교재 파일을 변경하지 않습니다.
definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ('inline', 'table_cells', 'render')]
exec(compile(ast.Module(body=definitions, type_ignores=[]), '<shared-markdown>', 'exec'))
template = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == 'template' for target in node.targets))
source = (ROOT / '교재.md').read_text(encoding='utf-8')
chapters = []
for part in re.split(r'^## ', source, flags=re.M)[1:]:
    title, body = part.split('\n', 1)
    markup = render(body)
    for name in ('STRUCTURE', 'FLOW', 'QUIZ'):
        markup = markup.replace('<p>&lt;!-- ' + name + '_PANEL --&gt;</p>', '<div data-widget="' + name.lower() + '"></div>')
    chapters.append(dict(title=title, body=markup, search=part))
assert len(chapters) == 9
page = template.replace('__DATA__', json.dumps(chapters, ensure_ascii=False).replace('<', '\\u003c'))
page = page.replace('C# 첫걸음', '프로그램의 흐름')
page = page.replace('읽고, 실행하고, 스스로 고치기', '감싸는 구조와 실행 순서 이해하기')
page = page.replace('변수, 조건문, 클래스…', 'namespace, Main, 중괄호…')
page = page.replace('csharp-first-completed', 'csharp-program-flow-completed')
page = page.replace('max="14"', 'max="9"')
page = page.replace('각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.', '명시적인 namespace · Program · Main 구조로 배웁니다. 완성 예제는 Program.cs 전체를 바꿔 실행하세요. 단계별 추적은 정해진 예제를 설명하는 학습 도구입니다.')
styles = (BASE / 'reading.css').read_text(encoding='utf-8') + (ROOT / 'flow.css').read_text(encoding='utf-8')
page = page.replace('</style>', styles + '</style>')
program = (ROOT / 'Program.cs').read_text(encoding='utf-8').rstrip('\n')
script = '\nconst flowProgram=' + json.dumps(program, ensure_ascii=False).replace('<', '\\u003c') + ';\n' + (ROOT / 'flow.js').read_text(encoding='utf-8')
page = page.replace('</script>', script + '\n</script>')
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print(f'생성 완료: {len(chapters)}개 단원 / 단일 HTML {(ROOT / "index.html").stat().st_size:,} bytes')
