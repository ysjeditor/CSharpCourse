//using System;
//using System.Diagnostics;
//using System.Runtime.InteropServices;
//using System.Text;
//using System.Threading;

//// ==========================================
//// 1. 게임 루프 및 전체 흐름 관리 클래스
//// ==========================================
//public class Game
//{
//    private bool _isRunning = true;
//    private bool _isPaused = false;

//    private readonly InputManager _input;
//    private readonly ApartmentMap _map;
//    private readonly Player _player;
//    private readonly Weapon _ak47;
//    private readonly Renderer3D _renderer;

//    public Game()
//    {
//        Console.OutputEncoding = Encoding.UTF8;
//        Console.CursorVisible = false;

//        // 콘솔 빠른 편집 모드 해제 및 ANSI 컬러 모드 활성화
//        ConsoleHelper.InitializeConsole();
//        try
//        {
//            if (OperatingSystem.IsWindows())
//            {
//                Console.SetWindowSize(102, 32);
//                Console.SetBufferSize(102, 32);
//            }
//        }
//        catch { }

//        Console.Clear();

//        _input = new InputManager();
//        _map = new ApartmentMap();
//        _player = new Player(6.5, 9.5); // 탁 트인 거실 중앙 시작
//        _ak47 = new Weapon("AK-47", 30);
//        _renderer = new Renderer3D(100, 30);
//    }

//    public static void Run()
//    {
//        Game game = new Game();
//        game.Loop();
//    }

//    // (1), (2) 게임 루프: 입력 -> 갱신 -> 렌더링
//    private void Loop()
//    {
//        Stopwatch stopwatch = Stopwatch.StartNew();
//        double lastTime = stopwatch.Elapsed.TotalSeconds;

//        while (_isRunning)
//        {
//            // (4) Delta Time 계산
//            double currentTime = stopwatch.Elapsed.TotalSeconds;
//            float deltaTime = (float)(currentTime - lastTime);
//            lastTime = currentTime;

//            // 1. 입력 (Input)
//            ProcessInput();

//            // 2. 갱신 (Update)
//            if (!_isPaused)
//            {
//                Update(deltaTime);
//            }

//            // 3. 렌더링 (Render)
//            Render();

//            // 약 60 FPS 유지
//            Thread.Sleep(15);
//        }

//        Console.Write("\x1b[0m");
//        Console.Clear();
//        Console.CursorVisible = true;
//        Console.WriteLine("게임을 종료했습니다.");
//    }

//    private void ProcessInput()
//    {
//        _input.Update(!_isPaused);

//        // ESC 일시정지 / 종료 탭 토글
//        if (_input.IsKeyPressed(ConsoleKey.Escape))
//        {
//            _isPaused = !_isPaused;
//            if (_isPaused)
//            {
//                HandlePauseMenu();
//            }
//        }

//        if (_isPaused) return;

//        // WASD 이동
//        double moveForward = 0;
//        double moveRight = 0;
//        double keyRotate = 0;

//        if (_input.IsKeyDown(ConsoleKey.W)) moveForward += 1;
//        if (_input.IsKeyDown(ConsoleKey.S)) moveForward -= 1;
//        if (_input.IsKeyDown(ConsoleKey.D)) moveRight += 1;
//        if (_input.IsKeyDown(ConsoleKey.A)) moveRight -= 1;

//        // 보조 키보드 회전 (Q/E 또는 좌우 방향키) + 실시간 마우스 좌우 회전
//        if (_input.IsKeyDown(ConsoleKey.LeftArrow) || _input.IsKeyDown(ConsoleKey.Q)) keyRotate -= 1;
//        if (_input.IsKeyDown(ConsoleKey.RightArrow) || _input.IsKeyDown(ConsoleKey.E)) keyRotate += 1;

//        double mouseDeltaX = _input.MouseDeltaX;

//        _player.SetMoveInput(moveForward, moveRight, keyRotate, mouseDeltaX);

//        // Space 점프
//        if (_input.IsKeyPressed(ConsoleKey.Spacebar))
//        {
//            _player.Jump();
//        }

//        // 좌클릭 연사 (꾹 누르고 있어도 계속 발사)
//        if (_input.IsMouseLeftDown())
//        {
//            _ak47.Fire();
//        }

//        // R 장전 (한 발 이상 쏴야 장전 가능)
//        if (_input.IsKeyPressed(ConsoleKey.R))
//        {
//            _ak47.Reload();
//        }
//    }

