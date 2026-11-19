using System.Diagnostics;

namespace Todo
{
    // 주석 comment
    /*
     *  2026-11-18
     *  키워드 : namespace, internal, class, static, void, string 문법
     *  
     *  note : 키워드 문법에 따라서 결정된 이름
     *  Main / WriteLine
     *  Program : 클래스.
     *  Main(  )    /   WriteLine( )
     *
     *
     */

    /*
     *  게임에서 처음에 게임 제목 타이틀이 나오고 그 아래에 플레이가 가능한 플레이어 이름 만드는거 구현해보세요?
     *  
     *  제목 - 문자열
     *  
     *  <입출력>
     *  stpe1. 자연어 -> 프로그래밍 언어로 바꾸고 -> 실행 가능한가?
     *  step2. 효율적인가? 왜 이런 이유로 선택했는지 근거를 말할 수 있는가? - 알고리즘
     *  
     *  [모험가 길드 ver] [1.0.0] 1. 자릿수 순서대로 호환, 메인, 사소한버그
     *  
     */

    internal class Program
    {
        int age = 25;
        int year = 2024;
        int temperature = -5;

        static void Main(string[] args)
        {
            // 텍스트, 실수, 정수
            // string 문자열       "..... " / "" 없으면 에러가 뜬다. -> 컨텍스트가 없음 이라고 뜬다.
            // 변수 -> 타입을 누가 정의했는가? -> 만든 사람

            string title = "모험가 길드"; // =는 오른쪽을 왼쪽에 대입한다라는 의미.
            float version = 1.00f;
            int hp = 10 -1;

            // C# 콘솔에서 출력을 할것인데 타이틀 이름은 @@@ 이고 버전은 1.0으로 출력하는 코드
            Console.WriteLine($"{title} {version}");
            Console.WriteLine(title); // 문자열 - string
            Console.WriteLine(hp);      // 정수 - int 
            Console.WriteLine(1.1f); // 1 이 나온다. 1.0적었을때 실수가 안나오네? 어떻게 해야 실수를 표현할 수 있을까
            Console.WriteLine(false);

            Console.ReadLine(); // 내가 작성한 것을 읽어오는 것.
        }
    }
}