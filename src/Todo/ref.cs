using System;

// 1. 사물함 설계도 (참조 타입: class)
class Player
{
    public int Hp;
}

class Program
{
    // [상황 1] ref가 없을 때: 사물함 번호가 적힌 '새 포스트잇(복사본)'을 받음
    static void Change(Player p)
    {
        // p에 적힌 '1번 사물함' 문을 열고 들어가서 체력을 80으로 고침
        // (밖에 있는 hero도 똑같이 1번 사물함을 보고 있으므로 영향을 받음!)
        p.Hp = 80;

        // 2번 사물함(Hp = 1)을 새로 만들고, '내 포스트잇(p)'의 번호만 2번으로 고쳐 씀
        // (밖에 있는 hero 포스트잇은 여전히 1번 사물함이라고 적혀 있음!)
        p = new Player { Hp = 1 };
    }

    // [상황 2] ref가 있을 때: 밖에 있는 '원본 포스트잇(hero)' 자체를 직접 빌려옴
    static void Replace(ref Player p)
    {
        // 3번 사물함(Hp = 1)을 새로 만들고, '원본 포스트잇(hero)'의 번호를 3번으로 직접 고쳐 씀!
        p = new Player { Hp = 1 };
    }

    // [보너스] 값 타입(int) 비교용 함수
    static void ChangeNumberNormal(int num)
    {
        num = 20; // 복사 받은 숫자만 20으로 바꿈 (원본 영향 없음)
    }

    static void ChangeNumberRef(ref int num)
    {
        num = 20; // 원본 변수 칸 자체에 20을 덮어씀 (원본 바뀜!)
    }

    static void Main()
    {
        Console.WriteLine("=== 1. 참조 타입(class) 전달 비교 ===");

        // 1번 사물함(Hp = 100)을 만들고, hero 포스트잇에 '1번 사물함'이라고 적음
        Player hero = new Player { Hp = 100 };
        Console.WriteLine($"처음 체력: {hero.Hp}"); // 100

        // ref 없이 전달 -> 1번 사물함 안의 내용물(80)만 바뀌고, 새 객체(1) 연결은 무시됨
        Change(hero);
        Console.WriteLine($"Change(hero) 실행 후 체력: {hero.Hp}"); // 80

        // ref 붙여서 전달 -> hero 포스트잇 자체가 새 객체(1)를 가리키도록 바뀜!
        Replace(ref hero);
        Console.WriteLine($"Replace(ref hero) 실행 후 체력: {hero.Hp}"); // 1


        Console.WriteLine("\n=== 2. 값 타입(int) 전달 비교 ===");

        int myScore = 10;
        Console.WriteLine($"처음 점수: {myScore}"); // 10

        ChangeNumberNormal(myScore);
        Console.WriteLine($"ref 없이 전달 후 점수: {myScore}"); // 여전히 10

        ChangeNumberRef(ref myScore);
        Console.WriteLine($"ref 붙여서 전달 후 점수: {myScore}"); // 20으로 바뀜!
    }
}
