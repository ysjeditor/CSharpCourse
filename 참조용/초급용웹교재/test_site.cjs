/* 개발용 DOM·실제 HTTP 통합 검사. npm install --prefix .qa --no-save jsdom 후 실행. */
const {JSDOM, VirtualConsole} = require('./.qa/node_modules/jsdom');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const errors = [];
const base = process.env.COURSE_TEST_URL || 'http://127.0.0.1:8767';
const exercises = JSON.parse(fs.readFileSync('exercises.json', 'utf8'));
const tick = () => new Promise(resolve => setTimeout(resolve, 30));
function dom(html, route = '') {
    const log = new VirtualConsole(); log.on('jsdomError', error => errors.push(error.message));
    return new JSDOM(html, {url: base + '/' + route, runScripts: 'dangerously', virtualConsole: log,
        beforeParse(w) {
            w.scrollTo = () => {};
            w.HTMLElement.prototype.scrollIntoView = () => {};
            w.fetch = (path, options = {}) => fetch(base + path,
                {...options, headers: {...options.headers, Origin: base}});
            w.confirm = () => true;
        }});
}
async function go(w, hash) { w.location.hash = hash; await tick(); }
async function main() {
    // HTML을 직접 연 경우 토큰이 없으므로 실제 실행은 비활성화됩니다.
    const offline = dom(fs.readFileSync('index.html', 'utf8'));
    await tick();
    assert.equal(offline.window.document.getElementById('title').textContent, '기초편');
    assert.equal(offline.window.document.querySelector('.practice').hidden, true);
    await go(offline.window, '#lesson-1');
    assert.equal(offline.window.document.getElementById('runCode').disabled, true);
    offline.window.close();

    const response = await fetch(base); assert.equal(response.status, 200);
    const live = dom(await response.text()); const w = live.window, d = w.document;
    await tick();
    assert.equal(d.querySelectorAll('#toc a').length, 8);
    assert.equal(d.querySelectorAll('#toc .group').length, 3);
    for (let n = 1; n <= 8; n++) {
        await go(w, '#lesson-' + n);
        assert.match(d.getElementById('title').textContent, new RegExp('^' + n + '장'));
        assert.equal(d.querySelector('.practice').hidden, false);
        assert.ok(d.querySelectorAll('#pageToc a').length > 5);
    }
    await go(w, '#lesson-3');
    const original = d.querySelector('.reference-content .load-example');
    const originalCode = original.closest('.code').querySelector('code').textContent;
    original.click();
    assert.equal(d.getElementById('editor').value, originalCode);
    assert.ok(d.getElementById('feedback').textContent.includes('원문 코드를 가져왔습니다'));
    const search = d.getElementById('search'); search.value = 'switch';
    search.dispatchEvent(new w.Event('input'));
    assert.ok(d.querySelector('#toc').textContent.includes('3장. 제어문'));
    search.value = '없는검색결과xyz'; search.dispatchEvent(new w.Event('input'));
    assert.equal(d.getElementById('empty').hidden, false);
    search.value = ''; search.dispatchEvent(new w.Event('input'));

    const editor = d.getElementById('editor'); editor.value = '// 보관할 코드';
    editor.dispatchEvent(new w.Event('input'));
    const section = d.querySelector('#pageToc a'); section.click(); await tick();
    assert.equal(d.getElementById('editor').value, '// 보관할 코드');
    d.getElementById('practiceTab').click(); await tick();
    assert.equal(d.getElementById('title').textContent, '3장. 제어문');
    assert.equal(d.getElementById('editor').value, '// 보관할 코드');
    d.getElementById('complete').click();
    assert.equal(d.getElementById('complete').getAttribute('aria-pressed'), 'true');
    assert.equal(d.getElementById('editor').value, '// 보관할 코드');
    await go(w, '#lesson-4'); await go(w, '#lesson-3');
    assert.equal(d.getElementById('editor').value, '// 보관할 코드');
    d.getElementById('theme').click(); assert.equal(d.body.classList.contains('dark'), true);
    d.getElementById('menu').click(); assert.equal(d.getElementById('menu').getAttribute('aria-expanded'), 'true');

    // Web UI가 전송한 장 번호를 실제 Python 서버가 채점하는지 확인합니다.
    for (const lesson of [0, 1, 2]) {
        await go(w, '#lesson-' + (lesson + 1));
        d.getElementById('editor').value = exercises[lesson].solution;
        d.getElementById('editor').dispatchEvent(new w.Event('input'));
        d.getElementById('gradeCode').click();
        const deadline = Date.now() + 60000;
        while (d.getElementById('gradeCode').disabled && Date.now() < deadline) await tick();
        assert.ok(d.getElementById('feedback').classList.contains('success'), d.getElementById('feedback').textContent);
    }
    await go(w, '#home'); assert.equal(d.querySelector('.practice').hidden, true);
    await go(w, '#lesson-99'); assert.equal(d.getElementById('title').textContent, '기초편');
    assert.deepEqual(errors, []);
    live.window.close();
    console.log('PASS: 8장 탐색, 개요, 검색, 절 이동, 코드 보관, 완료 표시, 테마, 모바일 메뉴, 실습 링크, 실제 HTTP 채점 3장');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
