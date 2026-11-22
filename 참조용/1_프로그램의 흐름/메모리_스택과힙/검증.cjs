const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { JSDOM, VirtualConsole } = require('../초급용웹교재/.qa/node_modules/jsdom');
const errors = [];
const log = new VirtualConsole();
log.on('jsdomError', e => errors.push(e.message));
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const dom = new JSDOM(html, { runScripts:'dangerously', virtualConsole:log,
  beforeParse(w) { w.IntersectionObserver = class { observe(){} }; }
});
const d = dom.window.document;
const click = id => d.getElementById(id).click();
assert.equal(d.querySelectorAll('aside nav a').length, 10);
const ids = [...d.querySelectorAll('[id]')].map(e => e.id);
assert.equal(new Set(ids).size, ids.length);
for (const a of d.querySelectorAll('a[href^="#"]')) assert.ok(d.querySelector(a.hash));
assert.equal(d.getElementById('back').disabled, true);
for (let i=0;i<7;i++) click('forward');
assert.equal(d.getElementById('forward').disabled, true);
assert.match(d.getElementById('heap').textContent, /재사용/);
click('back');
assert.match(d.getElementById('heap').textContent, /수집 후보/);
click('reset');
assert.match(d.getElementById('stepTitle').textContent, /^1 \/ 8/);
click('rootToggle');
assert.match(d.getElementById('rootResult').textContent, /도달하지 못/);
click('rootToggle');
assert.match(d.getElementById('rootResult').textContent, /살아 있습니다/);
for (const f of d.querySelectorAll('.quiz fieldset')) {
  f.querySelectorAll('button')[Number(f.dataset.correct)].click();
  assert.match(f.querySelector('.feedback').textContent, /^맞았습니다/);
  f.querySelectorAll('button')[1-Number(f.dataset.correct)].click();
  assert.match(f.querySelector('.feedback').textContent, /^다시 생각/);
}
click('theme'); assert.ok(d.body.classList.contains('dark'));
click('theme'); assert.ok(!d.body.classList.contains('dark'));
assert.doesNotMatch(d.body.textContent, /C:\\Users|ClaudeProject|제작중|제작 경로|작업 경로|�|順序/);
assert.equal(d.querySelectorAll('script[src],link[rel="stylesheet"],img[src]').length, 0);
assert.deepEqual(errors, []);
dom.window.close();
console.log('PASS: 10 chapters, anchors, 8 trace states, GC roots, quiz feedback, theme, offline assets, student text');
