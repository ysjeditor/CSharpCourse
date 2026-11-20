"""외부 패키지 없이 Markdown 교재를 독립 HTML로 변환합니다."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / '교재.md').read_text(encoding='utf-8')

def inline(text):
    """HTML을 허용하지 않는 인라인 Markdown. 코드 안의 기호는 그대로 보존."""
    tokens = re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', text)
    result = []
    for token in tokens:
        if token.startswith('`') and token.endswith('`'):
            result.append('<code>' + html.escape(token[1:-1]) + '</code>')
        elif token.startswith('**') and token.endswith('**'):
            result.append('<strong>' + inline(token[2:-2]) + '</strong>')
        else:
            result.append(html.escape(token))
    return ''.join(result)

def table_cells(line):
    # 코드 안의 | 기호는 열 구분자로 취급하지 않습니다.
    return [cell.strip().replace('\\|', '|') for cell in
            re.split(r'(?<!\\)\|(?=(?:[^`]*`[^`]*`)*[^`]*$)', line.strip().strip('|'))]

def render(text):
    output, paragraph = [], []
    lines, i, details = text.splitlines(), 0, False
    def flush():
        if paragraph:
            output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
            paragraph.clear()
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            flush()
            language, code = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError('닫히지 않은 코드 블록: ' + language)
            label = 'C# · 코드 예제' if language in ('cs', 'csharp') else '실행 결과' if language in ('text', 'output') else '코드'
            output.append('<div class="code"><div class="codebar"><span>' + label + '</span><button class="copy">복사</button></div><pre><code>' + html.escape('\n'.join(code)) + '</code></pre></div>')
        elif re.match(r'^#{3,6} ', line):
            flush()
            hashes, heading = line.split(' ', 1)
            if details and len(hashes) == 3:
                output.append('</details>')
                details = False
            if heading == '힌트와 해설':
                output.append('<details><summary>힌트와 해설 보기</summary>')
                details = True
            else:
                level = len(hashes) - 1
                output.append(f'<h{level}>' + inline(heading) + f'</h{level}>')
        elif line.startswith('|') and i + 1 < len(lines) and all(re.fullmatch(r':?-{3,}:?', c) for c in table_cells(lines[i+1])):
            flush()
            headers = table_cells(line)
            output.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + inline(c) + '</th>' for c in headers) + '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = table_cells(lines[i])
                if len(cells) != len(headers):
                    raise ValueError('표의 열 수가 일치하지 않습니다: ' + lines[i])
                output.append('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in cells) + '</tr>')
                i += 1
            output.append('</tbody></table></div>')
            continue
        elif re.match(r'^(?:[-*] |\d+\. )', line):
            flush()
            ordered = bool(re.match(r'^\d+\. ', line))
            tag = 'ol' if ordered else 'ul'
            pattern = r'^\d+\. (.*)' if ordered else r'^[-*] (.*)'
            output.append('<' + tag + '>')
            while i < len(lines):
                match = re.match(pattern, lines[i])
                if not match:
                    break
                output.append('<li>' + inline(match[1]) + '</li>')
                i += 1
            output.append('</' + tag + '>')
            continue
        elif line.startswith('> '):
            flush()
            quote = []
            while i < len(lines) and lines[i].startswith('> '):
                quote.append(lines[i][2:])
                i += 1
            output.append('<blockquote><p>' + inline(' '.join(quote)) + '</p></blockquote>')
            continue
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
        i += 1
    flush()
    if details:
        output.append('</details>')
    return ''.join(output)

parts = re.split(r'^## ', source, flags=re.M)[1:]
chapters = []
for part in parts:
    title, body = part.split('\n', 1)
    chapters.append(dict(title=title, body=render(body), search=part))
data = json.dumps(chapters, ensure_ascii=False).replace('<', '\\u003c')
template = r'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C# 첫걸음 · 입문 학습 교재</title>
<style>
:root{color-scheme:light;--bg:#f5f7fa;--paper:#fff;--ink:#202c3d;--muted:#58697e;--line:#dce3eb;--accent:#185f90;--soft:#e9f2f8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.85 'Segoe UI','Malgun Gothic',sans-serif}button,input{font:inherit}button,a{touch-action:manipulation}button{cursor:pointer;border:1px solid var(--line);border-radius:7px;background:var(--paper);color:var(--ink);padding:6px 12px}button:hover{background:var(--soft)}:focus-visible{outline:3px solid #d78224;outline-offset:3px}aside{position:fixed;inset:0 auto 0 0;width:300px;background:var(--paper);border-right:1px solid var(--line);padding:28px 20px;overflow:auto}.brand{font-size:25px;font-weight:800;letter-spacing:-1px}.label{font-size:12px;letter-spacing:2px;color:var(--accent);font-weight:700}.sub{font-size:13px;color:var(--muted)}input{width:100%;padding:10px 12px;margin:22px 0 12px;border:1px solid var(--line);border-radius:7px;background:var(--bg);color:var(--ink)}nav a{display:block;text-decoration:none;color:var(--muted);font-size:14px;padding:9px 10px;border-radius:7px;margin:3px 0}nav a[aria-current=page]{color:var(--accent);background:var(--soft);font-weight:700}nav a:hover{background:var(--bg)}progress{width:100%;height:7px;accent-color:var(--accent)}main{margin-left:300px;padding:30px 6vw 60px;max-width:1300px}.toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding-bottom:18px}.toolbar span{font-size:13px;color:var(--muted)}.hero{padding:38px 0 24px}h1{font-size:clamp(27px,3vw,39px);letter-spacing:-1.2px;line-height:1.4;margin:12px 0}article{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:20px 38px 35px}h2{font-size:20px;margin:30px 0 12px;letter-spacing:-.4px}p{margin:12px 0;word-break:keep-all;overflow-wrap:anywhere}.code{margin:20px 0;border-radius:9px;overflow:hidden;background:#142235;color:#e3edf7}.codebar{display:flex;justify-content:space-between;align-items:center;padding:8px 15px;background:#20334b;font-size:12px}.copy{font-size:12px;background:#2d4664;color:white;border-color:#50657e}pre{margin:0;padding:22px;overflow:auto;line-height:1.7;font:14px/1.75 Consolas,monospace;tab-size:4}details{background:var(--soft);padding:16px 20px;border-radius:8px;margin-top:25px}summary{cursor:pointer;color:var(--accent);font-weight:700}.bottom{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:24px}.bottom button:disabled{opacity:.4;cursor:default}.done{background:var(--accent);color:white}.done:hover{background:#124b73}footer{color:var(--muted);font-size:12px;margin-top:35px}footer a{color:var(--accent)}.notice{border-left:3px solid var(--accent);padding:8px 15px;color:var(--muted);font-size:14px;margin-bottom:25px}#status{font-size:13px;color:var(--accent);min-height:24px}body.dark{color-scheme:dark;--bg:#121c29;--paper:#1a2838;--ink:#e2ebf4;--muted:#acbdd0;--line:#35485d;--accent:#80c6f2;--soft:#243c51}body.dark .done{background:#285f85;color:white}.skip{position:absolute;left:-9999px}.skip:focus{left:320px;top:10px;background:var(--paper);z-index:5}
@media(max-width:850px){aside{position:relative;width:auto;border-right:0;border-bottom:1px solid var(--line);padding:20px}nav{max-height:210px;overflow:auto}main{margin:0;padding:20px}article{padding:8px 20px 25px}.hero{padding-top:25px}.toolbar{flex-wrap:wrap}.skip:focus{left:10px}}@media print{aside,.toolbar,.bottom,.copy,#status,.notice{display:none}main{margin:0;padding:0;max-width:none}article{border:0;padding:0}body{background:white;color:black}pre{white-space:pre-wrap;color:black}.code,.codebar{background:#f0f0f0;color:black}details{display:block}details>*{display:block}footer{margin-top:20px}}
</style></head><body>
<a class="skip" href="#content">본문으로 건너뛰기</a>
<aside><div class="label">PROGRAMMING / BEGINNER</div><div class="brand">C# 첫걸음<span style="color:var(--accent)">.</span></div><div class="sub">읽고, 실행하고, 스스로 고치기</div><label for="search" class="sub">단원·본문 검색</label><input id="search" type="search" placeholder="변수, 조건문, 클래스…" autocomplete="off"><div id="progressText" class="sub"></div><progress id="progress" max="14" value="0" aria-label="완료 단원 수"></progress><nav id="toc" aria-label="강의 목차"></nav><div id="empty" class="sub" hidden>검색 결과가 없습니다.</div></aside>
<main><div class="toolbar"><span>입문 학습 교재 / Visual Studio · C#</span><div><button id="theme" aria-pressed="false">어두운 화면</button></div></div><div class="hero"><div id="counter" class="label"></div><h1 id="title"></h1><div class="sub">개념 읽기 → 코드 실행 → 결과 확인 → 직접 해보기</div></div><div class="notice">각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.</div><article id="content" tabindex="-1"></article><div class="bottom"><button id="prev">← 이전 단원</button><button id="complete" class="done">학습 완료 표시</button><button id="next">다음 단원 →</button></div><div id="status" role="status" aria-live="polite"></div><footer>학습 기록은 현재 브라우저에 저장됩니다. 파일을 이동하거나 브라우저 설정을 변경하면 기록이 유지되지 않을 수 있습니다.</footer></main>
<script>
const chapters=__DATA__;
const $=id=>document.getElementById(id);let completed=[],current=0;
try{const stored=JSON.parse(localStorage.getItem('csharp-first-completed')||'[]');if(Array.isArray(stored))completed=[...new Set(stored.filter(x=>Number.isInteger(x)&&x>=0&&x<chapters.length))];document.body.classList.toggle('dark',localStorage.getItem('csharp-first-theme')==='dark')}catch{}
function save(key,value){try{localStorage.setItem(key,value);return true}catch{$('status').textContent='브라우저 저장을 사용할 수 없습니다. 현재 화면에서는 학습을 계속할 수 있습니다.';return false}}
function themeLabel(){const dark=document.body.classList.contains('dark');$('theme').textContent=dark?'밝은 화면':'어두운 화면';$('theme').setAttribute('aria-pressed',String(dark))}
function toc(){const q=$('search').value.trim().toLocaleLowerCase();$('toc').replaceChildren();let count=0;chapters.forEach((c,i)=>{if(q&&!c.search.toLocaleLowerCase().includes(q))return;count++;const a=document.createElement('a');a.href='#lesson-'+(i+1);a.textContent=(completed.includes(i)?'✓ ':'')+c.title;if(i===current)a.setAttribute('aria-current','page');$('toc').append(a)});$('empty').hidden=count>0;$('progress').max=chapters.length;$('progress').value=completed.length;$('progressText').textContent=`학습 완료 ${completed.length} / ${chapters.length}`}
function show(){const match=location.hash.match(/^#lesson-(\d+)$/);const n=match?Number(match[1])-1:0;current=n>=0&&n<chapters.length?n:0;const c=chapters[current];$('title').textContent=c.title;document.title=c.title+' · C# 첫걸음';$('counter').textContent=`LESSON ${String(current+1).padStart(2,'0')} / ${chapters.length}`;$('content').innerHTML=c.body;$('prev').disabled=current===0;$('next').disabled=current===chapters.length-1;$('complete').textContent=completed.includes(current)?'✓ 완료됨 · 표시 취소':'학습 완료 표시';$('complete').setAttribute('aria-pressed',String(completed.includes(current)));$('status').textContent='';toc()}
function go(delta){location.hash='lesson-'+(current+1+delta)}
window.addEventListener('hashchange',()=>{show();window.scrollTo(0,0)});$('prev').onclick=()=>go(-1);$('next').onclick=()=>go(1);$('search').oninput=toc;
$('complete').onclick=()=>{completed=completed.includes(current)?completed.filter(x=>x!==current):[...completed,current];show();save('csharp-first-completed',JSON.stringify(completed))};
$('theme').onclick=()=>{document.body.classList.toggle('dark');themeLabel();save('csharp-first-theme',document.body.classList.contains('dark')?'dark':'light')};
$('content').addEventListener('click',async event=>{const button=event.target.closest('.copy');if(!button)return;const code=button.closest('.code').querySelector('code').textContent;try{if(!navigator.clipboard)throw Error();await navigator.clipboard.writeText(code);$('status').textContent='코드를 복사했습니다. Program.cs에 붙여 넣으세요.'}catch{const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(button.closest('.code').querySelector('code'));selection.removeAllRanges();selection.addRange(range);$('status').textContent='코드를 선택했습니다. Ctrl+C로 복사하세요.'}});
themeLabel();show();
</script></body></html>'''
exercises = json.loads((ROOT / 'exercises.json').read_text(encoding='utf-8'))
assert len(exercises) == len(chapters)
public_exercises = [{k: v for k, v in exercise.items() if k != 'solution'} for exercise in exercises]
practice_data = json.dumps(public_exercises, ensure_ascii=False).replace('<', '\\u003c')
page = template.replace('__DATA__', data)
page = page.replace('</style>', (ROOT / 'reading.css').read_text(encoding='utf-8') + '</style>')
page = page.replace('</style>', (ROOT / 'practice.css').read_text(encoding='utf-8') + '</style>')
page = page.replace('각 코드는 Program.cs 전체를 바꾸어 실행하세요. 코드는 Visual Studio에서 실행하며, 이 페이지에서는 문서를 읽고 복사합니다.', '개념 설명의 짧은 코드는 문법을 살펴보는 코드 조각입니다. 따라 하기의 완성 예제는 Program.cs 전체를 바꿔 실행하세요. 아래 웹 실습에서는 문제의 출력 형식에 맞춰 작성하고 채점합니다.')
page = page.replace('</script>', '\nconst exercises=' + practice_data + ';\n' + (ROOT / 'practice.js').read_text(encoding='utf-8') + '\n</script>')
(ROOT / 'index.html').write_text(page, encoding='utf-8')
print(f'생성 완료: {len(chapters)}개 단원 / {(ROOT / "index.html").stat().st_size:,} bytes')