//    private void Update(float deltaTime)
//    {
//        _player.Update(deltaTime, _map);
//        _ak47.Update(deltaTime);
//    }

//    private void Render()
//    {
//        if (_isPaused) return;
//        _renderer.RenderFrame(_player, _map, _ak47);
//    }

//    // (4) ESC 메뉴: "종료" 입력 시 종료
//    private void HandlePauseMenu()
//    {
//        Console.Write("\x1b[0m");
//        Console.SetCursorPosition(0, 10);
//        Console.ForegroundColor = ConsoleColor.Yellow;
//        Console.WriteLine("==========================================");
//        Console.WriteLine("   [ 일시 정지 / PAUSE ]                  ");
//        Console.WriteLine("   게임을 끝내려면 '종료' 를 입력하세요.  ");
//        Console.WriteLine("   계속하려면 아무 글자나 Enter를 누르세요.");
//        Console.WriteLine("==========================================");
//        Console.ResetColor();
//        Console.CursorVisible = true;

//        Console.Write("입력 > ");
//        string? command = Console.ReadLine();

//        if (command != null && command.Trim() == "종료")
//        {
//            _isRunning = false;
//        }
//        else
//        {
//            _isPaused = false;
//            Console.CursorVisible = false;
//            ConsoleHelper.InitializeConsole();
//            Console.Clear();
//        }
//    }
//}

//// ==========================================
//// 콘솔 빠른 편집 모드 해제 & ANSI 가상 터미널 활성화 유틸리티
//// ==========================================
//public static class ConsoleHelper
//{
//    private const int STD_INPUT_HANDLE = -10;
//    private const int STD_OUTPUT_HANDLE = -11;
//    private const uint ENABLE_QUICK_EDIT_MODE = 0x0040;
//    private const uint ENABLE_EXTENDED_FLAGS = 0x0080;
//    private const uint ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004;

//    [DllImport("kernel32.dll", SetLastError = true)]
//    private static extern IntPtr GetStdHandle(int nStdHandle);

//    [DllImport("kernel32.dll")]
//    private static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);

//    [DllImport("kernel32.dll")]
//    private static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);

//    public static void InitializeConsole()
//    {
//        try
//        {
//            // 입력 핸들: 빠른 편집 모드 비활성화
//            IntPtr inHandle = GetStdHandle(STD_INPUT_HANDLE);
//            if (GetConsoleMode(inHandle, out uint inMode))
//            {
//                inMode &= ~ENABLE_QUICK_EDIT_MODE;
//                inMode |= ENABLE_EXTENDED_FLAGS;
//                SetConsoleMode(inHandle, inMode);
//            }

//            // 출력 핸들: ANSI 색상 시퀀스 활성화
//            IntPtr outHandle = GetStdHandle(STD_OUTPUT_HANDLE);
//            if (GetConsoleMode(outHandle, out uint outMode))
//            {
//                outMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
//                SetConsoleMode(outHandle, outMode);
//            }
//        }
//        catch { }
//    }
//}

//// ==========================================
//// 2. 실시간 키보드 & 마우스 감지기 (Windows API)
//// ==========================================
//public class InputManager
//{
//    [StructLayout(LayoutKind.Sequential)]
//    private struct POINT
//    {
//        public int X;
//        public int Y;
//    }

//    [StructLayout(LayoutKind.Sequential)]
//    private struct RECT
//    {
//        public int Left;
//        public int Top;
//        public int Right;
//        public int Bottom;
//    }

//    [DllImport("user32.dll")]
//    private static extern short GetAsyncKeyState(int vKey);

//    [DllImport("user32.dll")]
//    private static extern bool GetCursorPos(out POINT lpPoint);

//    [DllImport("user32.dll")]
//    private static extern bool SetCursorPos(int X, int Y);

//    [DllImport("user32.dll")]
//    private static extern IntPtr GetForegroundWindow();

//    [DllImport("user32.dll")]
//    private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

//    private const int KeyCount = 256;
//    private const int VK_LBUTTON = 0x01;

//    private readonly bool[] _prevKeyState = new bool[KeyCount];
//    private readonly bool[] _currKeyState = new bool[KeyCount];

//    public double MouseDeltaX { get; private set; }
//    private bool _firstMouseFrame = true;

//    public void Update(bool captureMouse)
//    {
//        Array.Copy(_currKeyState, _prevKeyState, KeyCount);
//        for (int i = 0; i < KeyCount; i++)
//        {
//            _currKeyState[i] = (GetAsyncKeyState(i) & 0x8000) != 0;
//        }

