"""새 PC에서 실제 C# 컴파일과 한글 입출력을 검사합니다. Node.js 불필요."""
import sys
import server

try:
    server.FRAMEWORK = server.framework()
    result = server.execute('System.Console.WriteLine(System.Console.ReadLine());', 0,
                            mode='run', stdin='설치 확인 성공\n')
    if result['status'] != 'ok' or result['results'][0]['actual'] != '설치 확인 성공':
        print('실행 검증 실패:', result)
        sys.exit(1)
    print(f'검증 성공: {server.FRAMEWORK} 컴파일, 실행, 한글 입출력')
except Exception as error:
    print(f'실행 검증 오류: {type(error).__name__}: {error}')
    sys.exit(1)
