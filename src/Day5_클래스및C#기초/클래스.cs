// 클래스

//class Program

// 기초 문법
// 클래스를 만드는 법
// 속성과 기능
// 클래스를 사용하는 법.

// 클래스를 왜 써야할까요
// Main에서 부터 시작한다. 모든 작업을 하면된다.
// AI야 Main에 모든 코드 전부다 적어서 실행하게 만들어 C#
// 100줄 넘는코드를 한번에 보고 이해가 됐나요? X
// Main 전체 코드를 몇개의 클래스를 만들고, 이 기능들이 겹치지 않게 어떻게 사용하면 될까?

// OOP 객체지향프로그래밍

메모장.Exe();

public class Enemy
{
    public string name; // 몬스터는 이름을 문자열로 표현할 수 있다.
    public int hp;

    // 위에 정의한 속성으로 무엇을 하는가? - 기능(멤버 함수)

    // 접근지시자 반환형 함수의 이름(반환 타입)
    // public, private, protected
    public void Hello()
    {
        Console.WriteLine($"{name}의 체력 : {hp}");
    }
}

public class 메모장
{
    public static void Exe()
    {
        Enemy 슬라임a = new Enemy();
        Enemy 슬라임b = new Enemy();

        슬라임a.name = "slime_A";
        슬라임b.name = "slime_B";  

        Console.WriteLine($"슬라임의 이름 : {슬라임a.name}");
        Console.WriteLine($"슬라임의 이름 : {슬라임b.name}");

        슬라임a.Hello();
        슬라임b.Hello();
    }
}