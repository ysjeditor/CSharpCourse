from pathlib import Path
import ast
import html
import json
import re
import hashlib
from diagrams import diagrams

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]/'입문웹교재'
WORKSPACE=next(p for p in ROOT.parents if (p/'templates'/'TextRPG'/'src').is_dir())
PROJECT=WORKSPACE/'templates'/'TextRPG'/'src'/'projects'/'text-rpg'
tree=ast.parse((BASE/'build.py').read_text(encoding='utf-8'))
definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('inline','table_cells','render')]
exec(compile(ast.Module(body=definitions,type_ignores=[]),'<markdown>','exec'))
template=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='template' for t in n.targets))
assets=ROOT/'assets';assets.mkdir(exist_ok=True)
figures=diagrams()
for key,value in figures.items():(assets/(key+'.svg')).write_text(value,encoding='utf-8')
files=sorted(p for p in PROJECT.rglob('*.cs') if not {'bin','obj'}.intersection(p.relative_to(PROJECT).parts))
assert len(files)==8
source_markup=[]
inventory=[]
for path in files:
    text=path.read_text(encoding='utf-8');relative=path.relative_to(PROJECT).as_posix()
    inventory.append({'file':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    markup='<details class="source-file"><summary>'+html.escape(relative)+'</summary><div class="code"><div class="codebar"><span>C# · 원본 코드</span><button class="copy">복사</button></div><pre><code>'+html.escape(text)+'</code></pre></div></details>'
    source_markup.append(markup)
(ROOT/'source-manifest.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
style=(BASE/'reading.css').read_text(encoding='utf-8')+(ROOT/'style.css').read_text(encoding='utf-8')
for name,kind,other in [('기획문서','플레이어 관점의 규칙','시스템문서'),('시스템문서','코드의 책임과 연결','기획문서')]:
    content=(ROOT/(name+'.md')).read_text(encoding='utf-8');chapters=[]
    for part in re.split(r'^## ',content,flags=re.M)[1:]:
        title,body=part.split('\n',1);markup=render(body)
        for key,value in figures.items():
            token='<p>&lt;!-- SVG:'+key+' --&gt;</p>'
            markup=markup.replace(token,'<figure class="diagram">'+value+'</figure>')
        markup=markup.replace('<p>&lt;!-- SOURCES --&gt;</p>',''.join(source_markup))
        chapters.append(dict(title=title,body=markup,search=part))
    page=template.replace('__DATA__',json.dumps(chapters,ensure_ascii=False).replace('<','\\u003c'))
    page=page.replace('C# 첫걸음','TextRPG '+name).replace('읽고, 실행하고, 스스로 고치기',kind)
    page=page.replace('변수, 조건문, 클래스…','사냥, 전직, 길드…').replace('csharp-first-completed','textrpg-'+name+'-completed')
    page=page.replace('각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.',kind+' · 통합 게임 기준으로 읽습니다. <a href="index.html" target="_top">두 문서와 실습 과제 보기</a> · <a href="'+other+'.html">'+other+' 열기</a>')
    page=page.replace('</style>',style+'</style>')
    page=page.replace('max="14"','max="'+str(len(chapters))+'"')
    # 세부 파일은 원본 답안이므로 각 details를 펼쳐 읽습니다.
    (ROOT/(name+'.html')).write_text(page,encoding='utf-8')
    print(name+': '+str(len(chapters))+'개 단원')
tasks=json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))
base_css=re.search(r'<style>(.*?)</style>',template,re.S)[1]
guide='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TextRPG · 기획에서 코드로</title><style>'''+base_css+style+'''</style></head><body><div class="guide-shell"><header class="guide-head"><div><div class="label">DESIGN → SYSTEM → CODE</div><h1>TextRPG · 기획에서 코드로</h1><div class="sub">기획의 문장을 클래스의 값·조건·동작으로 바꾸는 실습</div></div><div class="guide-links"><a href="기획문서.html" target="_blank" rel="noopener">기획 문서만 보기</a> · <a href="시스템문서.html" target="_blank" rel="noopener">시스템 문서만 보기</a></div></header><div class="guide-layout"><nav class="tasknav" id="tasks" aria-label="실습 단계"></nav><section class="task-card"><h2 id="taskTitle"></h2><p id="taskGoal"></p><p class="sub" id="taskFiles"></p><p id="taskCheck"></p><details><summary>구현 전에 생각할 힌트</summary><p id="taskHint"></p></details><div class="task-progress" id="progress"></div><label><input id="finished" type="checkbox">직접 구현하고 결과를 확인했습니다</label><div class="task-next"><button id="before">← 이전 과제</button><button id="after">다음 과제 →</button></div><div id="storageStatus" role="status"></div></section></div><p class="practice-note">과제를 고르면 두 문서의 해당 단원으로 이동합니다. 실제 구현은 별도의 Visual Studio 콘솔 프로젝트에서 진행하세요. 작은 창에서는 문서를 새 탭으로 열면 읽기 편합니다.</p><div class="document-pair"><section class="frame-card"><div class="frame-title">기획 · 무엇을 만들어야 하는가<a id="planLink" href="기획문서.html" target="_blank" rel="noopener">새 탭</a></div><iframe id="plan" title="게임 기획 문서"></iframe></section><section class="frame-card"><div class="frame-title">시스템 · 누가 어떤 책임을 맡는가<a id="systemLink" href="시스템문서.html" target="_blank" rel="noopener">새 탭</a></div><iframe id="system" title="클래스와 시스템 문서"></iframe></section></div></div><script>const tasks='''+json.dumps(tasks,ensure_ascii=False).replace('<','\\u003c')+';\n'+(ROOT/'guide.js').read_text(encoding='utf-8')+'</script></body></html>'
(ROOT/'index.html').write_text(guide,encoding='utf-8')
print('완료: SVG '+str(len(figures))+'개, 실제 소스 '+str(len(files))+'개, 과제 '+str(len(tasks))+'개')
