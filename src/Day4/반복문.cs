// 반복문
// 반복표현식을 줄일 수 있는 방법이 있을까?
// 프로그래머 반복을 진짜 싫어한다(ex 클래스)

// for반복문

// while반복문

//for (int a = 0; a < 10; a++)
//{
//    Console.WriteLine(a);
//}

// for반복문은, 100번 반복할거야. 반복횟수 눈에 보일때만 쓰면 효율적이다.

// while반복문
// 무한 반복문.

int grade = 0;
bool gameFinish = grade >= 10;
while (true)
{
    grade++;
    Console.WriteLine($"현재 등급 : {grade}");

    if (grade >= 10)
    {
        break;
    }
}

Console.WriteLine("게임 종료");
