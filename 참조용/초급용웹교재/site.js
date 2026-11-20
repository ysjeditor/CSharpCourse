const $ = id => document.getElementById(id);
let current = -1, completed = [];
const storagePrefix = 'csharp-part1-v3-';
try {
    const saved = JSON.parse(localStorage.getItem(storagePrefix + 'completed') || '[]');
    if (Array.isArray(saved)) completed = [...new Set(saved.filter(n => Number.isInteger(n) && n >= 0 && n < chapters.length))];
    document.body.classList.toggle('dark', localStorage.getItem(storagePrefix + 'theme') === 'dark');
} catch {}
function save(key, value) {
    try { localStorage.setItem(storagePrefix + key, value); }
    catch { $('status').textContent = '저장 기능을 사용할 수 없습니다. 현재 화면에서 계속 학습할 수 있습니다.'; }
}
function themeLabel() {
    const dark = document.body.classList.contains('dark');
    $('theme').textContent = dark ? '밝은 화면' : '어두운 화면';
    $('theme').setAttribute('aria-pressed', String(dark));
}
function toc() {
    const q = $('search').value.trim().toLocaleLowerCase();
    $('toc').replaceChildren(); let count = 0;
    groups.forEach((group, groupIndex) => {
        const selected = chapters.map((chapter, index) => ({chapter, index}))
            .filter(({chapter}) => chapter.group === groupIndex && (!q || chapter.search.toLocaleLowerCase().includes(q)));
        if (!selected.length) return;
        const heading = document.createElement('div'); heading.className = 'group'; heading.textContent = group; $('toc').append(heading);
        selected.forEach(({chapter, index}) => {
            const a = document.createElement('a'); a.href = '#lesson-' + (index + 1);
            a.textContent = (completed.includes(index) ? '✓ ' : '') + chapter.title;
            if (index === current) a.setAttribute('aria-current', 'page');
            $('toc').append(a); count++;
        });
    });
    $('empty').hidden = count > 0; $('progress').value = completed.length;
    $('progressText').textContent = `학습 완료 ${completed.length} / ${chapters.length}`;
}
function pageToc() {
    $('pageToc').replaceChildren();
    $('content').querySelectorAll('h2,h3,h4,h5,h6').forEach((heading, index) => {
        heading.id = 'section-' + (current + 1) + '-' + index;
        const a = document.createElement('a');
        const route = current < 0 ? 'home' : 'lesson-' + (current + 1);
        a.href = '#' + route + '--' + heading.id; a.textContent = heading.textContent;
        if (heading.tagName !== 'H2') a.className = 'depth';
        $('pageToc').append(a);
    });
    if (current >= 0) {
        const practice = document.createElement('a');
        practice.href = '#lesson-' + (current + 1) + '--practice';
        practice.textContent = '웹 실습 · 실행과 채점';
        $('pageToc').append(practice);
    }
}
function show() {
    const match = location.hash.match(/^#lesson-(\d+)(?:--(?:section-\d+-\d+|practice))?$/);
    const n = match ? Number(match[1]) - 1 : -1;
    current = n >= 0 && n < chapters.length ? n : -1;
    const doc = current < 0 ? home : chapters[current];
    $('title').textContent = doc.title; document.title = doc.title + ' · C# 프로그래밍';
    $('headerPage').textContent = current < 0 ? '기초편' : doc.title;
    $('breadcrumb').textContent = current < 0 ? '' : doc.title;
    $('content').innerHTML = doc.body;
    if (current < 0) {
        const links = document.createElement('div'); links.className = 'home-links';
        const start = document.createElement('a'); start.href = '#lesson-1'; start.textContent = '1장부터 시작하기'; links.append(start); $('content').append(links);
    }
    $('notice').hidden = current < 0; $('complete').hidden = current < 0;
    $('prev').disabled = current < 0; $('prev').textContent = current === 0 ? '기초편 개요' : '이전 장';
    $('next').disabled = current === chapters.length - 1; $('next').textContent = current < 0 ? '1장 시작하기' : '다음 장';
    $('complete').textContent = completed.includes(current) ? '✓ 완료됨 · 표시 취소' : '학습 완료 표시';
    $('complete').setAttribute('aria-pressed', String(completed.includes(current)));
    $('homeTab').removeAttribute('aria-current'); $('basicsTab').removeAttribute('aria-current');
    $(current < 0 ? 'homeTab' : 'basicsTab').setAttribute('aria-current', 'page');
    $('practiceTab').href = current < 0 ? '#lesson-1--practice' : '#lesson-' + (current + 1) + '--practice';
    $('status').textContent = ''; toc(); pageToc();
    $('sidebar').classList.remove('open'); $('menu').setAttribute('aria-expanded', 'false');
}
function afterRoute() {
    const suffix = location.hash.split('--')[1];
    if (suffix === 'practice') document.querySelector('.practice')?.scrollIntoView();
    else if (suffix) document.getElementById(suffix)?.scrollIntoView();
    else window.scrollTo(0, 0);
}
window.addEventListener('hashchange', () => {
    const route = location.hash.split('--')[0];
    const previous = current < 0 ? '#home' : '#lesson-' + (current + 1);
    if (route !== previous) show();
    afterRoute();
});
$('search').oninput = () => {
    toc();
    if (window.innerWidth <= 780 && $('search').value.trim()) {
        $('sidebar').classList.add('open');
        $('menu').setAttribute('aria-expanded', 'true');
    }
};
$('prev').onclick = () => { location.hash = current <= 0 ? 'home' : 'lesson-' + current; };
$('next').onclick = () => { location.hash = 'lesson-' + (current + 2); };
$('complete').onclick = () => {
    if (current < 0) return;
    completed = completed.includes(current) ? completed.filter(n => n !== current) : [...completed, current];
    save('completed', JSON.stringify(completed));
    $('complete').textContent = completed.includes(current) ? '✓ 완료됨 · 표시 취소' : '학습 완료 표시';
    $('complete').setAttribute('aria-pressed', String(completed.includes(current))); toc();
};
$('theme').onclick = () => { document.body.classList.toggle('dark'); themeLabel(); save('theme', document.body.classList.contains('dark') ? 'dark' : 'light'); };
$('menu').onclick = () => { const open = $('sidebar').classList.toggle('open'); $('menu').setAttribute('aria-expanded', String(open)); };
$('content').addEventListener('click', async event => {
    const load = event.target.closest('.load-example');
    if (load) {
        const editor = $('editor');
        if (!editor || editor.readOnly) return;
        const code = load.closest('.code').querySelector('code').textContent;
        if (editor.value.trim() && editor.value !== code && !confirm('현재 작성 코드를 이 예제로 바꿀까요?')) return;
        editor.value = code; editor.dispatchEvent(new Event('input'));
        $('feedback').textContent = '원문 코드를 가져왔습니다. 필요한 입력을 지정하고 실행하세요. 코드 조각은 앞의 선언이나 다른 파일이 필요할 수 있습니다. 채점은 지정 과제의 기준입니다.';
        document.querySelector('.practice').scrollIntoView();
        return;
    }
    const button = event.target.closest('.copy'); if (!button) return;
    const code = button.closest('.code').querySelector('code');
    try { await navigator.clipboard.writeText(code.textContent); $('status').textContent = '코드를 복사했습니다.'; }
    catch { const range = document.createRange(); range.selectNodeContents(code); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); $('status').textContent = '코드를 선택했습니다. Ctrl+C로 복사하세요.'; }
});
themeLabel(); show();
queueMicrotask(afterRoute);
