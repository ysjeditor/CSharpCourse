"""학습 문서를 위한 의존성 없는 SVG 도식."""
from html import escape as esc

COLORS = {'blue':('#e8f2ff','#235b91'), 'green':('#e6f5ee','#246e50'),
          'gold':('#fff2d8','#875818'), 'red':('#ffece7','#a44232'), 'purple':('#f1eafb','#694595')}

def svg(title, width, height, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title,quote=True)}">'
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#718399"/></marker></defs>'
            '<rect width="100%" height="100%" rx="14" fill="#f6f8fc"/>'
            f'<text x="26" y="34" font-size="18" font-weight="700" fill="#263b51">{esc(title)}</text>' + content + '</svg>')

def card(x,y,w,h,title,lines,tone='blue',badge=None):
    bg,ink=COLORS[tone]
    out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{ink}" stroke-opacity=".25"/>'
    out+=f'<rect x="{x}" y="{y+12}" width="4" height="{h-24}" rx="2" fill="{ink}"/>'
    out+=f'<text x="{x+18}" y="{y+31}" font-size="18" font-weight="700" fill="{ink}">{esc(title)}</text>'
    for i,line in enumerate(lines):
        out+=f'<text x="{x+18}" y="{y+59+i*24}" font-size="15" fill="#354b61">{esc(line)}</text>'
    if badge:
        out+=f'<text x="{x+w-18}" y="{y+30}" text-anchor="end" font-size="12" fill="{ink}">{esc(badge)}</text>'
    return out

