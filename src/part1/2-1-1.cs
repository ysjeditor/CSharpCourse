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