//        MouseDeltaX = 0;
//        if (!captureMouse)
//        {
//            _firstMouseFrame = true;
//            return;
//        }

//        IntPtr hwnd = GetForegroundWindow();
//        if (hwnd != IntPtr.Zero && GetWindowRect(hwnd, out RECT rect))
//        {
//            int centerX = (rect.Left + rect.Right) / 2;
//            int centerY = (rect.Top + rect.Bottom) / 2;

//            if (GetCursorPos(out POINT currentPos))
//            {
//                if (_firstMouseFrame)
//                {
//                    SetCursorPos(centerX, centerY);
//                    _firstMouseFrame = false;
//                }
//                else
//                {
//                    MouseDeltaX = currentPos.X - centerX;
//                    SetCursorPos(centerX, centerY);
//                }
//            }
//        }
//    }

//    public bool IsKeyDown(ConsoleKey key) => _currKeyState[(int)key];
//    public bool IsKeyPressed(ConsoleKey key) => _currKeyState[(int)key] && !_prevKeyState[(int)key];
//    public bool IsMouseLeftDown() => _currKeyState[VK_LBUTTON];
//}

//// ==========================================
//// 3. 한국식 아파트 구조 맵 (2D 그리드 데이터)
//// ==========================================
//public class ApartmentMap
//{
//    // 1: 외벽/콘크리트벽, 3: 베란다 통유리창, 0: 이동 가능 공간
//    private readonly int[,] _grid = new int[,]
//    {
//        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 },
//        { 1,3,3,3,3,3,1,3,3,3,3,3,3,3,3,1 }, // 베란다 (창문 3)
//        { 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 },
//        { 1,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1 }, // 거실-베란다 샤시 통로
//        { 1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1 }, // 좌: 안방 / 중: 거실 / 우: 주방
//        { 1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1 },
//        { 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 }, // 안방 문 / 주방 입구
//        { 1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1 },
//        { 1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1 }, // 좌: 화장실 / 우: 작은방 입구
//        { 1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1 }, // 화장실 문
//        { 1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,1 },
//        { 1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1 }, // 현관 중문
//        { 1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1 }, // 현관 입구
//        { 1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1 },
//        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 },
//        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 }
//    };

//    public int Width => _grid.GetLength(1);
//    public int Height => _grid.GetLength(0);

//    public int GetTile(int x, int y)
//    {
//        if (x < 0 || x >= Width || y < 0 || y >= Height) return 1;
//        return _grid[y, x];
//    }

//    public bool IsWalkable(double x, double y)
//    {
//        int tile = GetTile((int)x, (int)y);
//        return tile == 0;
//    }

//    public string GetZoneName(double x, double y)
//    {
//        if (y >= 11 && x <= 4) return "ENTRANCE (Hyungwan)";
//        if (y >= 8 && y <= 10 && x <= 4) return "BATHROOM (Hwajangsil)";
//        if (y >= 4 && y <= 6 && x <= 5) return "MASTER ROOM (Anbang)";
//        if (y >= 8 && y <= 10 && x >= 12) return "SMALL ROOM (Jageunbang)";
//        if (y >= 4 && y <= 6 && x >= 12) return "KITCHEN (Jubang)";
//        if (y <= 2) return "VERANDA (Beranda)";
//        return "LIVING ROOM (Geosil)";
//    }
//}

//// ==========================================
//// 4. 플레이어 상태 및 3D 물리(이동, 시야, 점프)
//// ==========================================
//public class Player
//{
//    public double X { get; private set; }
//    public double Y { get; private set; }
//    public double Angle { get; private set; } = -Math.PI / 2;
//    public double ZHeight { get; private set; } = 0;

//    private double _verticalVelocity = 0;
//    private bool _isGrounded = true;

//    private double _inputForward;
//    private double _inputRight;
//    private double _inputKeyRotate;
//    private double _inputMouseDeltaX;

//    private const double MoveSpeed = 4.5;
//    private const double KeyRotateSpeed = 2.6;
//    private const double MouseSensitivity = 0.0045;
//    private const double Gravity = 18.0;
//    private const double JumpForce = 6.5;

//    public Player(double startX, double startY)
//    {
//        X = startX;
//        Y = startY;
//    }

//    public void SetMoveInput(double forward, double right, double keyRotate, double mouseDeltaX)
//    {
//        _inputForward = forward;
//        _inputRight = right;
//        _inputKeyRotate = keyRotate;
//        _inputMouseDeltaX = mouseDeltaX;
//    }

