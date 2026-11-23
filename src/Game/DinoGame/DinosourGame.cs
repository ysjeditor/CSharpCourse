using System.Text;


class Dinosour
{
    // 화면 및 지형 설정
    const int WIDTH = 60;
    const int HEIGHT = 15;
    const int GROUND_Y = 12;

    // 공룡 물리 및 상태
    const int DINO_X = 6;
    static float dinoY = GROUND_Y;
    static float velocityY = 0f;
    const float GRAVITY = 0.65f;
    const float JUMP_FORCE = -2.4f;
    static bool isDucking = false;
    static int runAnimFrame = 0;

    // 장애물 관리
    class Obstacle
    {
        public int X;
        public int Y;
        public int Width;
        public int Height;
        public bool IsBird; // false: 선인장, true: 익룡
    }

    static List<Obstacle> obstacles = new List<Obstacle>();
    static int spawnTimer = 0;
    static Random rand = new Random();

    // 게임 진행 상태
    static int score = 0;
    static int highScore = 0;
    static bool isGameOver = false;
    static int gameSpeedMs = 45; // 숫자가 작을수록 빨라짐

    public static void Run()
    {
        Console.CursorVisible = false;
        Console.OutputEncoding = Encoding.UTF8;

        while (true)
        {
            ResetGame();

            // 메인 게임 루프 (Input -> Update -> Rendering)
            while (!isGameOver)
            {
                Input();
                Update();
                Rendering();
                Thread.Sleep(gameSpeedMs);
            }

            // 게임 오버 및 재시작 대기
            ShowGameOver();
            while (true)
            {
                if (Console.KeyAvailable)
                {
                    var key = Console.ReadKey(true).Key;
                    if (key == ConsoleKey.Spacebar || key == ConsoleKey.R) break;
                    if (key == ConsoleKey.Escape) return;
                }
                Thread.Sleep(20);
            }
        }
    }

    static void ResetGame()
    {
        dinoY = GROUND_Y;
        velocityY = 0f;
        isDucking = false;
        obstacles.Clear();
        spawnTimer = 20;
        score = 0;
        isGameOver = false;
        gameSpeedMs = 45;
        Console.Clear();
    }

    // 1. 입력 처리 (스페이스/위 화살표: 점프, 아래 화살표: 숙이기)
    static void Input()
    {
        bool downPressed = false;

        while (Console.KeyAvailable)
        {
            ConsoleKey key = Console.ReadKey(true).Key;

            // 땅에 있을 때만 점프 가능
            if ((key == ConsoleKey.Spacebar || key == ConsoleKey.UpArrow || key == ConsoleKey.W) && dinoY >= GROUND_Y)
            {
                velocityY = JUMP_FORCE;
                isDucking = false;
            }
            else if (key == ConsoleKey.DownArrow || key == ConsoleKey.S)
            {
                downPressed = true;
            }
            else if (key == ConsoleKey.Escape)
            {
                Environment.Exit(0);
            }
        }

        // 아래 키를 누르면 숙이기 토글/유지 (공중에서는 급강하)
        if (downPressed)
        {
            if (dinoY < GROUND_Y)
            {
                velocityY += 1.2f; // 공중 급강하
            }
            else
            {
                isDucking = !isDucking; // 땅에서는 숙이기 전환
            }
        }
    }

    // 2. 업데이트 (중력 물리, 장애물 이동/생성, 충돌 판정, 점수)
    static void Update()
    {
        // 공룡 점프 및 중력 계산
        if (dinoY < GROUND_Y || velocityY < 0)
        {
            dinoY += velocityY;
            velocityY += GRAVITY;

            if (dinoY >= GROUND_Y)
            {
                dinoY = GROUND_Y;
                velocityY = 0f;
            }
        }

        // 달리기 다리 애니메이션 프레임
        runAnimFrame = (runAnimFrame + 1) % 2;

        // 점수 증가 및 난이도(속도) 상승
        score++;
        if (score > highScore) highScore = score;
        if (score % 150 == 0 && gameSpeedMs > 20)
        {
            gameSpeedMs -= 2;
        }

        // 장애물 생성 타이머
        spawnTimer--;
        if (spawnTimer <= 0)
        {
            SpawnObstacle();
            spawnTimer = rand.Next(24, 48);
        }

        // 공룡 히트박스 계산 (숙이면 키가 1칸으로 줄어듦)
        int dinoBottom = (int)Math.Round(dinoY);
        int dinoHeight = isDucking ? 1 : 2;
        int dinoTop = dinoBottom - dinoHeight + 1;

        // 장애물 이동 및 충돌 체크
        for (int i = obstacles.Count - 1; i >= 0; i--)
        {
            Obstacle obs = obstacles[i];
            obs.X--;

            // 화면 왼쪽 밖으로 나가면 제거
            if (obs.X + obs.Width < 0)
            {
                obstacles.RemoveAt(i);
                continue;
            }

            // AABB 충돌 판정
            int obsLeft = obs.X;
            int obsRight = obs.X + obs.Width - 1;
            int obsBottom = obs.Y;
            int obsTop = obs.Y - obs.Height + 1;

            bool overlapX = (DINO_X + 1 >= obsLeft) && (DINO_X <= obsRight);
            bool overlapY = (dinoBottom >= obsTop) && (dinoTop <= obsBottom);

            if (overlapX && overlapY)
            {
                isGameOver = true;
            }
        }
    }

