const structureScopes = [
    {label:'namespace 영역',start:3,end:21,note:'FlowStudy가 감싸는 형식 선언의 범위입니다. namespace를 실행하는 순서가 아니라 이름의 소속을 표시합니다.'},
    {label:'Program 클래스',start:5,end:20,note:'Program이 멤버를 담는 범위입니다. Main과 Add를 선언하며, 호출문을 이 영역에 바로 적지는 않습니다.'},
    {label:'Main 본문',start:7,end:13,note:'Main 선언과 본문입니다. 실제 첫 실행문은 9줄이며, 출력·계산 문장은 8줄과 13줄의 중괄호 사이에 있습니다.'},
    {label:'Add 메서드',start:15,end:19,note:'Add의 선언과 본문입니다. Main에서 호출할 때 실행되고 return으로 호출한 자리로 돌아갑니다.'}
];
const flowStates = [
    {line:9,stack:['Main'],locals:'Main: 아직 초기화된 지역 변수 없음',out:[],note:'Main에 진입했습니다. 노란 줄은 다음에 실행할 문장입니다. 아직 아무것도 출력하지 않았습니다.'},
    {line:10,stack:['Main'],locals:'Main: total 초기화 전',out:['시작'],note:'9줄을 실행해 시작을 출력했습니다. 이제 Add(2, 3)을 호출하여 반환값을 받을 차례입니다.'},
    {line:17,stack:['Add','Main (10줄에서 결과 대기)'],locals:'Add: left = 2, right = 3\nMain: total 초기화 전',out:['시작'],note:'Add를 호출했습니다. 매개변수에 2와 3이 전달되고, Main은 호출한 자리에서 결과를 기다립니다.'},
    {line:18,stack:['Add','Main (10줄에서 결과 대기)'],locals:'Add: left = 2, right = 3, result = 5\nMain: total 초기화 전',out:['시작'],note:'17줄의 덧셈 결과를 Add의 result에 저장했습니다. 이제 return으로 5를 돌려줍니다.'},
    {line:11,stack:['Main'],locals:'Main: total = 5',out:['시작'],note:'Add가 5를 반환했고 Main의 10줄에서 total 초기화까지 마쳤습니다. Add의 지역 변수는 Main에서 직접 사용할 수 없습니다.'},
    {line:12,stack:['Main'],locals:'Main: total = 5',out:['시작','5'],note:'11줄에서 total의 값 5를 출력했습니다. 다음은 끝이라는 문자열을 출력합니다.'},
    {line:13,stack:['Main'],locals:'Main: total = 5',out:['시작','5','끝'],note:'12줄을 실행했습니다. 이제 Main 본문의 끝에 도달합니다. 뒤에 적힌 Add를 다시 자동 실행하지 않습니다.'},
    {line:null,stack:[],locals:'실행 중인 메서드 없음',out:['시작','5','끝'],note:'Main이 반환하여 이 단순 콘솔 예제의 실행이 끝났습니다. namespace와 class의 닫는 중괄호를 실행하는 단계는 없습니다.'}
];
function drawSource(container) {
    const view = document.createElement('div');
    view.className = 'source';
    view.setAttribute('aria-label','Program.cs 코드와 줄 번호');
    flowProgram.split('\n').forEach((text,index)=>{
        const row = document.createElement('div'); row.className='source-line'; row.dataset.line=index+1;
        const number=document.createElement('span'); number.className='line-number'; number.textContent=index+1;
        const code=document.createElement('code');code.textContent=text;
        row.append(number,code);view.append(row);
    });
    container.append(view);return view;
}
function mountStructure(root) {
    root.innerHTML='<section class="ide" aria-label="Visual Studio 구조 학습 패널"><div class="ide-title">Visual Studio 구조 안내 · 학습용 화면</div><div class="ide-grid"><div class="explorer"><strong>솔루션 탐색기</strong><br>▾ FlowStudy<br>　▾ 프로젝트<br>　　Program.cs</div><div class="editor"><div class="editor-head">Program.cs</div></div></div><div class="widget-controls" aria-label="범위 선택"></div><div class="widget-note" role="status" aria-live="polite"></div></section>';
    const view=drawSource(root.querySelector('.editor'));
    const controls=root.querySelector('.widget-controls'), note=root.querySelector('.widget-note');
    const buttons=structureScopes.map((scope,index)=>{
        const button=document.createElement('button');button.textContent=scope.label;
        button.onclick=()=>select(index);controls.append(button);return button;
    });
    function select(index){const scope=structureScopes[index];buttons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));view.querySelectorAll('.source-line').forEach(line=>line.classList.toggle('in-scope',+line.dataset.line>=scope.start&&+line.dataset.line<=scope.end));note.textContent=scope.note;}
    select(2);
}
function mountFlow(root) {
    root.innerHTML='<section class="ide" aria-label="메서드 호출과 복귀 추적"><div class="ide-title">고정 예제의 실행 추적 · 노란색은 다음 실행 위치</div><div class="trace-grid"><div class="editor"><div class="editor-head">Program.cs</div></div><div class="trace-info"><h4>호출 스택 · 맨 위가 현재 메서드</h4><pre class="stack"></pre><h4>지역 변수</h4><pre class="locals"></pre><h4>콘솔 출력</h4><pre class="console"></pre></div></div><div class="widget-controls"><button class="back">← 이전 단계</button><button class="forward">다음 단계 →</button><button class="reset">처음으로</button><span class="trace-count"></span></div><div class="widget-note" role="status" aria-live="polite"></div></section>';
    const view=drawSource(root.querySelector('.editor'));let step=0;
    function update(){const state=flowStates[step];view.querySelectorAll('.source-line').forEach(line=>line.classList.toggle('at-line',+line.dataset.line===state.line));root.querySelector('.stack').textContent=state.stack.join('\n↓\n')||'(없음)';root.querySelector('.locals').textContent=state.locals;root.querySelector('.console').textContent=state.out.join('\n')||'(아직 출력 없음)';root.querySelector('.widget-note').textContent=state.note;root.querySelector('.trace-count').textContent=`${step+1} / ${flowStates.length}`;root.querySelector('.back').disabled=step===0;root.querySelector('.forward').disabled=step===flowStates.length-1;}
    root.querySelector('.back').onclick=()=>{if(step>0)step--;update();};root.querySelector('.forward').onclick=()=>{if(step<flowStates.length-1)step++;update();};root.querySelector('.reset').onclick=()=>{step=0;update();};update();
}
const flowQuestions = [
    {q:'namespace, class, Main이 중첩되어 있습니다. 실행 흐름은 어디에 먼저 들어올까요?',choices:['namespace의 첫 중괄호를 먼저 실행한다','선택된 진입점 Main에 들어온다','파일에서 위에 선언된 모든 메서드를 실행한다'],answer:1,why:'namespace와 class는 선언 구조입니다. 이 문서의 실행 추적은 진입점 Main에 들어온 뒤의 문장부터 시작합니다.'},
    {q:'Main의 닫는 중괄호 뒤이지만 Program 클래스 안인 위치에 Console.WriteLine을 직접 쓰면?',choices:['Main의 다음 문장처럼 출력된다','프로그램 종료 후 출력된다','멤버 선언 위치에 실행문을 적어 오류가 난다'],answer:2,why:'실행문은 메서드 본문 등 허용된 실행 위치에 적습니다. 클래스에 포함된다는 사실만으로 직접 출력문을 쓸 수 있는 것은 아닙니다.'},
    {q:'static class Program을 class Program으로 바꾸고 static void Main()을 유지하면?',choices:['이 예제는 여전히 유효하다','Main의 static도 반드시 제거해야 한다','Program 객체를 직접 생성해야 실행된다'],answer:0,why:'일반 클래스 안에도 정적 Main을 선언할 수 있습니다. 클래스가 반드시 정적이어야 하는 것은 아닙니다.'},
    {q:'Add 안에서 return result;를 실행하면?',choices:['언제나 프로그램 전체가 종료된다','Main에서 호출한 자리로 결과를 반환한다','namespace의 첫 줄부터 다시 시작한다'],answer:1,why:'return은 현재 메서드를 종료합니다. 이 예제에서는 Add가 결과를 반환하고 Main이 다음 처리를 이어갑니다.'},
    {q:'Add 안에서 만든 result를 Main이 직접 출력하려고 하면?',choices:['같은 클래스이므로 항상 읽을 수 있다','Main이 Add보다 위에 있으므로 읽을 수 있다','다른 메서드의 지역 변수여서 이름으로 직접 읽을 수 없다'],answer:2,why:'지역 변수의 범위를 구분해야 합니다. 반환값을 Main의 total에 받은 뒤 total을 출력합니다.'}
];
function mountQuiz(root){flowQuestions.forEach((question,index)=>{const field=document.createElement('fieldset');field.className='quiz';const legend=document.createElement('legend');legend.textContent=`${index+1}. ${question.q}`;field.append(legend);question.choices.forEach((choice,i)=>{const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');input.type='radio';input.name='flow-question-'+index;input.value=i;text.textContent=choice;label.append(input,text);field.append(label);});const check=document.createElement('button');check.textContent='답 확인';const feedback=document.createElement('div');feedback.className='answer';feedback.setAttribute('role','status');check.onclick=()=>{const selected=field.querySelector('input:checked');if(!selected){feedback.textContent='먼저 답을 선택하세요.';return;}const correct=+selected.value===question.answer;feedback.className='answer '+(correct?'correct':'wrong');feedback.textContent=(correct?'✓ 맞았습니다. ':'다시 생각해보세요. ')+question.why;};field.append(check,feedback);root.append(field);});}
function mountFlowWidgets(){document.querySelectorAll('[data-widget]').forEach(root=>{if(root.dataset.widget==='structure')mountStructure(root);if(root.dataset.widget==='flow')mountFlow(root);if(root.dataset.widget==='quiz')mountQuiz(root);});}
const showFlowReading=show;
show=function(){showFlowReading();mountFlowWidgets();};
mountFlowWidgets();
