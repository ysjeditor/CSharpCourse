Console.Write("분을 입력하세요: ");

// 1. 사용자가 입력한 글자를 숫자(minutes)로 변환
if (int.TryParse(Console.ReadLine(), out int minutes))
{
    // 음수 입력 방지 (힌트 반영)
    if (minutes < 0)
    {
        Console.WriteLine("0 이상의 숫자를 입력해주세요.");
        return;
    }

    // 2. 시간과 남은 분 계산
    int hours = minutes / 60;           // 60으로 나눈 몫 = 시간
    int remainingMinutes = minutes % 60; // 60으로 나눈 나머지 = 남은 분

    Console.WriteLine($"{minutes}분은 {hours}시간 {remainingMinutes}분입니다.");
}
else
{
    Console.WriteLine("정수로 입력해주세요.");
}