function relativeGuidePath(source,target) {
    const base=source.split('/').slice(0,-1),dest=target.split('/');
    let common=0;while(common<base.length&&common<dest.length&&base[common]===dest[common])common++;
    const result=[...base.slice(common).map(()=>'..'),...dest.slice(common)].join('/');
    return result.startsWith('..')?result:'./'+result;
}
function folderTree(active='README.md') {
    const element=document.createElement('div');element.className='folder-tree';
    [{path:'README.md',label:'├─ README.md   ← 저장소의 첫 안내'},
     {path:'assets',label:'├─ assets/     ← 이미지·GIF'},
     {path:'docs',label:'├─ docs/       ← 개발 일지·상세 문서'},
     {path:'src',label:'└─ src/        ← 실제 코드·프로젝트'}].forEach(item=>{
         const row=document.createElement('div');row.dataset.folder=item.path;row.textContent=item.label;
         if(item.path===active)row.className='tree-active';element.append(row);
     });return element;
}
function mountFolders(root) {
    root.innerHTML='<div class="guide-box"><div class="folder-actions" aria-label="폴더 역할 선택"></div><div class="tree-slot"></div><p class="folder-note" role="status"></p></div>';
    const info=[['README.md','루트 README','요약과 링크를 갱신합니다. assets/README.md나 src/README.md가 아니라 저장소 루트의 README.md를 엽니다.'],['assets','assets · 그림','실행 이미지나 GIF를 실제 파일로 저장합니다. README에는 이미지 문법으로 이 파일을 연결합니다.'],['docs','docs · 기록','날짜·주제 폴더에 상세 내용을 쓰고 docs/개발일지.md에서 연결합니다. README에는 오늘 한 일을 한 행으로 요약합니다.'],['src','src · 코드','코드와 csproj를 실제로 만듭니다. README의 실행 명령과 소스 바로가기도 실제 위치로 갱신합니다.']];
    info.forEach(([path,label,note])=>{const button=document.createElement('button');button.textContent=label;button.onclick=()=>select(path,note,button);root.querySelector('.folder-actions').append(button);});
    function select(path,note,chosen){root.querySelector('.tree-slot').replaceChildren(folderTree(path));root.querySelector('.folder-note').textContent=note;root.querySelectorAll('.folder-actions button').forEach(b=>b.setAttribute('aria-pressed',String(b===chosen)));}
    root.querySelector('button').click();
}
function mountSyntax(root) {
    root.innerHTML='<section class="guide-box"><div class="syntax-actions" aria-label="Markdown 문법 선택"></div><div class="compare-grid"><div><div class="pane-title">Markdown 원문</div><div class="code"><div class="codebar"><span>입력할 문법</span><button class="copy">복사</button></div><pre><code></code></pre></div></div><div><div class="pane-title">표시 결과 · 학습용 미리보기</div><div class="md-preview syntax-preview"></div></div></div><p class="link-status" role="status"></p></section>';
    guideData.syntax.forEach((item,index)=>{const button=document.createElement('button');button.textContent=item.label;button.onclick=()=>{root.querySelector('.code code').textContent=item.source;root.querySelector('.syntax-preview').innerHTML=item.html;root.querySelectorAll('.syntax-actions button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));root.querySelector('.link-status').textContent='';};root.querySelector('.syntax-actions').append(button);});
    root.querySelector('.syntax-actions button').click();
    root.addEventListener('click',event=>{const link=event.target.closest('[data-link-path]');if(link)root.querySelector('.link-status').textContent='연결 대상: '+link.dataset.linkPath+' · 예시 경로입니다. 실제 파일이 있어야 GitHub에서 열립니다.';});
}
function mountReadmeMap(root) {
    root.innerHTML='<section class="guide-box workbench"><div class="readme-actions" aria-label="README 수정 작업"></div><div class="work-note"><strong class="action-label"></strong><p class="action-note" role="status" aria-live="polite"></p><div class="tree-slot"></div></div><div class="mode-actions"><button data-mode="before">원본 템플릿</button><button data-mode="after">완성 예시</button><span class="range-label"></span></div><div class="compare-grid"><div class="readme-pane"><div class="pane-title">README.md · 수정 위치를 줄 번호로 확인</div><div class="source-lines" tabindex="0" aria-label="README 원문과 강조된 수정 범위"></div></div><div class="readme-pane"><div class="pane-title">GitHub 스타일 미리보기 · 대상 구역 강조</div><div class="md-preview readme-preview" tabindex="0"></div></div></div><div class="replacement"><div class="pane-title">완성 예시에서 가져올 내용 · 자신의 정보로 바꿔 사용</div><div class="code"><div class="codebar"><span>선택한 작업의 Markdown</span><button class="copy">복사</button></div><pre><code></code></pre></div></div><p class="link-status" role="status"></p></section>';
    let selected=0,mode='before';
    guideData.steps.forEach((step,index)=>{const button=document.createElement('button');button.textContent=step.title;button.onclick=()=>{selected=index;update();};root.querySelector('.readme-actions').append(button);});
    root.querySelectorAll('[data-mode]').forEach(button=>button.onclick=()=>{mode=button.dataset.mode;update();});
    function update() {
        const step=guideData.steps[selected],range=step[mode],source=guideData[mode];
        root.querySelector('.action-label').textContent=step.action+' · 편집할 파일: 루트 README.md · 관련 위치: '+step.folder;
        root.querySelector('.action-note').textContent=step.note;
        root.querySelector('.tree-slot').replaceChildren(folderTree('README.md'));
        root.querySelector('.range-label').textContent=`${mode==='before'?'원본':'완성'} ${range[0]+1}~${range[1]+1}줄 · 줄 번호보다 제목과 문장으로 찾으세요.`;
        root.querySelectorAll('.readme-actions button').forEach((button,index)=>button.setAttribute('aria-pressed',String(index===selected)));
        root.querySelectorAll('[data-mode]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.mode===mode)));
        const lines=root.querySelector('.source-lines');lines.replaceChildren();
        source.split('\n').forEach((line,index)=>{const row=document.createElement('div');row.className='readme-line';row.dataset.line=index+1;if(index>=range[0]&&index<=range[1])row.classList.add('highlight');const number=document.createElement('span');number.className='line-number';number.textContent=index+1;const code=document.createElement('code');code.textContent=line||' ';row.append(number,code);lines.append(row);});
        const preview=root.querySelector('.readme-preview');preview.innerHTML=guideData[mode+'Html'];
        let target=[...preview.querySelectorAll('[data-readme-section]')].find(section=>section.dataset.readmeSection===step.section);
        if(!target&&mode==='before'&&selected===4)target=[...preview.querySelectorAll('[data-readme-section]')].find(section=>section.dataset.readmeSection==='개발 기록 (매일 추가)');
        if(target)target.classList.add('preview-highlight');
        root.querySelector('.replacement code').textContent=step.copy;
        root.querySelector('.link-status').textContent='';
        const focus=lines.querySelector('.highlight');
        if(focus)lines.scrollTop=Math.max(0,focus.offsetTop-lines.clientHeight/3);
        if(target)preview.scrollTop=Math.max(0,target.offsetTop-20);
    }
    root.addEventListener('click',event=>{const link=event.target.closest('[data-link-path]');if(link)root.querySelector('.link-status').textContent='이 링크가 가리킬 경로: '+link.dataset.linkPath+' · 실제 저장소의 파일/PR 주소와 일치하는지 확인하세요.';});
    update();
}
function mountPaths(root) {
    const sources=['README.md','docs/개발일지.md','docs/2026-11-19-콘솔출력/설명.md'];
    const targets=['assets/console-output.svg','docs/2026-11-19-콘솔출력/TIL.md','src/HelloReadme/HelloReadme.csproj'];
    root.innerHTML='<section class="guide-box"><div class="path-controls"><label>링크를 작성하는 문서<select class="from"></select></label><label>연결할 실제 파일<select class="to"></select></label></div><div class="path-explanation" role="status" aria-live="polite"></div><div class="code"><div class="codebar"><span>이 위치에서 사용할 Markdown</span><button class="copy">복사</button></div><pre><code></code></pre></div><p class="sub">선택한 문서의 폴더에서 공통 경로까지 올라간 뒤 대상 파일로 이동합니다.</p></section>';
    const from=root.querySelector('.from'),to=root.querySelector('.to');
    for(const value of sources){const option=document.createElement('option');option.value=value;option.textContent=value;from.append(option);}
    for(const value of targets){const option=document.createElement('option');option.value=value;option.textContent=value;to.append(option);}
    function update(){const relative=relativeGuidePath(from.value,to.value);const up=relative.split('/').filter(part=>part==='..').length;root.querySelector('.path-explanation').textContent=`출발: ${from.value} → 위로 ${up}단계 → 대상: ${to.value}\n정확한 상대경로: ${relative}`;root.querySelector('.code code').textContent=to.value.endsWith('.svg')?`![콘솔 출력 예시](${relative})`:to.value.endsWith('TIL.md')?`[TIL](${relative})`:`[프로젝트 파일](${relative})`;}
    from.onchange=to.onchange=update;update();
}
function mountChecklist(root) {
    const items=['루트 README.md를 수정했다.','프로젝트 제목과 한 줄 소개를 내 내용으로 바꿨다.','오늘 기록을 표 구분선 바로 아래에 추가했고 기존 기록은 유지했다.','docs에 실제 상세 문서를 만들고 개발 일지에서 연결했다.','이미지 파일을 assets에 넣고 문서 위치에 맞는 상대경로를 썼다.','실제 csproj 경로와 명령을 실행할 폴더를 적었다.','실행 결과와 README의 그림·설명이 일치한다.','PR을 아직 만들지 않았다면 작성 전, 만들었다면 실제 URL을 적었다.','브랜치에 코드·문서·이미지가 함께 올라가며 민감 정보는 포함하지 않았다.'];
    let checked=[];try{const stored=JSON.parse(localStorage.getItem('github-readme-final-checks')||'[]');if(Array.isArray(stored))checked=stored.filter(n=>Number.isInteger(n)&&n>=0&&n<items.length);}catch{}
    const box=document.createElement('div');box.className='guide-box final-checks';const status=document.createElement('p');status.setAttribute('role','status');
    function progress(){status.textContent=`직접 확인 ${checked.length} / ${items.length} · 저장소를 자동 검사한 결과는 아닙니다.`;}
    items.forEach((item,index)=>{const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');input.type='checkbox';input.checked=checked.includes(index);text.textContent=item;input.onchange=()=>{checked=input.checked?[...new Set([...checked,index])]:checked.filter(n=>n!==index);try{localStorage.setItem('github-readme-final-checks',JSON.stringify(checked));}catch{}progress();};label.append(input,text);box.append(label);});box.append(status);root.append(box);progress();
}
function mountReadmeGuide(){document.querySelectorAll('[data-guide-widget]').forEach(root=>{const mounts={folders:mountFolders,syntax:mountSyntax,readme_map:mountReadmeMap,paths:mountPaths,checklist:mountChecklist};mounts[root.dataset.guideWidget]?.(root);});}
const originalReadmeGuideShow=show;
show=function(){originalReadmeGuideShow();mountReadmeGuide();};
mountReadmeGuide();