//    public void Jump()
//    {
//        if (_isGrounded)
//        {
//            _verticalVelocity = JumpForce;
//            _isGrounded = false;
//        }
//    }

//    public void Update(float deltaTime, ApartmentMap map)
//    {
//        Angle += (_inputKeyRotate * KeyRotateSpeed * deltaTime) + (_inputMouseDeltaX * MouseSensitivity);

//        double dirX = Math.Cos(Angle);
//        double dirY = Math.Sin(Angle);
//        double rightX = -dirY;
//        double rightY = dirX;

//        double moveX = (dirX * _inputForward + rightX * _inputRight) * MoveSpeed * deltaTime;
//        double moveY = (dirY * _inputForward + rightY * _inputRight) * MoveSpeed * deltaTime;

//        if (map.IsWalkable(X + moveX, Y)) X += moveX;
//        if (map.IsWalkable(X, Y + moveY)) Y += moveY;

//        if (!_isGrounded)
//        {
//            ZHeight += _verticalVelocity * deltaTime;
//            _verticalVelocity -= Gravity * deltaTime;

//            if (ZHeight <= 0)
//            {
//                ZHeight = 0;
//                _verticalVelocity = 0;
//                _isGrounded = true;
//            }
//        }
//    }
//}

//// ==========================================
//// 5. AK-47 무기 시스템 (발사, 화염, 장전, 사운드)
//// ==========================================
//public class Weapon
//{
//    public string Name { get; }
//    public int MaxAmmo { get; }
//    public int CurrentAmmo { get; private set; }
//    public bool IsFiringFlash { get; private set; }
//    public bool IsReloading { get; private set; }

//    private float _fireCooldown = 0f;
//    private float _flashTimer = 0f;
//    private float _reloadTimer = 0f;

//    private const float FireRate = 0.12f;
//    private const float ReloadDuration = 1.2f;

//    public Weapon(string name, int maxAmmo)
//    {
//        Name = name;
//        MaxAmmo = maxAmmo;
//        CurrentAmmo = maxAmmo;
//    }

//    public void Fire()
//    {
//        if (IsReloading || _fireCooldown > 0f || CurrentAmmo <= 0) return;

//        CurrentAmmo--;
//        _fireCooldown = FireRate;
//        IsFiringFlash = true;
//        _flashTimer = 0.08f;

//        ThreadPool.QueueUserWorkItem(_ =>
//        {
//            try { Console.Beep(180, 45); } catch { }
//        });
//    }

//    public void Reload()
//    {
//        if (IsReloading || CurrentAmmo >= MaxAmmo) return;

//        IsReloading = true;
//        _reloadTimer = ReloadDuration;

//        ThreadPool.QueueUserWorkItem(_ =>
//        {
//            try
//            {
//                Console.Beep(400, 60);
//                Thread.Sleep(80);
//                Console.Beep(600, 80);
//            }
//            catch { }
//        });
//    }

//    public void Update(float deltaTime)
//    {
//        if (_fireCooldown > 0f) _fireCooldown -= deltaTime;

//        if (_flashTimer > 0f)
//        {
//            _flashTimer -= deltaTime;
//            if (_flashTimer <= 0f) IsFiringFlash = false;
//        }

//        if (IsReloading)
//        {
//            _reloadTimer -= deltaTime;
//            if (_reloadTimer <= 0f)
//            {
//                IsReloading = false;
//                CurrentAmmo = MaxAmmo;
//            }
//        }
//    }
//}

//// ==========================================
//// 6. 2D -> 3D 레이캐스팅 렌더러 & 3D 원근 UI (어지러움 방지 명암 고정형)
//// ==========================================
//public class Renderer3D
//{
//    private readonly int _width;
//    private readonly int _height;
//    private readonly char[,] _charBuffer;
//    private readonly string[,] _colorBuffer;
//    private const double Fov = Math.PI / 3.0;

//    // ANSI 컬러 코드 상수
//    private const string ColReset = "\x1b[0m";
//    private const string ColWallBright = "\x1b[97m";   // 근거리 벽: 밝은 흰색
//    private const string ColWallMid = "\x1b[37m";      // 중거리 벽: 일반 회색
//    private const string ColWallDark = "\x1b[90m";     // 원거리 벽: 어두운 회색
//    private const string ColWallDeep = "\x1b[30;1m";   // 최원거리 벽: 짙은 회색
//    private const string ColWindow = "\x1b[96m";       // 베란다 창문: 하늘색
//    private const string ColEdge = "\x1b[33m";         // 벽 모서리 경계선: 은은한 노란색
//    private const string ColCeiling = "\x1b[90m";      // 천장
//    private const string ColFloor = "\x1b[37m";        // 마룻바닥
//    private const string ColUI = "\x1b[92m";           // 3D 홀로그램 UI: 연두색
//    private const string ColGun = "\x1b[33m";          // AK-47 총기: 황동/우드톤
//    private const string ColFlash = "\x1b[91;1m";      // 총구 화염: 밝은 적황색

