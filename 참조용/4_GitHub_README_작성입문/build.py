from pathlib import Path
import ast
import base64
import html
import json
import re
import hashlib

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'입문웹교재'
WORKSPACE=next(path for path in ROOT.parents if (path/'templates'/'1_Project').is_dir())
TEMPLATE_ROOT=WORKSPACE/'templates'/'1_Project'
EXAMPLE=ROOT/'samples'/'완성예시'

def inline(text):
    tokens=re.split(r'(`[^`]+`|\*\*[^*]+\*\*|!\[[^\]]*\]\([^)]+\)|\[[^\]]+\]\([^)]+\))',text)
    result=[]
    for token in tokens:
        if token.startswith('`') and token.endswith('`'):result.append('<code>'+html.escape(token[1:-1])+'</code>')
        elif token.startswith('**') and token.endswith('**'):result.append('<strong>'+inline(token[2:-2])+'</strong>')
        elif re.fullmatch(r'!?\[[^\]]*\]\([^)]+\)',token):
            match=re.fullmatch(r'(!?)\[([^\]]*)\]\(([^)]+)\)',token)
            image,label,target=match.groups()
            if image:
                if target.endswith('console-output.svg'):
                    data=base64.b64encode((EXAMPLE/'assets'/'console-output.svg').read_bytes()).decode('ascii')
                    result.append('<img class="readme-image" alt="'+html.escape(label,quote=True)+'" src="data:image/svg+xml;base64,'+data+'">')
                else:result.append('<span class="image-placeholder">이미지: '+html.escape(label)+' · '+html.escape(target)+'</span>')
            else:result.append('<button type="button" class="guide-link" data-link-path="'+html.escape(target,quote=True)+'">'+html.escape(label)+'</button>')
        else:result.append(html.escape(token))
    return ''.join(result)

