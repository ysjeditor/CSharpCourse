using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

namespace Todo
{
    class Game2
    {
        // Windows API: 마우스 버튼 실시간 감지
        [DllImport("user32.dll")]
        static extern short GetAsyncKeyState(int vKey);
        const int VK_LBUTTON = 0x01; // 마우스 좌클릭
        const int VK_RBUTTON = 0x02; // 마우스 우클릭

        // Windows API: 콘솔 빠른 편집 모드(클릭 시 화면 멈춤) 해제용
        [DllImport("kernel32.dll", SetLastError = true)]
        static extern IntPtr GetStdHandle(int nStdHandle);

        [DllImport("kernel32.dll")]
        static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);

        [DllImport("kernel32.dll")]
        static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);

        const int STD_INPUT_HANDLE = -10;
        const uint ENABLE_QUICK_EDIT_MODE = 0x0040;
        const uint ENABLE_EXTENDED_FLAGS = 0x0080;

        static bool prevLeftClick = false;
        static bool prevRightClick = false;

        // 맵 크기 및 설정
        const int WIDTH = 44;
        const int HEIGHT = 18;
        static char[,] map = new char[HEIGHT, WIDTH];

        // 오브젝트 체력 관리 (좌표 -> 남은 내구도)
        static Dictionary<(int x, int y), int> resourceHp = new Dictionary<(int x, int y), int>();

        // 플레이어 상태
        static int playerX = 5;
        static int playerY = 8;
        static int dirX = 1; // 플레이어가 바라보는 방향
        static int dirY = 0;

        // 인벤토리 및 재화
        static int woodCount = 0;
        static int stoneCount = 0;
        static long gold = 0;
        static Dictionary<string, int> fishInventory = new Dictionary<string, int>()
        {
            { "피라미 (일반)", 0 },
            { "붕어 (고급)", 0 },
            { "잉어 (희귀)", 0 },
            { "황금쏘가리 (영웅)", 0 },
            { "전설의 용왕잉어 (전설)", 0 }
        };

        // UI 및 시스템 상태
        static bool showInventory = false;
        static string statusMessage = "WASD: 이동 | 좌클릭: 채집/낚아채기 | 우클릭: 찌 던지기 | I: 가방";
        static Random rand = new Random();

        // 낚시 시스템 상태
        enum FishingState { None, Casting, Biting }
        static FishingState fishState = FishingState.None;
        static int fishTimer = 0;
        static int biteWindow = 0;
        static int bobberX = -1, bobberY = -1;

        // 콘솔 클릭 멈춤 현상 방지 설정
        static void InitConsole()
        {
            Console.CursorVisible = false;
            Console.OutputEncoding = Encoding.UTF8;

            IntPtr consoleHandle = GetStdHandle(STD_INPUT_HANDLE);
            if (GetConsoleMode(consoleHandle, out uint consoleMode))
            {
                consoleMode &= ~ENABLE_QUICK_EDIT_MODE; // 빠른 편집 모드 끄기
                consoleMode |= ENABLE_EXTENDED_FLAGS;
                SetConsoleMode(consoleHandle, consoleMode);
            }
        }

        // 게임 실행 진입점
        public static void Run()
        {
            InitConsole();
            InitMap();

            // 클리어 조건: 나무 100개, 바위 100개, 골드 50만원 이상
            while (!(woodCount >= 100 && stoneCount >= 100 && gold >= 500000))
            {
                Input();
                Update();
                Rendering();
                Thread.Sleep(50); // 약 20 FPS
            }

            // 클리어 화면
            Console.Clear();
            Console.WriteLine("==================================================");
            Console.WriteLine("         🎉 축하합니다! 게임 클리어! 🎉           ");
            Console.WriteLine("==================================================");
            Console.WriteLine($"  최종 나무: {woodCount}개");
            Console.WriteLine($"  최종 바위: {stoneCount}개");
            Console.WriteLine($"  최종 골드: {gold:N0} G");
            Console.WriteLine("==================================================");
        }

        // 초기 맵 및 자원 생성
        static void InitMap()
        {
            for (int y = 0; y < HEIGHT; y++)
            {
                for (int x = 0; x < WIDTH; x++)
                {
                    if (y == 0 || y == HEIGHT - 1 || x == 0 || x == WIDTH - 1)
                    {
                        map[y, x] = '#'; // 외곽 울타리
                    }
                    else if (x >= WIDTH - 12 && y >= 3 && y <= HEIGHT - 4)
                    {
                        map[y, x] = '~'; // 오른쪽 낚시터 연못
                    }
                    else
                    {
                        map[y, x] = '.'; // 초원 바닥
                    }
                }
            }

            // 초기 나무(T)와 바위(O) 배치
            SpawnResources(28);
        }

        static void SpawnResources(int count)
        {
            for (int i = 0; i < count; i++)
            {
                int rx = rand.Next(2, WIDTH - 14);
                int ry = rand.Next(2, HEIGHT - 2);

                if (map[ry, rx] == '.' && !(rx == playerX && ry == playerY))
                {
                    bool isTree = rand.Next(2) == 0;
                    map[ry, rx] = isTree ? 'T' : 'O'; // T: 온전한 나무, O: 온전한 바위
                    resourceHp[(rx, ry)] = 3; // 3번 캘 수 있는 내구도 부여
                }
            }
        }

        // 1. 입력 처리 (WASD, I키, 마우스 좌/우클릭)
        static void Input()
        {
            // 키보드 입력 처리
            while (Console.KeyAvailable)
            {
                ConsoleKeyInfo keyInfo = Console.ReadKey(true);
                ConsoleKey key = keyInfo.Key;

                if (key == ConsoleKey.I)
                {
                    showInventory = !showInventory;
                    statusMessage = showInventory ? "인벤토리를 열었습니다. (I키로 닫기)" : "초원으로 돌아왔습니다.";
                    return;
                }

                if (showInventory) return; // 인벤토리 열려있을 땐 이동 제한

                // 낚시 중 이동하면 낚시 취소
                int nextX = playerX;
                int nextY = playerY;

                if (key == ConsoleKey.W) { nextY--; dirX = 0; dirY = -1; }
                else if (key == ConsoleKey.S) { nextY++; dirX = 0; dirY = 1; }
                else if (key == ConsoleKey.A) { nextX--; dirX = -1; dirY = 0; }
                else if (key == ConsoleKey.D) { nextX++; dirX = 1; dirY = 0; }

                if (nextX != playerX || nextY != playerY)
                {
                    if (fishState != FishingState.None)
                    {
                        fishState = FishingState.None;
                        bobberX = -1;
                        statusMessage = "움직여서 낚시가 취소되었습니다.";
                    }

                    // 빈 초원('.')으로만 이동 가능
                    if (map[nextY, nextX] == '.')
                    {
                        playerX = nextX;
                        playerY = nextY;
                    }
                }
            }

            if (showInventory) return;

            // 마우스 클릭 에지(누르는 순간) 감지
            bool currLeft = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;
            bool currRight = (GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0;

            bool leftClicked = currLeft && !prevLeftClick;
            bool rightClicked = currRight && !prevRightClick;

            prevLeftClick = currLeft;
            prevRightClick = currRight;

            int targetX = playerX + dirX;
            int targetY = playerY + dirY;

            // [우클릭] 낚시터 앞에서 찌 던지기
            if (rightClicked)
            {
                if (fishState == FishingState.None && map[targetY, targetX] == '~')
                {
                    fishState = FishingState.Casting;
                    bobberX = targetX;
                    bobberY = targetY;
                    fishTimer = rand.Next(25, 65); // 입질까지 대기 시간
                    statusMessage = "🎣 찌를 던졌습니다! 물고기가 물기를 기다리는 중...";
                }
                else if (fishState != FishingState.None)
                {
                    fishState = FishingState.None;
                    bobberX = -1;
                    statusMessage = "낚싯대를 거두었습니다.";
                }
                else
                {
                    statusMessage = "낚시터 물가(~)를 바라보고 우클릭해야 찌를 던질 수 있습니다!";
                }
            }

            // [좌클릭] 나무/바위 채집 또는 물고기 낚아채기
            if (leftClicked)
            {
                // 1) 낚시 중일 때 좌클릭
                if (fishState == FishingState.Biting)
                {
                    CatchFish();
                    fishState = FishingState.None;
                    bobberX = -1;
                }
                else if (fishState == FishingState.Casting)
                {
                    fishState = FishingState.None;
                    bobberX = -1;
                    statusMessage = "너무 일찍 당겼습니다! 물고기가 도망갔습니다.";
                }
                // 2) 나무 또는 바위 채집
                else if (resourceHp.ContainsKey((targetX, targetY)))
                {
                    HarvestResource(targetX, targetY);
                }
            }
        }

        // 나무 및 바위 채집 & 갈려나가는 시각 연출
        static void HarvestResource(int x, int y)
        {
            char tile = map[y, x];
            bool isTree = (tile == 'T' || tile == 't' || tile == ';');

            resourceHp[(x, y)]--;
            int hp = resourceHp[(x, y)];

            if (isTree)
            {
                int gained = rand.Next(3, 7); // 한 번 캘 때마다 3~6개 획득
                woodCount += gained;

                // 체력에 따라 나무가 갈려나가는 모양 변화: T -> t -> ; -> .
                if (hp == 2) { map[y, x] = 't'; statusMessage = $"🪓 나무를 깎아냈습니다! (+{gained} 나무) [남은 내구도: 2]"; }
                else if (hp == 1) { map[y, x] = ';'; statusMessage = $"🪓 나무 밑동만 남았습니다! (+{gained} 나무) [남은 내구도: 1]"; }
                else
                {
                    map[y, x] = '.';
                    resourceHp.Remove((x, y));
                    statusMessage = $"🌲 나무를 완전히 베어냈습니다! (+{gained} 나무)";
                }
            }
            else
            {
                int gained = rand.Next(3, 7);
                stoneCount += gained;

                // 체력에 따라 바위가 부서지는 모양 변화: O -> o -> * -> .
                if (hp == 2) { map[y, x] = 'o'; statusMessage = $"⛏️ 바위에 금이 갔습니다! (+{gained} 바위) [남은 내구도: 2]"; }
                else if (hp == 1) { map[y, x] = '*'; statusMessage = $"⛏️ 바위가 산산조각 나기 직전입니다! (+{gained} 바위) [남은 내구도: 1]"; }
                else
                {
                    map[y, x] = '.';
                    resourceHp.Remove((x, y));
                    statusMessage = $"🪨 바위를 완전히 채굴했습니다! (+{gained} 바위)";
                }
            }
        }
        // 물고기 낚기 확률 및 보상 계산 (최대 100만 골드)
        static void CatchFish()
        {
            int roll = rand.Next(1, 101); // 1 ~ 100 확률
            string fishName;
            long reward;
            if (roll <= 40) // 40%
            {
                fishName = "피라미 (일반)";
                reward = 5000;
            }
            else if (roll <= 70) // 30%
            {
                fishName = "붕어 (고급)";
                reward = 25000;
            }
            else if (roll <= 88) // 18%
            {
                fishName = "잉어 (희귀)";
                reward = 100000;
            }
            else if (roll <= 96) // 8%
            {
                fishName = "황금쏘가리 (영웅)";
                reward = 300000;
            }
            else // 4%
            {
                fishName = "전설의 용왕잉어 (전설)";
                reward = 1000000;
            }
            fishInventory[fishName]++;
            gold += reward;
            statusMessage = $"🎉 월척! [{fishName}] 낚시 성공! (+{reward:N0} G 획득)";
        }
        // 2. 게임 로직 업데이트 (낚시 타이머, 자원 리젠)
        static void Update()
        {
            if (showInventory) return;
            // 낚시 입질 타이머 진행
            if (fishState == FishingState.Casting)
            {
                fishTimer--;
                if (fishTimer <= 0)
                {
                    fishState = FishingState.Biting;
                    biteWindow = 35; // 약 1.75초 동안 좌클릭 기회 제공
                    statusMessage = "❗❗ [입질 왔다!!] 지금 즉시 마우스 [좌클릭] 하세요!! ❗❗";
                }
            }
            else if (fishState == FishingState.Biting)
            {
                biteWindow--;
                if (biteWindow <= 0)
                {
                    fishState = FishingState.None;
                    bobberX = -1;
                    statusMessage = "💨 놓쳤습니다! 물고기가 미끼만 먹고 도망갔습니다.";
                }
            }
            // 초원에 자원이 부족해지면 자동으로 새 나무/바위 생성
            if (resourceHp.Count < 12)
            {
                SpawnResources(10);
            }
        }
        // 3. 화면 렌더링
        static void Rendering()
        {
            Console.SetCursorPosition(0, 0);
            StringBuilder sb = new StringBuilder();
            // 상단 목표 현황판
            sb.AppendLine("==========================================================");
            sb.AppendLine($" [목표] 나무: {woodCount}/100 | 바위: {stoneCount}/100 | 골드: {gold:N0} / 500,000 G");
            sb.AppendLine("==========================================================");
            if (showInventory)
            {
                // 인벤토리 화면 출력
                sb.AppendLine("                    🎒 [ 인벤토리 ]                       ");
                sb.AppendLine("----------------------------------------------------------");
                sb.AppendLine($"  🌲 보유 나무 : {woodCount} 개");
                sb.AppendLine($"  🪨 보유 바위 : {stoneCount} 개");
                sb.AppendLine($"  💰 보유 골드 : {gold:N0} G");
                sb.AppendLine("----------------------------------------------------------");
                sb.AppendLine("  🐟 [낚은 물고기 도감 & 보유 수량]");
                foreach (var fish in fishInventory)
                {
                    sb.AppendLine($"   - {fish.Key,-22} : {fish.Value} 마리");
                }
                for (int i = 0; i < 4; i++) sb.AppendLine("                                                          ");
                sb.AppendLine("----------------------------------------------------------");
                sb.AppendLine("  ※ [I] 키를 다시 누르면 필드로 돌아갑니다.               ");
            }
            else
            {
                // 필드 화면 출력
                for (int y = 0; y < HEIGHT; y++)
                {
                    sb.Append("  ");
                    for (int x = 0; x < WIDTH; x++)
                    {
                        if (x == playerX && y == playerY)
                        {
                            // 플레이어 방향 표시
                            char pChar = dirY == -1 ? '▲' : dirY == 1 ? '▼' : dirX == -1 ? '◄' : '►';
                            sb.Append(pChar);
                        }
                        else if (x == bobberX && y == bobberY)
                        {
                            // 낚시 찌 (입질 오면 '!'로 깜빡임)
                            sb.Append(fishState == FishingState.Biting ? '!' : 'o');
                        }
                        else
                        {
                            sb.Append(map[y, x]);
                        }
                    }
                    // 우측 범례 안내
                    if (y == 1) sb.Append("  [범례]");
                    else if (y == 3) sb.Append("  ►▲▼◄ : 플레이어");
                    else if (y == 4) sb.Append("  T→t→; : 나무(갈림)");
                    else if (y == 5) sb.Append("  O→o→* : 바위(갈림)");
                    else if (y == 6) sb.Append("  ~     : 낚시터");
                    else if (y == 8) sb.Append("  [조작법]");
                    else if (y == 9) sb.Append("  WASD  : 이동");
                    else if (y == 10) sb.Append("  좌클릭: 채집/낚기");
                    else if (y == 11) sb.Append("  우클릭: 찌 던지기");
                    else if (y == 12) sb.Append("  I     : 인벤토리");
                    sb.AppendLine("          ");
                }
            }
            sb.AppendLine("----------------------------------------------------------");
            sb.AppendLine($" 알림: {statusMessage,-48}");
            sb.AppendLine("==========================================================");
            Console.Write(sb.ToString());
        }
    }
}