def grid(title,nodes,cols=3,edges=(),height=140):
    width=1080; gap=30; cell=(width-48-gap*(cols-1))/cols
    positions=[(24+(i%cols)*(cell+gap),64+(i//cols)*(height+48)) for i in range(len(nodes))]
    body=''
    for a,b in edges:
        ax,ay=positions[a];bx,by=positions[b]
        if ay==by:
            x1=ax+cell if bx>ax else ax;x2=bx if bx>ax else bx+cell
            body+=f'<path d="M{x1} {ay+height/2}L{x2} {by+height/2}" stroke="#718399" stroke-width="2" fill="none" marker-end="url(#arrow)"/>'
        else:
            mid=(ay+height+by)/2
            body+=f'<path d="M{ax+cell/2} {ay+height}V{mid}H{bx+cell/2}V{by}" stroke="#718399" stroke-width="2" fill="none" marker-end="url(#arrow)"/>'
    for i,node in enumerate(nodes):
        body+=card(*positions[i],cell,height,*node)
    rows=(len(nodes)+cols-1)//cols
    return svg(title,width,64+rows*(height+48)-24,body)

def monster_art(kind,cx,cy,color):
    if kind==0:
        return f'<path d="M{cx-45} {cy+22}Q{cx-48} {cy-15} {cx} {cy-28}Q{cx+48} {cy-15} {cx+45} {cy+22}Z" fill="{color}"/>'+f'<circle cx="{cx-14}" cy="{cy}" r="4" fill="#24384a"/><circle cx="{cx+14}" cy="{cy}" r="4" fill="#24384a"/>'
    if kind==1:
        return f'<path d="M{cx-30} {cy-15}L{cx-53} {cy-25}L{cx-35} {cy+3}L{cx-20} {cy+29}H{cx+20}L{cx+35} {cy+3}L{cx+53} {cy-25}L{cx+30} {cy-15}Z" fill="{color}"/>'+f'<circle cx="{cx-12}" cy="{cy}" r="4" fill="#24384a"/><circle cx="{cx+12}" cy="{cy}" r="4" fill="#24384a"/>'
    if kind==2:
        return f'<rect x="{cx-37}" y="{cy-31}" width="74" height="62" rx="17" fill="{color}"/><path d="M{cx-23} {cy+18}L{cx-20} {cy+1}L{cx-12} {cy+18}M{cx+12} {cy+18}L{cx+20} {cy+1}L{cx+23} {cy+18}" fill="#fff6dc"/>'+f'<path d="M{cx-25} {cy-9}h16M{cx+9} {cy-9}h16" stroke="#24384a" stroke-width="5"/>'
    return f'<path d="M{cx-10} {cy-29}L{cx-45} {cy-43}L{cx-30} {cy+3}L{cx-54} {cy+25}L{cx-8} {cy+16}L{cx+8} {cy+32}L{cx+42} {cy+10}L{cx+22} {cy-10}L{cx+30} {cy-38}L{cx+8} {cy-29}Z" fill="{color}"/><circle cx="{cx+12}" cy="{cy-9}" r="4" fill="#fff6dc"/>'

def monsters():
    data=[('슬라임','초원',30,6,20,'#65baa2'),('고블린','동굴',55,12,30,'#92b76a'),('오크','폐광',110,20,50,'#b29070'),('드래곤','화산',300,45,120,'#cb786e')]
    body=''
    for i,(name,habitat,hp,atk,exp,color) in enumerate(data):
        x=24+(i%2)*531;y=64+(i//2)*245
        body+=f'<rect x="{x}" y="{y}" width="501" height="215" rx="14" fill="white" stroke="#dce4ee"/>'
        body+=monster_art(i,x+78,y+90,color)
        body+=f'<text x="{x+150}" y="{y+39}" font-size="23" font-weight="700" fill="#253d54">{i+1}. {name}</text><text x="{x+150}" y="{y+65}" font-size="15" fill="#64768b">{habitat} · 새 전투는 최대 HP</text>'
        for j,(label,value) in enumerate([('HP',hp),('ATK',atk),('보상',exp)]):
            body+=f'<text x="{x+150+j*108}" y="{y+106}" font-size="13" fill="#64768b">{label}</text><text x="{x+150+j*108}" y="{y+134}" font-size="24" font-weight="700" fill="#253d54">{value}</text>'
        body+=f'<rect x="{x+24}" y="{y+173}" width="453" height="10" rx="5" fill="#edf1f6"/><rect x="{x+24}" y="{y+173}" width="{453*hp/300}" height="10" rx="5" fill="{color}"/>'
    return svg('몬스터 카드 · 바 길이는 최대 HP의 상대 크기',1080,558,body)

def diagrams():
    return {
      'journey':grid('플레이의 중심은 메뉴로 돌아오는 반복',[
          ('01 이름 등록',['모험가 증명서 발급','Lv.1 · HP 100 · ATK 15'],'blue'),
          ('02 메인 메뉴',['사냥 / 전직 / 가입','도감 / 길드 / 내 정보'],'gold'),
          ('03 사냥과 성장',['선공 → 반격 → 승패','승리하면 처치·성장'],'green'),
          ('04 전직',['조건 검사 후 직업 변경','HP +20 · ATK +5'],'purple'),
          ('05 길드 참여',['조건 충족 후 가입','명단 · 검색 · 추방'],'blue'),
          ('06 메뉴 복귀 / 종료',['각 기능 후 메뉴로','0 또는 메인 입력 종료'],'gold')],edges=[(0,1),(1,2),(2,5),(3,4),(4,5)]),
      'screens':grid('콘솔 화면 와이어프레임',[
          ('시작 화면',['QUEST LOG','이름은? > 아린','환영합니다, 아린'],'blue'),
          ('메인 메뉴',['1 사냥  2 전직  3 가입','4 도감  5 길드  6 내정보','0 종료  | 선택 > 6'],'gold'),
          ('내 정보 / 결과',['[아린] 모험가 Lv.1','HP 100/100 · ATK 15','처치 0 → 메뉴로 복귀'],'green')],height=154,edges=[(0,1),(1,2)]),
      'battle':grid('전투 규칙 · 한쪽이 쓰러질 때까지 반복',[
          ('01 전투 시작',['모험가와 새 몬스터','둘 다 생존하면 턴 시작'],'blue'),
          ('02 모험가 공격',['일반 ATK / 치명 1.5배','HP 하한은 0'],'gold'),
          ('03 몬스터 생존?',['사망: 즉시 승리','생존: 반격 단계'],'purple'),
          ('승리 처리',['처치 종 기록 · 처치 +1','조건에 따라 레벨 상승'],'green'),
          ('04 몬스터 반격',['몬스터 ATK로 공격','모험가 생존 시 다음 턴'],'red'),
          ('패배 처리',['성장 보상 없음','HP 전체 회복 → 메뉴'],'blue')],edges=[(0,1),(1,2),(2,4),(4,5)]),
      'growth':grid('성장 예시 · 슬라임만 사냥했을 때',[
          ('시작',['Lv.1 / 처치 0','HP 100 · ATK 15'],'blue'),
          ('2마리 처치',['Lv.2 / 처치 2','HP 110 · ATK 18'],'green'),
          ('4마리 처치',['Lv.3 / 처치 4','HP 120 · ATK 21'],'gold'),
          ('가입 가능',['Lv.2 이상 AND 처치 1 이상','두 조건 모두 검사'],'blue'),
          ('기사 전직 성공',['모험가 · Lv.3 · 처치 4','최대 HP 140 · ATK 26'],'purple'),
          ('일반 성장 규칙',['이번 보상 ≥ 30 OR 짝수 처치','충족 시 레벨은 한 번만 +1'],'green')],edges=[(0,1),(1,2),(1,3),(2,4)]),
      'monsters':monsters(),
      'guild':grid('길드 기능의 입출력',[
          ('가입 신청',['기존 이름이면 중복 안내','레벨 2 · 처치 1 모두 검사'],'blue'),
          ('명단 표시',['세라 · 도윤은 시작 시 등록','가입 순서대로 표시'],'green'),
          ('정확한 이름 검색',['입력: 세라 → 현재 상태','없는 이름 → 없음'],'gold'),
          ('조건 미달',['부족한 레벨·처치 표시','상태를 바꾸지 않음'],'red'),
          ('추방',['입력: 도윤 → 제거','없는 대상 → 실패 안내'],'purple'),
          ('완료 확인',['추방 후 명단에 없음','이름 검색 결과도 없음'],'blue')],edges=[(0,1),(1,2),(1,4),(4,5)]),
      'learning':grid('문법 데모의 기능을 하나의 플레이로 연결',[
          ('입출력 + 변수',['1 시작 화면 · 2 HP 교환','2번은 기본 메뉴 미연결'],'blue'),
          ('판단 + 반복 + 함수',['3 가입 · 4 전직 · 5 반복','6 치명타 함수'],'gold'),
          ('클래스 + 자료구조',['7 캐릭터 · 8 도감 배열','9 명단 List · 10 검색'],'green')],height=150,edges=[(0,1),(1,2)]),
      'architecture':grid('클래스 책임 지도 · 화살표는 사용/호출이며 상속이 아닙니다',[
          ('Program.cs',['최상위 진입 코드','new Game().Run()'],'blue'),
          ('Game',['시작 · 메뉴 · 기능 조립','hero / guild / codex 보유'],'gold'),
          ('Battle «static»',['Fight(hero, monster)','전투 처리 → bool 반환'],'red'),
          ('Guild',['명단과 이름 색인','CanJoin / Join / Expel / Find'],'green'),
          ('Character',['능력치 · 성장 · 전직','RollDamage / TakeDamage'],'purple'),
          ('MonsterCodex',['고정 도감 · 처치 집합','Spawn / MarkDefeated'],'blue'),
          ('Job «enum»',['모험가 / 기사','도적 / 마법사'],'purple'),
          ('보유와 전달',['Game이 상태를 유지','Battle은 객체 참조를 받음'],'gold'),
          ('Monster',['도감 원본과 전투 사본','Clone / TakeDamage'],'green')],height=133,edges=[(0,1),(1,2),(1,3),(1,4),(1,5),(2,4),(5,8)]),
      'models':grid('모델의 핵심 계약 · private set은 내부 변경',[
          ('Character',['Name: string { get; }','Level / Hp / Attack / Kills','IsAlive → Hp > 0','성장 · 전직 · 피해 계산'],'purple'),
          ('Monster',['Name / MaxHp / Attack','ExpReward / Habitat','Hp { get; private set; }','Clone은 MaxHp로 새 객체'],'green')],cols=2,height=186),
      'clone':grid('도감과 사냥 대상의 객체를 구분',[
          ('도감 배열 원본',['_monsters[0] = 슬라임','MaxHp 30 / Hp 30'],'blue'),
          ('Spawn(0) → Clone()',['새 Monster 생성','원본과 다른 참조'],'gold'),
          ('전투 사본',['TakeDamage(15)','Hp 15 → 원본 Hp는 30'],'red')],edges=[(0,1),(1,2)]),
      'sequence':grid('사냥의 호출 흐름 · 아래 기능은 순차적으로 연결됩니다',[
          ('Game.Hunt',['번호 입력·검증','1부터 Count → pick - 1'],'gold'),
          ('MonsterCodex.Spawn',['원본 Clone','새 Monster 반환'],'blue'),
          ('Battle.Fight',['RollDamage → TakeDamage','영웅 생존 여부 반환'],'red'),
          ('승리: MarkDefeated',['HashSet에 종 이름 추가','같은 종은 중복 저장 안 함'],'green'),
          ('승리: RecordKill',['Kills +1 → 성장 조건 검사','스탯 변경 후 Describe'],'purple'),
          ('패배: Heal',['HP = MaxHp','보상 없이 메뉴로'],'blue')],edges=[(0,1),(1,2),(2,3),(3,4),(2,5)]),
      'translation':grid('기획 문장을 코드의 값·조건·동작으로 번역',[
          ('기획: 처치를 기록한다',['몬스터를 이기면 1 증가','그 뒤 성장 조건 판단'],'blue'),
          ('값과 조건',['Kills++','expReward >= 30','OR Kills % 2 == 0'],'gold'),
          ('동작: 한 번 레벨업',['Level++ / MaxHp += 10','Attack += 3 / Hp = MaxHp'],'green')],height=163,edges=[(0,1),(1,2)]),
      'storage':grid('길드의 자료구조 두 개는 같은 Character를 가리킵니다',[
          ('List<Character>',['세라 → 도윤 → 아린','순서 있는 명단'],'blue'),
          ('Character 아린',['같은 객체 참조','성장 후 상태도 함께 보임'],'purple'),
          ('Dictionary<string, Character>',['키: 아린 → 값: Character','정확한 이름 검색'],'green'),
          ('Join의 갱신',['List에 추가','Dictionary에 키 등록'],'gold'),
          ('Expel의 갱신',['검색한 객체를 List에서 제거','Dictionary에서 키 제거'],'red'),
          ('검증할 일관성',['추방 후 Count 감소','Find(name)는 null'],'blue')],edges=[(0,1),(2,1),(3,4),(4,5)])
    }
