
namespace Todo
{
    class Game
    {
        // 게임 상태 변수 (클래스 내부에서 공유)
        static int width = 30;
        static int height = 15;

        static int playerX = width / 2;
        static int playerY = height - 2;

        static Random rand = new Random();
        static int enemyX = rand.Next(1, width - 1);
        static int enemyY = 1;

        static int score = 0;
        static bool isGameOver = false;

        // 게임의 전체 실행 흐름을 관리하는 진입점
        public static void Run()
        {
            Console.CursorVisible = false;

            while (!isGameOver)
            {
                Input();
                Update();
                Rendering();
                Thread.Sleep(60); // FPS 조절
            }

            // 게임 오버 화면 출력
            Console.Clear();
            Console.WriteLine("=====================");
            Console.WriteLine("     GAME OVER!      ");
            Console.WriteLine($"   최종 점수: {score}    ");
            Console.WriteLine("=====================");
        }

        // 1. 입력 기능: 키보드 조작 처리
        static void Input()
        {
            if (Console.KeyAvailable)
            {
                ConsoleKeyInfo keyInfo = Console.ReadKey(true);
                if (keyInfo.Key == ConsoleKey.LeftArrow && playerX > 1)
                {
                    playerX--;
                }
                else if (keyInfo.Key == ConsoleKey.RightArrow && playerX < width - 2)
                {
                    playerX++;
                }
                else if (keyInfo.Key == ConsoleKey.Escape)
                {
                    isGameOver = true;
                }
            }
        }

        // 2. 업데이트 기능: 게임 데이터 및 충돌 판정 계산
        static void Update()
        {
            enemyY++;

            // 장애물이 바닥에 도달하면 점수 증가 및 위치 재설정
            if (enemyY >= height - 1)
            {
                enemyY = 1;
                enemyX = rand.Next(1, width - 1);
                score += 10;
            }

            // 플레이어와 장애물 충돌 체크
            if (playerX == enemyX && playerY == enemyY)
            {
                isGameOver = true;
            }
        }

        // 3. 렌더링 기능: 현재 상태를 콘솔 화면에 출력
        static void Rendering()
        {
            Console.SetCursorPosition(0, 0);

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    if (y == 0 || y == height - 1 || x == 0 || x == width - 1)
                    {
                        Console.Write("#"); // 벽
                    }
                    else if (x == playerX && y == playerY)
                    {
                        Console.Write("A"); // 플레이어
                    }
                    else if (x == enemyX && y == enemyY)
                    {
                        Console.Write("V"); // 장애물
                    }
                    else
                    {
                        Console.Write(" "); // 빈 공간
                    }
                }
                Console.WriteLine();
            }

            Console.WriteLine($"점수: {score} | 조작: ← → | 종료: ESC");
        }
    }
}