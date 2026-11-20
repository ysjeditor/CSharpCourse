// 과제 데이터와 이 스크립트는 build.py가 HTML 안에 포함합니다.
const practiceRoot = document.createElement('section');
practiceRoot.className = 'practice';
practiceRoot.setAttribute('aria-label', '직접 코드 작성과 채점');
$('content').after(practiceRoot);
let requestInFlight = false;
let renderVersion = 0;
const memoryDrafts = new Map();
const token = document.querySelector('meta[name="runner-token"]')?.content;
const draftKey = i => 'csharp-part1-v3-practice-' + i;
function readDraft(i) {
    if (memoryDrafts.has(i)) return memoryDrafts.get(i);
    try { return localStorage.getItem(draftKey(i)) ?? exercises[i].starter; }
    catch { return exercises[i].starter; }
}
function storeDraft(i, value) {
    memoryDrafts.set(i, value);
    try { localStorage.setItem(draftKey(i), value); return '작성 코드가 이 브라우저에 저장되었습니다.'; }
    catch { return '브라우저 저장을 사용할 수 없어 현재 페이지에서만 유지됩니다.'; }
}
function mountPractice() {
    const lesson = current, version = ++renderVersion;
    practiceRoot.hidden = lesson < 0;
    if (lesson < 0) return;
    const exercise = exercises[lesson];
    practiceRoot.innerHTML = '<div class="label">CODE PRACTICE</div><h2 id="practiceTitle"></h2><p id="practiceGoal"></p><div class="connection" id="connection" role="status"></div><details class="testlist"><summary>채점 입력과 예상 출력 보기</summary><div id="tests"></div></details><label for="editor">Program.cs · 직접 코드를 작성하세요</label><textarea id="editor" spellcheck="false" wrap="off" autocomplete="off" autocapitalize="off" aria-describedby="practiceGoal editorHelp"></textarea><div id="editorHelp" class="sub">Tab: 공백 4칸 · Ctrl+Enter: 채점 · 출력은 줄바꿈 차이와 끝의 줄바꿈만 무시합니다.</div><div id="draftStatus" class="save-state" role="status"></div><label for="stdin">직접 실행할 입력값 (한 줄에 하나씩)</label><textarea id="stdin" rows="3" placeholder="예: 135"></textarea><div class="actions"><button id="runCode">실행</button><button id="gradeCode" class="done">채점하기</button><button id="resetCode">초기 코드 복원</button><button id="copyDraft">작성 코드 복사</button></div><div class="feedback" id="feedback" role="status" aria-live="polite">코드를 작성하고 실행 또는 채점하기를 누르세요.</div><details><summary>막혔을 때 힌트</summary><p id="practiceHint"></p></details>';
    $('practiceTitle').textContent = exercise.title;
    $('practiceGoal').textContent = exercise.goal;
    $('practiceHint').textContent = exercise.hint;
    $('editor').value = readDraft(lesson);
    $('stdin').value = exercise.cases[0].input;
    exercise.cases.forEach((test, i) => {
        const pre = document.createElement('pre');
        pre.textContent = `테스트 ${i + 1}\n입력: ${test.input || '(없음)'}\n예상 출력:\n${test.expected}`;
        $('tests').append(pre);
    });
    const online = !!token && location.protocol === 'http:';
    $('connection').textContent = online ? '실행기 연결 확인 중…' : '읽기·편집 모드입니다. 실제 실행과 채점은 같은 폴더의 실습시작.bat을 실행해 열린 브라우저에서 사용하세요.';
    $('runCode').disabled = $('gradeCode').disabled = !online || requestInFlight;
    if (online) fetch('/api/health').then(r => { if (!r.ok) throw Error(); return r.json(); }).then(data => {
        if (version === renderVersion) $('connection').textContent = `실제 C# 실행기 연결됨 · ${data.framework} · 테스트별 실행 제한 3초`;
    }).catch(() => { if (version === renderVersion) $('connection').textContent = '실행기에 연결할 수 없습니다. 실습시작.bat을 다시 실행하세요.'; });
    $('editor').oninput = () => { $('draftStatus').textContent = storeDraft(lesson, $('editor').value); };
    $('editor').onkeydown = e => {
        if (e.key === 'Tab') {
            e.preventDefault(); const ed = e.target;
            ed.setRangeText('    ', ed.selectionStart, ed.selectionEnd, 'end'); ed.dispatchEvent(new Event('input'));
        }
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); $('gradeCode').click(); }
    };
    $('resetCode').onclick = () => {
        if (!confirm('현재 작성 코드를 초기 코드로 바꿀까요?')) return;
        $('editor').value = exercise.starter; $('editor').dispatchEvent(new Event('input'));
    };
    $('copyDraft').onclick = async () => {
        try { await navigator.clipboard.writeText($('editor').value); $('draftStatus').textContent = '작성 코드를 복사했습니다.'; }
        catch { $('editor').focus(); $('editor').select(); $('draftStatus').textContent = 'Ctrl+C로 복사하세요.'; }
    };
    async function submit(mode) {
        if (!online || requestInFlight) return;
        requestInFlight = true;
        $('runCode').disabled = $('gradeCode').disabled = true;
        $('editor').readOnly = true;
        $('stdin').readOnly = true;
        $('resetCode').disabled = true;
        $('feedback').className = 'feedback';
        $('feedback').textContent = '컴파일하고 실행하는 중입니다. 첫 실행은 시간이 걸릴 수 있습니다…';
        const source = $('editor').value, stdin = $('stdin').value;
        storeDraft(lesson, source);
        try {
            const response = await fetch('/api/run', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Runner-Token': token }, body: JSON.stringify({ source, stdin, lesson, mode }) });
            const result = await response.json();
            if (version !== renderVersion) return;
            if (!response.ok) throw Error(result.message || '실행 요청에 실패했습니다.');
            const labels = { timeout: '시간 초과: 반복 종료 조건을 확인하세요.', output_limit: '출력 제한 초과: 반복 출력과 종료 조건을 확인하세요.', runtime_error: '실행 중 예외: 아래 오류와 줄 번호를 확인하세요.' };
            let text = '';
            if (result.status === 'compile_error') {
                text = '✕ 컴파일 오류\n' + (result.diagnostics || []).map(d => `${d.line}줄 ${d.column}열 · ${d.code}: ${d.message}`).join('\n');
                if (!result.diagnostics?.length) text += '\n' + result.output;
                const error = result.diagnostics?.find(d => d.severity === 'error');
                if (error) {
                    const lines = source.split('\n');
                    const start = lines.slice(0, error.line - 1).reduce((n, line) => n + line.length + 1, 0);
                    $('editor').focus(); $('editor').setSelectionRange(start, start + (lines[error.line - 1]?.length || 0));
                }
            } else if (result.results) {
                text = mode === 'grade' ? (result.status === 'passed' ? `✓ 전체 ${result.total}개 테스트 통과\n검사한 입력의 출력이 모두 일치합니다.` : `✕ ${result.total}개 중 ${result.results.filter(r => r.passed).length}개 통과`) : '실행 결과';
                result.results.forEach(r => {
                    text += `\n\n${mode === 'grade' ? (r.passed ? '✓' : '✕') + ' 테스트 ' + r.number : '직접 실행'}\n입력: ${r.input || '(없음)'}\n`;
                    if (r.status !== 'ok') text += (labels[r.status] || r.status) + '\n';
                    if (mode === 'grade') text += `예상 출력:\n${r.expected}\n`;
                    text += `실제 출력:\n${r.actual || '(출력 없음)'}`;
                });
                if (result.diagnostics?.length) text += '\n\n컴파일 경고:\n' + result.diagnostics.map(d => `${d.line}줄 ${d.code}: ${d.message}`).join('\n');
            } else text = (labels[result.status] || result.message || result.status) + '\n' + (result.output || '');
            $('feedback').textContent = text;
            $('feedback').className = 'feedback ' + (result.status === 'passed' || (mode === 'run' && result.status === 'ok') ? 'success' : 'failure');
        } catch (error) {
            if (version === renderVersion) { $('feedback').textContent = error.message + '\n실습시작.bat 창이 켜져 있는지 확인하세요.'; $('feedback').className = 'feedback failure'; }
        } finally {
            requestInFlight = false;
            const run = $('runCode'), grade = $('gradeCode');
            if (run && grade) run.disabled = grade.disabled = !online;
            if (version === renderVersion) {
                $('editor').readOnly = false;
                $('stdin').readOnly = false;
                $('resetCode').disabled = false;
            }
        }
    }
    $('runCode').onclick = () => submit('run');
    $('gradeCode').onclick = () => submit('grade');
}
const showReading = show;
show = function () { showReading(); mountPractice(); };
mountPractice();