    static void SpawnObstacle()
    {
        // 점수가 150점 이상이면 익룡(공중 장애물)도 등장
        bool spawnBird = (score >= 150) && (rand.Next(100) < 35);

        if (spawnBird)
        {
            // 익룡 높이: 서 있으면 부딪히고 숙이면 피해지는 높이(GROUND_Y - 1) 또는 점프 높이
            int birdY = (rand.Next(2) == 0) ? GROUND_Y - 1 : GROUND_Y - 3;
            obstacles.Add(new Obstacle
            {
                X = WIDTH - 2,
                Y = birdY,
                Width = 2,
                Height = 1,
                IsBird = true
            });
        }
        else
        {
            // 선인장 (1~2칸 높이, 1~2칸 폭)
            int height = rand.Next(1, 3);
            int width = rand.Next(1, 3);
            obstacles.Add(new Obstacle
            {
                X = WIDTH - 2,
                Y = GROUND_Y,
                Width = width,
                Height = height,
                IsBird = false
            });
        }
    }

    // 3. 렌더링 (버퍼에 맵을 그린 뒤 한 번에 콘솔 출력)
    static void Rendering()
    {
        char[,] buffer = new char[HEIGHT, WIDTH];

        // 배경 초기화
        for (int y = 0; y < HEIGHT; y++)
        {
            for (int x = 0; x < WIDTH; x++)
            {
                if (y == GROUND_Y + 1)
                    buffer[y, x] = ((x + score) % 7 == 0) ? '.' : '─'; // 움직이는 지면 효과
                else
                    buffer[y, x] = ' ';
            }
        }

        // 장애물 그리기
        foreach (var obs in obstacles)
        {
            for (int dy = 0; dy < obs.Height; dy++)
            {
                for (int dx = 0; dx < obs.Width; dx++)
                {
                    int drawX = obs.X + dx;
                    int drawY = obs.Y - dy;
                    if (drawX >= 0 && drawX < WIDTH && drawY >= 0 && drawY < HEIGHT)
                    {
                        buffer[drawY, drawX] = obs.IsBird ? (runAnimFrame == 0 ? 'W' : 'M') : 'Ψ';
                    }
                }
            }
        }

        // 공룡 그리기
        int dinoDrawY = (int)Math.Round(dinoY);
        if (isDucking)
        {
            // 숙인 공룡 (납작한 1줄)
            buffer[dinoDrawY, DINO_X] = '▄';
            buffer[dinoDrawY, DINO_X + 1] = '►';
        }
        else
        {
            // 서 있는 공룡 (머리 + 다리 애니메이션)
            if (dinoDrawY - 1 >= 0)
            {
                buffer[dinoDrawY - 1, DINO_X] = '█';
                buffer[dinoDrawY - 1, DINO_X + 1] = '▀';
            }
            buffer[dinoDrawY, DINO_X] = (runAnimFrame == 0) ? '┘' : '└';
            buffer[dinoDrawY, DINO_X + 1] = (runAnimFrame == 0) ? '└' : '┘';
        }

        // 문자열로 합쳐서 출력
        Console.SetCursorPosition(0, 0);
        StringBuilder sb = new StringBuilder();
        sb.AppendLine($"  HI {highScore:D5}   SCORE {score:D5}   |  점프: Space/↑  숙이기: ↓");
        sb.AppendLine(new string('=', WIDTH));

        for (int y = 0; y < HEIGHT; y++)
        {
            for (int x = 0; x < WIDTH; x++)
            {
                sb.Append(buffer[y, x]);
            }
            sb.AppendLine();
        }

        Console.Write(sb.ToString());
    }

    static void ShowGameOver()
    {
        Console.SetCursorPosition(WIDTH / 2 - 12, HEIGHT / 2 - 1);
        Console.Write("========================");
        Console.SetCursorPosition(WIDTH / 2 - 12, HEIGHT / 2);
        Console.Write("      G A M E  O V E R  ");
        Console.SetCursorPosition(WIDTH / 2 - 12, HEIGHT / 2 + 1);
        Console.Write("  다시 시작: Space / R  ");
        Console.SetCursorPosition(WIDTH / 2 - 12, HEIGHT / 2 + 2);
        Console.Write("========================");
    }
}