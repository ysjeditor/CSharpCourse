"""독립 예제들을 C# 9로 빌드하고 출력 검증. python 검증.py"""
from pathlib import Path
import os
import re
import subprocess
import tempfile

root = Path(__file__).resolve().parent
env = dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_NOLOGO='1')
sdks = subprocess.run(['dotnet', '--list-sdks'], capture_output=True, encoding='utf-8', check=True).stdout
versions = [int(v) for v in re.findall(r'^(\d+)\.\d+\.\d+', sdks, re.M) if int(v) >= 6]
if not versions:
    raise SystemExit('.NET SDK 6 이상이 필요합니다.')
framework = f'net{max(versions)}.0'
count = 0
with tempfile.TemporaryDirectory(prefix='csharp-syntax-docs-') as directory:
    work = Path(directory)
    (work / 'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>', encoding='utf-8')
    (work / 'Example.csproj').write_text(
        '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
        f'<TargetFramework>{framework}</TargetFramework><OutputType>Exe</OutputType>'
        '<LangVersion>9.0</LangVersion><ImplicitUsings>disable</ImplicitUsings>'
        '<Nullable>enable</Nullable><UseAppHost>false</UseAppHost>'
        '<EnableNETAnalyzers>false</EnableNETAnalyzers></PropertyGroup></Project>', encoding='utf-8')
    for document in sorted(root.glob('[0-9][0-9]_*.md')):
        text = document.read_text(encoding='utf-8')
        code = re.search(r'```csharp\n(.*?)\n```', text, re.S)
        expected = re.search(r'```text\n(.*?)\n```', text, re.S)
        if not code or not expected:
            raise AssertionError(f'{document.name}: 예제 또는 예상 출력 누락')
        assert 'UnityEngine' not in code[1]
        (work / 'Program.cs').write_text(code[1], encoding='utf-8')
        built = subprocess.run(['dotnet', 'build', '--nologo', '-v:q', '--disable-build-servers',
                                '-p:UseSharedCompilation=false'], cwd=work, env=env,
                               capture_output=True, encoding='utf-8', errors='replace', timeout=45)
        if built.returncode:
            raise AssertionError(f'{document.name}\n{built.stdout}\n{built.stderr}')
        result = subprocess.run(['dotnet', str(work / 'bin' / 'Debug' / framework / 'Example.dll')],
                                cwd=work, env=env, capture_output=True, encoding='utf-8', errors='replace', timeout=10)
        assert result.returncode == 0, f'{document.name}\n{result.stderr}'
        actual = result.stdout.replace('\r\n', '\n').rstrip('\n')
        assert actual == expected[1], f'{document.name}: {actual!r} != {expected[1]!r}'
        count += 1
        print(f'PASS {document.name}', flush=True)
assert count == 13, count
for match in re.findall(r'\]\(([^)]+\.md)\)', (root / 'README.md').read_text(encoding='utf-8')):
    assert (root / match).is_file(), match
print(f'검증 완료: {count}개 예제 / C# 9 / 목차 링크 정상')
