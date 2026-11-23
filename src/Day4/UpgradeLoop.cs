int gold = 100;
int grade = 0;
int bestGrade = 0;
bool running = true;
bool exceptionInput = false;
string message = "최고 등급 +10 무기를 만들어 보세요!";


Random random = new Random();



// 무슨 반복문? 게임 -> while
// 위에 있는 변수들을 어떻게 바꿀 건지 하나씩 만드는 것.
while (running)
{
    int cost = (grade + 1) * 10;
    int chance = 90 - grade * 8;
    int sellPrice = grade * 20;

    // Render
    if(exceptionInput == false)
    {
        Console.Clear();
    }

    Console.WriteLine("=== 무기 강화 ===");
        Console.WriteLine($"골드: {gold} | 무기: +{grade} | 최고: +{bestGrade}");
        Console.WriteLine($"강화 비용: {cost} | 성공 확률: {chance}%");
        Console.WriteLine($"판매 가격: {sellPrice} | 실패하면 무기는 +0으로 돌아갑니다.");
        Console.WriteLine(message);
        Console.WriteLine("[1] 강화 [2] 팔기 [0] 종료");

    if (grade >= 10)
    {
        Console.WriteLine("+10 달성! 승리했습니다.");
        break;
    }
    if (gold < 10 && grade == 0)
    {
        Console.WriteLine($"파산! 최고 기록: +{bestGrade}");
        break;
    }

    // 입력
    string? choice = Console.ReadLine();
    if (choice == "1")
    {
        if (gold < cost)
        {
            message = " 강화 비용이 부족합니다. 무기를 팔아 보세요.";
        }
        else
        {
            gold = gold - cost; // 강화 성공
            if (random.Next(100) < chance)
            {
                grade = grade + 1;
                if (grade > bestGrade) bestGrade = grade;
                message = $"강화 성공! +{grade}";
            }
            else
            {
                grade = 0;
                message = "강화 실패! 새 +0 무기로 다시 시작합니다.";
            }
        }
    }
    else if (choice == "2")
    {
        if (grade == 0)
        {
            message = "+0 무기는 팔 수 없습니다.";
        }
        else
        {
            gold = gold + sellPrice;
            grade = 0;
            message = $"(sellPrice)골드에 판매했습니다. 새 +0 무기를 받았습니다.";
        }
    }
    else if (choice == "0" || choice == null)
    {
        running = false;
    }
    else
    {
        Console.WriteLine("1, 2, 0 중 하나를 입력하세요");
        exceptionInput = true;
    }
}