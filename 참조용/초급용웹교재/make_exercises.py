"""초급 교재 실습 원본. 수정 뒤 python make_exercises.py && python build.py."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
items = []

def add(title, goal, starter, cases, hint, solution):
    items.append(dict(title=title, goal=goal, starter=starter,
        cases=[dict(input=i, expected=o) for i, o in cases], hint=hint,
        solution=solution))

add('첫 C# 실행', '두 줄에 C# 기초편, 실행 성공을 순서대로 출력하세요.',
    'using System;\n\n// Console.WriteLine으로 두 줄을 출력하세요.\n',
    [('', 'C# 기초편\n실행 성공')], 'WriteLine을 두 번 호출합니다.',
    'using System; Console.WriteLine("C# 기초편"); Console.WriteLine("실행 성공");')

add('입력 검증과 가격 계산', '정수 가격을 읽어 2개 가격만 출력하세요. 0~1000000 밖의 값이나 문자는 입력오류입니다.',
    'using System;\n\n// 입력을 검증한 뒤 계산하세요.\n',
    [('1200\n','2400'),('0\n','0'),('1000000\n','2000000'),('-1\n','입력오류'),('1000001\n','입력오류'),('abc\n','입력오류'),('','입력오류')],
    'TryParse 성공 여부와 범위를 함께 확인합니다.',
    'using System; if(int.TryParse(Console.ReadLine(),out int p)&&p>=0&&p<=1000000) Console.WriteLine(p*2); else Console.WriteLine("입력오류");')

add('짝수 합계', '0~1000의 정수 n을 읽어 1부터 n까지 짝수의 합만 출력하세요. 유효하지 않으면 입력오류입니다.',
    'using System;\n\n// 입력 검증, 누적 변수, 반복문을 작성하세요.\n',
    [('6\n','12'),('0\n','0'),('1\n','0'),('2\n','2'),('1000\n','250500'),('-1\n','입력오류'),('1001\n','입력오류'),('abc\n','입력오류')],
    '합계를 반복문 밖에서 0으로 만들고 짝수만 더합니다.',
    'using System; if(!int.TryParse(Console.ReadLine(),out int n)||n<0||n>1000){Console.WriteLine("입력오류");return;} int sum=0;for(int i=1;i<=n;i++)if(i%2==0)sum+=i;Console.WriteLine(sum);')

add('배열 최댓값', '세 줄의 정수를 배열에 담아 최댓값만 출력하세요. 음수와 중복을 허용합니다.',
    'using System;\n\nint[] values = { int.Parse(Console.ReadLine()!), int.Parse(Console.ReadLine()!), int.Parse(Console.ReadLine()!) };\n// 최댓값을 구하세요.\n',
    [('70\n90\n80\n','90'),('-8\n-2\n-5\n','-2'),('9\n9\n1\n','9'),('0\n-1\n-2\n','0')],
    '첫 요소로 max를 초기화하세요.',
    'using System; int[] a={int.Parse(Console.ReadLine()!),int.Parse(Console.ReadLine()!),int.Parse(Console.ReadLine()!)};int m=a[0];foreach(int x in a)if(x>m)m=x;Console.WriteLine(m);')

add('학생 번호 검색', '101은 지수, 102는 현우입니다. 번호를 읽어 이름을 출력하고, 없는 번호나 문자에는 없음이라고 출력하세요.',
    'using System;\nusing System.Collections.Generic;\n\nvar students = new Dictionary<int,string> { {101,"지수"}, {102,"현우"} };\n// 입력을 검증하고 조회하세요.\n',
    [('101\n','지수'),('102\n','현우'),('999\n','없음'),('abc\n','없음')],
    'TryParse와 TryGetValue를 차례로 사용합니다.',
    'using System;using System.Collections.Generic;var s=new Dictionary<int,string>{{101,"지수"},{102,"현우"}};if(int.TryParse(Console.ReadLine(),out int n)&&s.TryGetValue(n,out string? name))Console.WriteLine(name);else Console.WriteLine("없음");')

add('문자열 정리', '쉼표로 구분한 한 줄의 앞뒤 공백과 빈 항목을 제거하고 영문을 대문자로 바꾸어 /로 연결하세요. 남은 항목이 없으면 없음입니다.',
    'using System;\nusing System.Text;\n\nstring input = Console.ReadLine() ?? "";\n// 분리, 정리, 연결을 작성하세요.\n',
    [(' a,, b \n','A/B'),('apple, banana\n','APPLE/BANANA'),(' , , \n','없음'),('\n','없음'),(' 지수, csharp \n','지수/CSHARP')],
    'TrimEntries와 RemoveEmptyEntries로 나눈 뒤 StringBuilder에 누적합니다.',
    '''using System;using System.Text;
string[] words=(Console.ReadLine()??"").Split(',',StringSplitOptions.TrimEntries|StringSplitOptions.RemoveEmptyEntries);
var b=new StringBuilder();foreach(string w in words){if(b.Length>0)b.Append('/');b.Append(w.ToUpperInvariant());}Console.WriteLine(words.Length==0?"없음":b.ToString());''')

add('계산 메서드', '가격과 수량을 두 줄로 입력받아 Total 메서드가 반환한 곱만 출력하세요. 입력은 각각 0~10000의 정수입니다.',
    'using System;\n\nint price = int.Parse(Console.ReadLine()!);\nint quantity = int.Parse(Console.ReadLine()!);\nConsole.WriteLine(Total(price, quantity));\n\nstatic int Total(int price, int quantity)\n{\n    // 결과를 반환하세요.\n}\n',
    [('100\n3\n','300'),('0\n5\n','0'),('10000\n10000\n','100000000')],
    '메서드는 곱을 반환하고 호출부가 출력합니다.',
    'using System;int p=int.Parse(Console.ReadLine()!),q=int.Parse(Console.ReadLine()!);Console.WriteLine(Total(p,q));static int Total(int price,int quantity)=>price*quantity;')

add('재귀 팩토리얼', '0~12의 정수 n을 읽어 재귀 함수로 n!을 출력하세요. 유효하지 않은 입력은 입력오류입니다.',
    'using System;\n\n// 입력을 검증한 뒤 Factorial을 호출하세요.\n\nstatic long Factorial(int n)\n{\n    // 종료 조건과 재귀 호출을 작성하세요.\n    return 0;\n}\n',
    [('0\n','1'),('1\n','1'),('5\n','120'),('12\n','479001600'),('-1\n','입력오류'),('13\n','입력오류'),('abc\n','입력오류')],
    '0!은 1이며 나머지는 n * Factorial(n-1)입니다.',
    'using System;if(int.TryParse(Console.ReadLine(),out int n)&&n>=0&&n<=12)Console.WriteLine(Factorial(n));else Console.WriteLine("입력오류");static long Factorial(int n)=>n==0?1:n*Factorial(n-1);')

assert len(items) == 8
(ROOT / 'exercises.json').write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(items)}개 실습, {sum(len(x["cases"]) for x in items)}개 입력 생성')