def build():
    tree=ast.parse((BASE/'build.py').read_text(encoding='utf-8'))
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('table_cells','render')]
    scope={'html':html,'re':re,'inline':inline}
    exec(compile(ast.Module(body=functions,type_ignores=[]),'<markdown>','exec'),scope)
    renderer=scope['render']
    template=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='template' for t in n.targets))
    def preview(source):
        # 제목을 기존 변환기의 지원 범위로 옮기고 표시 수준을 원래대로 되돌립니다.
        promoted=[];fenced=False
        for line in source.splitlines():
            if line.startswith('```'):fenced=not fenced
            if not fenced:line=re.sub(r'^(#{1,4}) ',lambda m:'##'+m[1]+' ',line)
            promoted.append(line)
        value=renderer('\n'.join(promoted))
        value=value.replace('<p>---</p>','<hr>')
        value=re.sub(r'<(/?)h([2-5])>',lambda m:'<'+m[1]+'h'+str(int(m[2])-1)+'>',value)
        value=value.replace('<li>[ ] ','<li><input type="checkbox" disabled> ').replace('<li>[x] ','<li><input type="checkbox" checked disabled> ')
        return value
    before=(TEMPLATE_ROOT/'README.md').read_text(encoding='utf-8').rstrip('\n')
    after=(EXAMPLE/'README.md').read_text(encoding='utf-8').rstrip('\n')
    def find(source,value):
        return next(i for i,line in enumerate(source.splitlines()) if value in line)
    def section(source,title):
        lines=source.splitlines();heading='## '+title
        start=next(i for i,line in enumerate(lines) if line==heading or line.startswith(heading+' ('))
        end=next((i-1 for i in range(start+1,len(lines)) if lines[i].startswith('## ')),len(lines)-1)
        return [start,end]
    def sections(source):
        parts=re.split(r'(?m)^(?=## )',source)
        result=[]
        for index,part in enumerate(parts):
            key=part.splitlines()[0][3:] if part.startswith('## ') else '__intro'
            result.append('<section data-readme-section="'+html.escape(key,quote=True)+'">'+preview(part)+'</section>')
        return ''.join(result)
    table_before=find(before,'|---|');today=find(after,'| 2026-11-19')
    steps=[
      dict(title='1. 프로젝트 이름',folder='README.md',section='__intro',before=[0,0],after=[0,0],action='교체',note='루트 README.md의 첫 줄 # [프로젝트 이름]을 자신의 저장소 주제로 바꿉니다. # 뒤에는 공백을 둡니다.'),
      dict(title='2. 한 줄 소개',folder='README.md',section='__intro',before=[2,5],after=[2,4],action='교체',note='제목 바로 아래의 인용문 자리표시자와 예시 안내를 실제 한 줄 소개로 바꿉니다. 상세 구현 설명은 docs에 둡니다.'),
      dict(title='3. 오늘 기록 한 행',folder='docs',section='개발 기록 (매일 추가)',before=[table_before,table_before+1],after=[today,today],action='추가',note='개발 기록 표의 --- 구분선 바로 아래, 기존 첫 날짜 행 위에 오늘 행을 삽입합니다. 강조된 기존 행을 덮어쓰거나 삭제하는 작업이 아닙니다. 완성 예시의 한 행을 참고하세요.'),
      dict(title='4. 상세 문서 바로가기',folder='docs',section='바로가기',before=section(before,'바로가기'),after=[find(after,'| [TIL]'),find(after,'| [기능 설명]')],action='추가·갱신',note='docs의 실제 TIL.md·설명.md를 먼저 작성한 뒤 바로가기 표에 링크합니다. README 기준 경로이므로 ./docs/부터 시작합니다.'),
      dict(title='5. 실행 화면 이미지',folder='assets',section='실행 화면',before=[find(before,'## 개발 기록'),find(before,'## 개발 기록')],after=section(after,'실행 화면'),action='새 구역 추가',note='assets에 그림을 저장하고 개발 기록 제목 위에 ## 실행 화면 구역을 추가합니다. 원본의 개발 기록 제목 자체는 유지합니다. 이미지 문법에는 !가 필요합니다.'),
      dict(title='6. 실제 소스 연결',folder='src',section='바로가기',before=[find(before,'| [소스 코드]'),find(before,'| [소스 코드]')],after=[find(after,'| [소스 코드]'),find(after,'| [소스 코드]')],action='갱신',note='src에 만든 실제 Program.cs 경로로 바로가기를 연결합니다. 없는 코드 파일로 링크만 먼저 만들지 않습니다.'),
      dict(title='7. 실행 명령',folder='src',section='실행',before=section(before,'실행'),after=section(after,'실행'),action='교체',note='## 실행 아래에 필요한 SDK와 명령의 출발 폴더를 적고 실제 csproj 경로를 지정합니다. src 바로 아래에 프로젝트가 없으면 기존 cd src + dotnet run을 그대로 쓰지 않습니다.'),
      dict(title='8. PR 칸 갱신',folder='README.md',section='개발 기록 (매일 추가)',before=[find(before,'| 2026-11-18'),find(before,'| 2026-11-18')],after=[today,today],action='상태 갱신',note='PR을 열기 전에는 작성 전으로 둡니다. 연 다음 GitHub에서 실제 PR URL을 복사해 같은 행의 마지막 칸을 [PR #번호](실제 URL)로 바꿉니다. 번호나 URL을 추측하지 않습니다.'),
      dict(title='9. 매일의 순서',folder='docs',section='매일 하는 일 (리듬)',before=section(before,'매일 하는 일'),after=section(after,'매일 하는 일'),action='확인',note='코드·상세 문서 작성 → 개발 일지 → README 요약 → 실행·링크 확인 → 커밋·PR 순서로 적용합니다. 변경하지 않은 실행 안내와 기존 날짜 행은 유지합니다.')
    ]
    for step in steps:step['copy']='\n'.join(after.splitlines()[step['after'][0]:step['after'][1]+1]).strip('\n')
    syntax_raw=[
      ('제목','# 프로젝트 이름\n\n## 실행\n\n### 확인한 결과'),
      ('강조·인라인 코드','**중요한 결과**를 기록합니다. 실행 메서드는 `Main`입니다.'),
      ('목록·체크','- src: 실제 코드\n- docs: 상세 문서\n\n1. 파일 작성\n2. 링크 확인\n\n- [ ] 실행 확인\n- [x] 문서 작성'),
      ('문서 링크','[개발 일지](./docs/개발일지.md)'),
      ('이미지','![콘솔 출력 예시](./assets/console-output.svg)'),
      ('표','| 날짜 | 한 일 |\n| --- | --- |\n| 2026-11-19 | 콘솔 출력 |'),
      ('코드 블록','```csharp\nConsole.WriteLine("안녕하세요");\n```')
    ]
    guide_data={'before':before,'after':after,'beforeHtml':sections(before),'afterHtml':sections(after),'steps':steps,
        'syntax':[{'label':label,'source':raw,'html':preview(raw)} for label,raw in syntax_raw]}
    chapters=[]
    for part in re.split(r'^## ',(ROOT/'교재.md').read_text(encoding='utf-8'),flags=re.M)[1:]:
        title,body=part.split('\n',1);markup=renderer(body)
        for key in ('FOLDERS','SYNTAX','README_MAP','PATHS','CHECKLIST'):
            markup=markup.replace('<p>&lt;!-- '+key+' --&gt;</p>','<div data-guide-widget="'+key.lower()+'"></div>')
        chapters.append({'title':title,'body':markup,'search':part})
    assert len(chapters)==9
    page=template.replace('__DATA__',json.dumps(chapters,ensure_ascii=False).replace('<','\\u003c'))
    page=page.replace('C# 첫걸음','README 입문').replace('PROGRAMMING / BEGINNER','GITHUB / README')
    page=page.replace('읽고, 실행하고, 스스로 고치기','파일 위치 → Markdown → 기록 갱신')
    page=page.replace('입문 학습 교재 / Visual Studio · C#','GitHub 문서 작성 / templates/1_Project')
    page=page.replace('개념 읽기 → 코드 실행 → 결과 확인 → 직접 해보기','구조 확인 → 수정 위치 선택 → 원문과 미리보기 비교 → 내 문서에 반영')
    page=page.replace('변수, 조건문, 클래스…','README, 상대경로, 이미지, 개발 기록…')
    page=page.replace('csharp-first-completed','github-readme-guide-completed').replace('max="14"','max="9"')
    page=page.replace('코드를 복사했습니다. Program.cs에 붙여 넣으세요.','복사했습니다. 안내된 파일 위치에서 사용하세요.')
    page=page.replace('각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.',
        '루트 README.md를 수정하는 연습입니다. 버튼으로 정확한 구역과 줄을 확인한 뒤 자신의 저장소에 반영하세요. 원본 템플릿과 GitHub 저장소를 자동으로 수정하지 않습니다.')
    style=(BASE/'reading.css').read_text(encoding='utf-8')+(ROOT/'style.css').read_text(encoding='utf-8')
    page=page.replace('</style>',style+'</style>')
    page=page.replace('</script>','\nconst guideData='+json.dumps(guide_data,ensure_ascii=False).replace('<','\\u003c')+';\n'+(ROOT/'guide.js').read_text(encoding='utf-8')+'\n</script>')
    (ROOT/'index.html').write_text(page,encoding='utf-8')
    manifest={'template':'templates/1_Project/README.md','sha256':hashlib.sha256((TEMPLATE_ROOT/'README.md').read_bytes()).hexdigest()}
    (ROOT/'template-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('생성 완료: 9개 단원 / README 작업 9개 / Markdown 예시 7개')
    return chapters,guide_data

if __name__=='__main__':build()
