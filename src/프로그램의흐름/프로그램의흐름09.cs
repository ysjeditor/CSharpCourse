static void FirstWrittenMethod()
{
    Console.WriteLine("2. 저는 코드상 맨 위에 적혀있지만, Main이 불러줄 때 실행됩니다.");
}

static void Main(string[] args)
{
    Console.WriteLine("1. 프로그램 시작! 실행 흐름은 무조건 Main으로 가장 먼저 들어옵니다.");

    FirstWrittenMethod();

    Console.WriteLine("3. Main의 마지막 줄까지 실행되면 프로그램이 종료됩니다.");
}