//    public Renderer3D(int width, int height)
//    {
//        _width = width;
//        _height = height;
//        _charBuffer = new char[height, width];
//        _colorBuffer = new string[height, width];
//    }

//    public void RenderFrame(Player player, ApartmentMap map, Weapon weapon)
//    {
//        int horizonOffset = (int)(player.ZHeight * 8);
//        int prevHitX = -1;
//        int prevHitY = -1;

//        for (int x = 0; x < _width; x++)
//        {
//            double rayAngle = (player.Angle - Fov / 2.0) + ((double)x / _width) * Fov;
//            double eyeX = Math.Cos(rayAngle);
//            double eyeY = Math.Sin(rayAngle);

//            double distanceToWall = 0;
//            bool hitWall = false;
//            int hitTileType = 1;
//            int hitX = 0, hitY = 0;

//            while (!hitWall && distanceToWall < 16.0)
//            {
//                distanceToWall += 0.04;
//                hitX = (int)(player.X + eyeX * distanceToWall);
//                hitY = (int)(player.Y + eyeY * distanceToWall);

//                int tile = map.GetTile(hitX, hitY);
//                if (tile > 0)
//                {
//                    hitWall = true;
//                    hitTileType = tile;
//                }
//            }

//            bool isCornerEdge = (hitX != prevHitX || hitY != prevHitY);
//            prevHitX = hitX;
//            prevHitY = hitY;

//            double correctedDist = distanceToWall * Math.Cos(rayAngle - player.Angle);
//            if (correctedDist < 0.1) correctedDist = 0.1;

//            int ceiling = (int)(_height / 2.0 - _height / correctedDist) + horizonOffset;
//            int floor = _height - ceiling + (horizonOffset * 2);

//            // [어지러움 해결] 거리에 따라 문자를 바꾸지 않고 '#' 하나로 고정하고 색상(밝기)만 변경!
//            char wallChar = isCornerEdge ? '|' : (hitTileType == 3 ? '/' : '#');
//            string wallColor = isCornerEdge ? ColEdge : GetWallShadeColor(correctedDist, hitTileType);

//            for (int y = 0; y < _height; y++)
//            {
//                if (y <= ceiling)
//                {
//                    _charBuffer[y, x] = (y % 4 == 0 && x % 10 == 0) ? '+' : ' ';
//                    _colorBuffer[y, x] = ColCeiling;
//                }
//                else if (y > ceiling && y <= floor)
//                {
//                    if (y == ceiling + 1 || y == floor)
//                    {
//                        _charBuffer[y, x] = '-';
//                        _colorBuffer[y, x] = ColEdge;
//                    }
//                    else
//                    {
//                        _charBuffer[y, x] = wallChar;
//                        _colorBuffer[y, x] = wallColor;
//                    }
//                }
//                else
//                {
//                    double b = 1.0 - (((double)y - _height / 2.0 - horizonOffset) / (_height / 2.0));
//                    if (b < 0.35) _charBuffer[y, x] = '-';
//                    else if (b < 0.7) _charBuffer[y, x] = '.';
//                    else _charBuffer[y, x] = ' ';
//                    _colorBuffer[y, x] = ColFloor;
//                }
//            }
//        }

//        // 중앙 조준점
//        int cx = _width / 2;
//        int cy = _height / 2;
//        if (weapon.IsFiringFlash)
//            DrawText(cx - 2, cy, "< + >", ColFlash, overwriteSpace: false);
//        else
//            DrawText(cx - 1, cy, "-+-", ColUI, overwriteSpace: false);

//        // 3D 원근 투영 UI
//        Draw3DPerspectiveUI(player, map, weapon);

//        // 1인칭 AK-47과 손, 총구 화염
//        DrawFirstPersonAK47(weapon);

//        // 색상 변경이 일어날 때만 ANSI 코드를 삽입해 렌더링 속도 최적화
//        StringBuilder sb = new StringBuilder(_width * _height * 2);
//        string currentColor = "";

