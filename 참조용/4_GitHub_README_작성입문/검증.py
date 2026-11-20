from pathlib import Path
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import build

ROOT=Path(__file__).resolve().parent
chapters,data=build.build()
page=(ROOT/'index.html').read_text(encoding='utf-8')
assert len(chapters)==9 and len(data['steps'])==9 and len(data['syntax'])==7
assert '&lt;!-- README_MAP' not in page and '&lt;!-- PATHS' not in page
assert page.count('data-guide-widget=')==5
assert 'id="print"' not in page
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=',page)
script=re.search(r'<script>(.*?)</script>',page,re.S)[1]
result=subprocess.run(['node','--check'],input=script,encoding='utf-8',capture_output=True)
assert result.returncode==0,result.stderr
for step in data['steps']:
    for mode in ('before','after'):
        start,end=step[mode];assert 0<=start<=end<len(data[mode].splitlines()),step
    assert step['copy']=='\n'.join(data['after'].splitlines()[step['after'][0]:step['after'][1]+1]).strip('\n')
    assert 'data-readme-section="'+step['section']+'"' in data['afterHtml'],step
assert data['steps'][2]['copy'].startswith('| 2026-11-19')
assert '---' in data['before'].splitlines()[data['steps'][2]['before'][0]]
assert '![콘솔 출력 예시]' in data['steps'][4]['copy']
assert '--project ./src/HelloReadme/HelloReadme.csproj' in data['steps'][6]['copy']
assert 'data:image/svg+xml;base64,' in data['afterHtml']
manifest=json.loads((ROOT/'template-manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256((build.TEMPLATE_ROOT/'README.md').read_bytes()).hexdigest()==manifest['sha256']
print('PASS 단원·위젯·Markdown·강조 범위·템플릿 해시',flush=True)

sources=['README.md','docs/개발일지.md','docs/2026-11-19-콘솔출력/설명.md']
targets=['assets/console-output.svg','docs/2026-11-19-콘솔출력/TIL.md','src/HelloReadme/HelloReadme.csproj']
pairs=[]
for source in sources:
    for target in targets:
        relative=posixpath.relpath(target,posixpath.dirname(source) or '.')
        if not relative.startswith('..'):relative='./'+relative
        pairs.append([source,target,relative])
model='const document={querySelectorAll:()=>[]};function show(){};\n'+(ROOT/'guide.js').read_text(encoding='utf-8')
model+='\nconst assert=require("node:assert/strict");const pairs='+json.dumps(pairs,ensure_ascii=False)+';for(const [source,target,path] of pairs)assert.equal(relativeGuidePath(source,target),path);console.log("PASS relative paths: 9");'
result=subprocess.run(['node'],input=model,encoding='utf-8',capture_output=True)
assert result.returncode==0,result.stderr
print(result.stdout.strip(),flush=True)
example=ROOT/'samples'/'완성예시';count=0
for path in example.rglob('*.md'):
    source=path.read_text(encoding='utf-8')
    # 코드 안에 문법 예시가 있어도 모든 경로가 이 예제에서는 유효해야 합니다.
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',source):
        if '://' in target or target.startswith('#'):continue
        resolved=(path.parent/target).resolve()
        assert resolved.is_relative_to(example.resolve()),(path,target)
        assert resolved.exists(),(path,target)
        count+=1
ET.parse(example/'assets'/'console-output.svg')
print(f'PASS 완성 예시 상대 링크 {count}개와 SVG',flush=True)

with tempfile.TemporaryDirectory(prefix='readme-guide-sample-') as directory:
    work=Path(directory)
    project=example/'src'/'HelloReadme'
    for path in project.glob('*'):
        if path.is_file():shutil.copyfile(path,work/path.name)
    (work/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>',encoding='utf-8')
    env=dict(os.environ,DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_NOLOGO='1')
    result=subprocess.run(['dotnet','build','--nologo','-v:q','--disable-build-servers','-p:UseSharedCompilation=false'],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=60)
    assert result.returncode==0,result.stdout+result.stderr
    result=subprocess.run(['dotnet',str(work/'bin'/'Debug'/'net10.0'/'HelloReadme.dll')],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=10)
    assert result.returncode==0,result.stderr
    assert result.stdout.strip()=='안녕하세요, GitHub!',repr(result.stdout)
print('PASS 콘솔 프로젝트 컴파일·실제 출력 / 전체 검증 완료')
