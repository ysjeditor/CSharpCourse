from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import build

ROOT=Path(__file__).resolve().parent
for path in (ROOT/'assets').glob('*.svg'):
    tree=ET.parse(path)
    assert tree.getroot().attrib.get('viewBox')
    assert tree.getroot().attrib.get('aria-label')
assert len(list((ROOT/'assets').glob('*.svg')))==13
for name in ('index','기획문서','시스템문서'):
    text=(ROOT/(name+'.html')).read_text(encoding='utf-8')
    assert '__DATA__' not in text and '&lt;!-- SVG:' not in text and '&lt;!-- SOURCES' not in text
    assert 'id="print"' not in text
    js=re.search(r'<script>(.*?)</script>',text,re.S)[1]
    result=subprocess.run(['node','--check'],input=js,encoding='utf-8',capture_output=True)
    assert result.returncode==0,result.stderr
    for link in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"',text):assert (ROOT/link).is_file(),link
for entry in json.loads((ROOT/'source-manifest.json').read_text(encoding='utf-8')):
    assert hashlib.sha256((build.PROJECT/entry['file']).read_bytes()).hexdigest()==entry['sha256']
assert len(build.files)==8
tasks=json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))
assert len(tasks)==10
assert all(1<=task['plan']<=8 and 1<=task['system']<=9 for task in tasks)
print('PASS SVG 13개 / HTML·JavaScript 3개 / 소스 8개 / 과제 매핑 10개',flush=True)

harness=r'''
using TextRpg;
static class Verification
{
    static int checks;
    static void Check(bool condition,string message)
    { if(!condition)throw new Exception(message);checks++; }
    static void Main()
    {
        var hero=new Character("아린");
        Check(hero.Level==1&&hero.Hp==100&&hero.Attack==15&&hero.Kills==0,"초기값");
        hero.TakeDamage(1000);Check(hero.Hp==0&&!hero.IsAlive,"HP 하한");hero.Heal();
        Check(hero.Hp==100,"회복");
        var normal=hero.RollDamage(0);var critical=hero.RollDamage(1);
        Check(normal.damage==15&&!normal.isCritical,"일반 피해");
        Check(critical.damage==22&&critical.isCritical,"치명타 절삭");
        var guild=new Guild();Check(!guild.CanJoin(hero,out _),"초기 가입 거절");
        hero.RecordKill(20);Check(hero.Level==1&&hero.Kills==1,"슬라임 첫 처치");
        hero.RecordKill(20);Check(hero.Level==2&&hero.Kills==2&&hero.Attack==18,"둘째 성장");
        Check(guild.CanJoin(hero,out _),"가입 조건 충족");
        Check(guild.Join(hero)&&guild.Count==1,"가입 등록");
        Check(!guild.Join(hero)&&guild.Count==1,"중복 이름 거절");
        Check(object.ReferenceEquals(hero,guild.Find("아린")),"같은 참조");
        hero.RecordKill(20);hero.RecordKill(20);
        Check(hero.Level==3&&hero.Attack==21&&hero.MaxHp==120,"4킬 성장");
        Check(hero.TryChangeJob(Job.기사,out _)&&hero.MaxHp==140&&hero.Attack==26&&hero.Hp==140,"기사 전직");
        Check(!hero.TryChangeJob(Job.도적,out _),"재전직 거절");
        Check(guild.Find("아린")!.Job==Job.기사,"가입 후 변경 반영");
        Check(guild.Expel("아린")&&guild.Count==0&&guild.Find("아린")==null,"두 구조 삭제");
        Check(!guild.Expel("없음"),"없는 대상 추방");
        var reward=new Character("보상");reward.RecordKill(30);reward.RecordKill(30);
        Check(reward.Level==3,"동시 조건도 한 번 상승");
        var boundary=new Character("경계",Job.모험가,2,1,100,15);
        Check(guild.CanJoin(boundary,out _),"가입 경계 2/1");
        Check(guild.Join(new Character("조건미달")),"Join은 자격 검사 안 함");
        var codex=new MonsterCodex();Check(codex.Count==4,"도감 4종");
        var spawn=codex.Spawn(0);spawn.TakeDamage(20);
        Check(spawn.Hp==10&&codex[0].Hp==30&&!object.ReferenceEquals(spawn,codex[0]),"도감 사본");
        Check(codex.Spawn(0).Hp==30,"새 사냥 HP");
        Check(codex[0].Attack==6&&codex[2].MaxHp==110&&codex[3].ExpReward==120,"통합 수치");
        var savedOut=Console.Out;var savedIn=Console.In;var writer=new StringWriter();
        Console.SetOut(writer);
        var strong=new Character("강함",100,10000);
        Check(Battle.Fight(strong,codex.Spawn(0))&&strong.Hp==100,"사망 시 반격 없음");
        Console.SetIn(new StringReader("아린\n4\n5\na\n세라\n5\nb\n도윤\n5\na\n도윤\n3\n2\n1\n1\nabc\n6\nx\n0\n"));
        new Game().Run();
        Console.SetOut(savedOut);Console.SetIn(savedIn);
        var output=writer.ToString();
        Check(output.Contains("몬스터 도감")&&output.Contains("찾음: [세라]"),"도감 검색 메뉴");
        Check(output.Contains("'도윤' 님을 추방")&&output.Contains("'도윤' 없음"),"추방 후 조회");
        Check(output.Contains("[거절]")&&output.Contains("[실패]"),"가입 전직 거절");
        Check(output.Contains("잘못된 번호")&&output.Contains("알 수 없는 선택")&&output.Contains("모험을 종료"),"입력과 종료");
        Console.WriteLine("PASS C# 규칙 및 메뉴 검증 "+checks+"개");
    }
}
'''
env=dict(os.environ,DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_NOLOGO='1')
with tempfile.TemporaryDirectory(prefix='text-rpg-doc-check-') as directory:
    work=Path(directory)
    for path in build.files:
        if path.name=='Program.cs':continue
        target=work/path.relative_to(build.PROJECT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    (work/'Verification.cs').write_text(harness,encoding='utf-8')
    (work/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>',encoding='utf-8')
    (work/'Verification.csproj').write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable><UseAppHost>false</UseAppHost></PropertyGroup></Project>',encoding='utf-8')
    result=subprocess.run(['dotnet','build','--nologo','-v:q','--disable-build-servers','-p:UseSharedCompilation=false'],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=60)
    assert result.returncode==0,result.stdout+result.stderr
    result=subprocess.run(['dotnet',str(work/'bin'/'Debug'/'net10.0'/'Verification.dll')],cwd=work,env=env,capture_output=True,encoding='utf-8',errors='replace',timeout=15)
    assert result.returncode==0,result.stdout+result.stderr
    print(result.stdout.strip())
