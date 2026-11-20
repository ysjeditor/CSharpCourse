"""13개 Markdown 문서를 단일 오프라인 HTML로 생성: python build.py"""
from pathlib import Path
import ast
import html
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / '입문웹교재'

def build():
    # 기존 교재의 생성기를 실행하지 않고 변환 함수와 템플릿만 재사용합니다.
    tree = ast.parse((BASE / 'build.py').read_text(encoding='utf-8'))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name in ('inline', 'table_cells', 'render')]
    scope = {'html': html, 're': re}
    exec(compile(ast.Module(body=functions, type_ignores=[]), '<shared-markdown>', 'exec'), scope)
    template = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == 'template' for target in node.targets))
    chapters = []
    files = sorted(ROOT.glob('[0-9][0-9]_*.md'))
    for path in files:
        source = path.read_text(encoding='utf-8')
        title, body = source.split('\n', 1)
        assert title.startswith('# '), path.name
        # 개별 문서의 ## 제목을 기존 단원 본문 변환기가 처리하는 ###로 맞춥니다.
        body = re.sub(r'^(#{2,5}) ', lambda match: '#' + match[1] + ' ', body, flags=re.M)
        chapters.append({'title': title[2:], 'body': scope['render'](body), 'search': source})
    assert len(chapters) == 13, '학습 문서 13개가 필요합니다.'
    data = json.dumps(chapters, ensure_ascii=False).replace('<', '\\u003c')
    page = template.replace('__DATA__', data)
    page = page.replace('C# 첫걸음', 'C# 더 배우기')
    page = page.replace('<title>C# 더 배우기 · 입문 학습 교재</title>', '<title>알아두면 유용한 기타 문법 · C# 더 배우기</title>')
    page = page.replace('PROGRAMMING / BEGINNER', 'C# / NEXT STEPS')
    page = page.replace('읽고, 실행하고, 스스로 고치기', '알아두면 유용한 기타 문법 · 13개 단원')
    page = page.replace('입문 학습 교재 / Visual Studio · C#', '입문 다음 단계 / Visual Studio · C# 9')
    page = page.replace('개념 읽기 → 코드 실행 → 결과 확인 → 직접 해보기', '개념 이해 → 예제 실행 → 결과 해석 → 실수 점검')
    page = page.replace('변수, 조건문, 클래스…', '인터페이스, 예외, 람다, 비동기…')
    page = page.replace('csharp-first-completed', 'csharp-extra-syntax-completed')
    page = page.replace('max="14"', 'max="13"')
    page = page.replace('각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.',
                        'C# 9 범위의 일반 C# 문법과 .NET 기초 기능을 배웁니다. 각 실행 예제는 명시적인 Program.Main을 포함합니다. Visual Studio의 콘솔 프로젝트에서 Program.cs 전체를 바꿔 하나씩 실행하세요.')
    page = page.replace('</style>', (BASE / 'reading.css').read_text(encoding='utf-8') + '</style>')
    (ROOT / 'index.html').write_text(page, encoding='utf-8')
    print(f'생성 완료: {len(chapters)}개 단원 / {(ROOT / "index.html").stat().st_size:,} bytes')
    return chapters

if __name__ == '__main__':
    build()
