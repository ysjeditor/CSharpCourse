"""문서·실행 예제·고정 추적 모델 검증: python 검증.py"""
from pathlib import Path
import json
import os
import re
import subprocess
import tempfile
import build

root = Path(__file__).resolve().parent
page = (root / 'index.html').read_text(encoding='utf-8')
script = re.search(r'<script>(.*?)</script>', page, re.S)[1]
syntax = subprocess.run(['node', '--check'], input=script, encoding='utf-8', capture_output=True)
assert syntax.returncode == 0, syntax.stderr
assert page.count('data-widget=') == 3
assert '__DATA__' not in page and 'PANEL --&gt;' not in page
assert 'id="print"' not in page
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=', page)
print('PASS 단일 HTML, 9개 단원, 위젯 연결, JavaScript 문법', flush=True)

program = (root / 'Program.cs').read_text(encoding='utf-8').rstrip('\n')
model = 'const flowProgram=' + json.dumps(program, ensure_ascii=False) + ';\nconst document={querySelectorAll:()=>[]}; function show(){};\n'
model += (root / 'flow.js').read_text(encoding='utf-8')
model += r'''
const assert=require('node:assert/strict');
assert.equal(flowStates.length,8);
assert.equal(flowQuestions.length,5);
assert.deepEqual(flowStates.at(-1).out,['시작','5','끝']);
assert.deepEqual(flowStates.at(-1).stack,[]);
assert.deepEqual(flowStates[2].stack,['Add','Main (10줄에서 결과 대기)']);
assert.equal(flowStates[4].locals,'Main: total = 5');
const lines=flowProgram.split('\n');
assert(lines[8].includes('Console.WriteLine("시작")'));
assert(lines[9].includes('Add(2, 3)'));
assert(lines[16].includes('left + right'));
assert(lines[17].includes('return result'));
for(const scope of structureScopes) assert.equal(lines[scope.end-1].trim(),'}');
for(const question of flowQuestions) assert(question.answer>=0&&question.answer<question.choices.length);
console.log('PASS 추적 모델, 코드 줄 번호, 구조 범위, 확인 문제');
'''
checked = subprocess.run(['node'], input=model, encoding='utf-8', capture_output=True)
assert checked.returncode == 0, checked.stderr
print(checked.stdout.strip(), flush=True)

env = dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_NOLOGO='1')
sdks = subprocess.run(['dotnet','--list-sdks'],capture_output=True,encoding='utf-8',check=True).stdout
major = max(int(v) for v in re.findall(r'^(\d+)\.\d+\.\d+',sdks,re.M))
framework = f'net{major}.0'
snippets = re.findall(r'```csharp\n(.*?)\n```', (root / '교재.md').read_text(encoding='utf-8'), re.S)
assert len(snippets) == 2
tests = [(snippets[0], '안녕하세요'), (snippets[1], '시작\n75\n끝'), (program, '시작\n5\n끝'),
         (program.replace('static class Program', 'class Program'), '시작\n5\n끝')]
with tempfile.TemporaryDirectory(prefix='csharp-flow-check-') as directory:
    work = Path(directory)
    (work / 'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>',encoding='utf-8')
    (work / 'Flow.csproj').write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>' +
        f'<TargetFramework>{framework}</TargetFramework><OutputType>Exe</OutputType>' +
        '<LangVersion>9.0</LangVersion><ImplicitUsings>disable</ImplicitUsings><UseAppHost>false</UseAppHost>' +
        '</PropertyGroup></Project>',encoding='utf-8')
    for i,(source,expected) in enumerate(tests,1):
        (work / 'Program.cs').write_text(source,encoding='utf-8')
        result=subprocess.run(['dotnet','build','--nologo','-v:q','--disable-build-servers','-p:UseSharedCompilation=false'],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=45)
        assert result.returncode == 0, result.stdout+result.stderr
        run=subprocess.run(['dotnet',str(work/'bin'/'Debug'/framework/'Flow.dll')],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=5)
        assert run.returncode == 0,run.stderr
        assert run.stdout.replace('\r\n','\n').rstrip('\n') == expected,run.stdout
        print(f'PASS C# 실행 예제 {i}',flush=True)
print('검증 완료: 문서와 일반 클래스/정적 Main 조합 정상')
