"""개인 PC용 실제 C# 실행·채점 서버. python server.py 로 시작."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
import webbrowser

ROOT = Path(__file__).resolve().parent
EXERCISES = json.loads((ROOT / 'exercises.json').read_text(encoding='utf-8'))
TOKEN = secrets.token_urlsafe(32)
SLOT = threading.BoundedSemaphore(1)
LIMIT = 32768

def stop(process):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
    else:
        import signal
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

def command(args, cwd, stdin='', timeout=5):
    """파일 대신 제한된 메모리에 출력 수집. 제한 초과/시간 초과 시 프로세스 트리 종료."""
    env = dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_NOLOGO='1',
               DOTNET_CLI_UI_LANGUAGE='en', DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1')
    process = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, env=env, start_new_session=os.name != 'nt')
    chunks, size = [], [0]
    overflow = threading.Event()
    def read():
        while True:
            block = os.read(process.stdout.fileno(), 4096)
            if not block:
                break
            room = max(0, LIMIT - size[0])
            chunks.append(block[:room])
            size[0] += len(block)
            if size[0] > LIMIT:
                overflow.set()
                break
    thread = threading.Thread(target=read, daemon=True)
    thread.start()
    try:
        process.stdin.write(stdin.encode('utf-8'))
        process.stdin.close()
    except (BrokenPipeError, OSError):
        pass
    deadline = time.monotonic() + timeout
    reason = None
    while process.poll() is None:
        if overflow.is_set():
            reason = 'output_limit'
            break
        if time.monotonic() >= deadline:
            reason = 'timeout'
            break
        time.sleep(.025)
    if reason:
        stop(process)
    process.wait()
    thread.join(timeout=2)
    if overflow.is_set():
        reason = 'output_limit'
    result = dict(code=process.returncode, output=b''.join(chunks).decode('utf-8', errors='replace'), reason=reason)
    process.stdout.close()
    return result

def framework():
    result = subprocess.run(['dotnet', '--list-sdks'], capture_output=True, text=True, encoding='utf-8')
    versions = re.findall(r'^(\d+)\.\d+\.\d+', result.stdout, re.M)
    supported = [int(v) for v in versions if int(v) >= 10]
    if not supported:
        raise RuntimeError('.NET SDK 10 이상이 필요합니다. 런타임만 설치된 경우 실행할 수 없습니다.')
    return f'net{max(supported)}.0'

FRAMEWORK = None

def normalize(value):
    return value.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n')

def execute(source, lesson, mode='grade', stdin=''):
    with tempfile.TemporaryDirectory(prefix='csharp-lesson-') as directory:
        work = Path(directory)
        (work / 'Program.cs').write_text(source, encoding='utf-8')
        # 별도 파일의 모듈 초기화자로 설정해 학생 코드의 줄 번호를 유지합니다.
        (work / 'RunnerEncoding.cs').write_text(
            'internal static class RunnerEncoding { '
            '[System.Runtime.CompilerServices.ModuleInitializer] '
            'internal static void Initialize() { '
            'System.Console.InputEncoding = new System.Text.UTF8Encoding(false); '
            'System.Console.OutputEncoding = new System.Text.UTF8Encoding(false); } }', encoding='utf-8')
        (work / 'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>', encoding='utf-8')
        (work / 'Practice.csproj').write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType>'
            f'<TargetFramework>{FRAMEWORK}</TargetFramework><ImplicitUsings>enable</ImplicitUsings>'
            '<Nullable>enable</Nullable><UseAppHost>false</UseAppHost>'
            '<RestoreSources></RestoreSources></PropertyGroup></Project>', encoding='utf-8')
        built = command(['dotnet', 'build', 'Practice.csproj', '--nologo', '-v:q',
                         '-p:UseSharedCompilation=false', '--disable-build-servers'], work, timeout=45)
        if built['reason']:
            return dict(status=built['reason'], message='컴파일 시간 또는 출력 제한을 초과했습니다.', output=built['output'])
        diagnostics = list(dict.fromkeys(re.findall(r'Program\.cs\((\d+),(\d+)\): (error|warning) (CS\d+): (.*?) \[', built['output'])))
        errors = [dict(line=int(a), column=int(b), severity=c, code=d, message=e) for a,b,c,d,e in diagnostics]
        if built['code']:
            return dict(status='compile_error', message='컴파일 오류를 먼저 수정하세요.', diagnostics=errors, output=built['output'])
        dll = work / 'bin' / 'Debug' / FRAMEWORK / 'Practice.dll'
        cases = EXERCISES[lesson]['cases'] if mode == 'grade' else [dict(input=stdin)]
        results = []
        for index, case in enumerate(cases):
            run = command(['dotnet', str(dll)], work, stdin=case['input'], timeout=3)
            actual = normalize(run['output'])
            status = run['reason'] or ('runtime_error' if run['code'] else 'ok')
            passed = status == 'ok' and (mode != 'grade' or actual == normalize(case['expected']))
            results.append(dict(number=index+1, input=case['input'], actual=actual,
                                expected=case.get('expected'), passed=passed, status=status))
            if status != 'ok':
                break
        passed = len(results) == len(cases) and all(r['passed'] for r in results)
        return dict(status=('passed' if passed else 'failed') if mode == 'grade' else results[0]['status'],
                    results=results, diagnostics=errors, total=len(cases), mode=mode)

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body, kind='application/json; charset=utf-8'):
        data = json.dumps(body, ensure_ascii=False).encode('utf-8') if isinstance(body, dict) else body
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def valid_host(self):
        return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

    def do_GET(self):
        if not self.valid_host():
            return self.reply(403, dict(message='127.0.0.1 주소로 접속하세요.'))
        if self.path in ('/', '/index.html'):
            page = (ROOT / 'index.html').read_text(encoding='utf-8').replace('</head>', f'<meta name="runner-token" content="{TOKEN}"></head>')
            return self.reply(200, page.encode('utf-8'), 'text/html; charset=utf-8')
        if self.path == '/api/health':
            return self.reply(200, dict(ready=True, framework=FRAMEWORK))
        return self.reply(404, dict(message='없는 주소입니다.'))

    def do_POST(self):
        origin = f'http://127.0.0.1:{self.server.server_port}'
        if not self.valid_host() or self.headers.get('Origin') != origin or self.headers.get('X-Runner-Token') != TOKEN:
            return self.reply(403, dict(message='교재를 로컬 서버 주소에서 다시 열어주세요.'))
        if self.path != '/api/run':
            return self.reply(404, dict(message='없는 주소입니다.'))
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 100000:
                return self.reply(413, dict(message='요청 크기가 제한을 초과했습니다.'))
            data = json.loads(self.rfile.read(length))
            source, lesson = data['source'], data['lesson']
            mode, stdin = data.get('mode', 'grade'), data.get('stdin', '')
            if not isinstance(source, str) or len(source) > 40000 or not isinstance(lesson, int) or not 0 <= lesson < len(EXERCISES):
                raise ValueError()
            if mode not in ('grade', 'run') or not isinstance(stdin, str) or len(stdin) > 8000:
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            return self.reply(400, dict(message='입력 데이터가 올바르지 않습니다.'))
        if not SLOT.acquire(blocking=False):
            return self.reply(429, dict(message='다른 코드가 실행 중입니다. 잠시 후 다시 시도하세요.'))
        try:
            self.reply(200, execute(source, lesson, mode, stdin))
        except Exception as error:
            self.reply(500, dict(message=f'실행기 오류: {type(error).__name__}'))
        finally:
            SLOT.release()

def main():
    global FRAMEWORK
    parser = argparse.ArgumentParser(description='C# 초급 교재 로컬 실행기')
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if not shutil.which('dotnet'):
        raise SystemExit('.NET SDK를 설치한 뒤 다시 실행하세요.')
    FRAMEWORK = framework()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError:
        raise SystemExit('서버를 시작할 수 없습니다. 포트 사용 여부를 확인하거나 --port 8768을 사용하세요.')
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'C# 교재: {url} ({FRAMEWORK})\n종료: Ctrl+C', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