//        for (int y = 0; y < _height; y++)
//        {
//            for (int x = 0; x < _width; x++)
//            {
//                string cellColor = _colorBuffer[y, x];
//                if (cellColor != currentColor)
//                {
//                    sb.Append(cellColor);
//                    currentColor = cellColor;
//                }
//                sb.Append(_charBuffer[y, x]);
//            }
//            sb.AppendLine();
//        }
//        sb.Append(ColReset);

//        Console.SetCursorPosition(0, 0);
//        Console.Write(sb.ToString());
//    }

//    // 거리별 색상 명암 반환 (문양 교체 없이 눈이 편안한 3D 거리감 제공)
//    private string GetWallShadeColor(double distance, int tileType)
//    {
//        if (tileType == 3) return ColWindow; // 베란다 창문

//        if (distance <= 2.5) return ColWallBright;
//        if (distance <= 5.0) return ColWallMid;
//        if (distance <= 8.5) return ColWallDark;
//        return ColWallDeep;
//    }

//    private void Draw3DPerspectiveUI(Player player, ApartmentMap map, Weapon weapon)
//    {
//        string zone = map.GetZoneName(player.X, player.Y);
//        DrawText(2, 1,  @"+--------------------------------+", ColUI, overwriteSpace: true);
//        DrawText(3, 2, $@"| LOC : {zone,-24} |", ColUI, overwriteSpace: true);
//        DrawText(4, 3,  @"| [WASD]Move [Mouse]Look [Spc]Jmp| ", ColUI, overwriteSpace: true);
//        DrawText(5, 4,  @"+--------------------------------+  ", ColUI, overwriteSpace: true);
//        DrawText(6, 5,  @" \__________________________________", ColUI, overwriteSpace: false);

//        int rx = _width - 35;
//        string status = weapon.IsReloading ? "RELOADING..." : (weapon.CurrentAmmo == 0 ? "PRESS [R]!" : "READY");
//        DrawText(rx, 1,      @"+----------------------------+", ColUI, overwriteSpace: true);
//        DrawText(rx - 1, 2, $@"/| WEAPON : {weapon.Name,-16} |", ColUI, overwriteSpace: true);
//        DrawText(rx - 2, 3, $@"/ | AMMO   : {weapon.CurrentAmmo,2} / {weapon.MaxAmmo} (INF)   |", ColUI, overwriteSpace: true);
//        DrawText(rx - 3, 4, $@"/  | STATUS : {status,-16} |", ColUI, overwriteSpace: true);
//        DrawText(rx - 4, 5,  @"   +----------------------------+", ColUI, overwriteSpace: true);
//    }

//    private void DrawFirstPersonAK47(Weapon weapon)
//    {
//        int gunX = _width / 2 + 4;
//        int gunY = _height - 10;

//        if (weapon.IsFiringFlash)
//        {
//            gunY += 1;
//            gunX += 1;
//        }
//        else if (weapon.IsReloading)
//        {
//            gunY += 3;
//        }

//        if (weapon.IsFiringFlash)
//        {
//            DrawText(gunX - 7, gunY - 3, @"    \  |  /    ", ColFlash, overwriteSpace: false);
//            DrawText(gunX - 9, gunY - 2, @"  --== ( * ) ==--", ColFlash, overwriteSpace: false);
//            DrawText(gunX - 7, gunY - 1, @"    /  |  \    ", ColFlash, overwriteSpace: false);
//        }

//        string[] akModel =
//        {
//            @"       /===[_]==\           ",
//            @"      /==========\          ",
//            @"     /[AK-47]=====\____     ",
//            @"    ( (L-HAND) )===|____|   ",
//            @"     \________/   /  /      ",
//            @"        |  |     /  /       ",
//            @"       (WRIST)  (R-HAND)    ",
//            @"      /      \  /      \    "
//        };

//        for (int i = 0; i < akModel.Length; i++)
//        {
//            DrawText(gunX, gunY + i, akModel[i], ColGun, overwriteSpace: false);
//        }
//    }

//    private void DrawText(int startX, int startY, string text, string color, bool overwriteSpace)
//    {
//        if (startY < 0 || startY >= _height) return;
//        for (int i = 0; i < text.Length; i++)
//        {
//            int px = startX + i;
//            if (px >= 0 && px < _width)
//            {
//                if (overwriteSpace || text[i] != ' ')
//                {
//                    _charBuffer[startY, px] = text[i];
//                    _colorBuffer[startY, px] = color;
//                }
//            }
//        }
//    }
//}
