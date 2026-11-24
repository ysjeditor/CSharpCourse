using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

// ==========================================
// 1. 게임 루프 및 전체 흐름 관리 클래스
// ==========================================
public class Game
{
    private bool _isRunning = true;
    private bool _isPaused = false;

    private readonly InputManager _input;
    private readonly ApartmentMap _map;
    private readonly Player _player;
    private readonly Weapon _ak47;
    private readonly Renderer3D _renderer;

    public Game()
    {
        Console.OutputEncoding = Encoding.UTF8;
        Console.CursorVisible = false;

        ConsoleHelper.DisableQuickEdit();
        try
        {
            if (OperatingSystem.IsWindows())
            {
                Console.SetWindowSize(102, 32);
                Console.SetBufferSize(102, 32);
            }
        }
        catch { }

        Console.Clear();

        _input = new InputManager();
        _map = new ApartmentMap();
        _player = new Player(6.5, 9.5);
        _ak47 = new Weapon("AK-47", 30);
        _renderer = new Renderer3D(100, 30);
    }

    public static void Run()
    {
        Game game = new Game();
        game.Loop();
    }

    private void Loop()
    {
        Stopwatch stopwatch = Stopwatch.StartNew();
        double lastTime = stopwatch.Elapsed.TotalSeconds;

        while (_isRunning)
        {
            double currentTime = stopwatch.Elapsed.TotalSeconds;
            float deltaTime = (float)(currentTime - lastTime);
            lastTime = currentTime;

            ProcessInput();

            if (!_isPaused)
            {
                Update(deltaTime);
            }

            Render();

            Thread.Sleep(15);
        }

        Console.Clear();
        Console.CursorVisible = true;
        Console.WriteLine("게임을 종료했습니다.");
    }

    private void ProcessInput()
    {
        _input.Update(!_isPaused);

        if (_input.IsKeyPressed(ConsoleKey.Escape))
        {
            _isPaused = !_isPaused;
            if (_isPaused)
            {
                HandlePauseMenu();
            }
        }

        if (_isPaused) return;

        double moveForward = 0;
        double moveRight = 0;
        double keyRotate = 0;

        if (_input.IsKeyDown(ConsoleKey.W)) moveForward += 1;
        if (_input.IsKeyDown(ConsoleKey.S)) moveForward -= 1;
        if (_input.IsKeyDown(ConsoleKey.D)) moveRight += 1;
        if (_input.IsKeyDown(ConsoleKey.A)) moveRight -= 1;

        if (_input.IsKeyDown(ConsoleKey.LeftArrow) || _input.IsKeyDown(ConsoleKey.Q)) keyRotate -= 1;
        if (_input.IsKeyDown(ConsoleKey.RightArrow) || _input.IsKeyDown(ConsoleKey.E)) keyRotate += 1;

        double mouseDeltaX = _input.MouseDeltaX;

        _player.SetMoveInput(moveForward, moveRight, keyRotate, mouseDeltaX);

        if (_input.IsKeyPressed(ConsoleKey.Spacebar))
        {
            _player.Jump();
        }

        if (_input.IsMouseLeftDown())
        {
            _ak47.Fire();
        }

        if (_input.IsKeyPressed(ConsoleKey.R))
        {
            _ak47.Reload();
        }
    }

    private void Update(float deltaTime)
    {
        _player.Update(deltaTime, _map);
        _ak47.Update(deltaTime);
    }

    private void Render()
    {
        if (_isPaused) return;
        _renderer.RenderFrame(_player, _map, _ak47);
    }

    private void HandlePauseMenu()
    {
        Console.SetCursorPosition(0, 10);
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine("==========================================");
        Console.WriteLine("   [ 일시 정지 / PAUSE ]                  ");
        Console.WriteLine("   게임을 끝내려면 '종료' 를 입력하세요.  ");
        Console.WriteLine("   계속하려면 아무 글자나 Enter를 누르세요.");
        Console.WriteLine("==========================================");
        Console.ResetColor();
        Console.CursorVisible = true;

        Console.Write("입력 > ");
        string? command = Console.ReadLine();

        if (command != null && command.Trim() == "종료")
        {
            _isRunning = false;
        }
        else
        {
            _isPaused = false;
            Console.CursorVisible = false;
            ConsoleHelper.DisableQuickEdit();
            Console.Clear();
        }
    }
}

// ==========================================
// 콘솔 빠른 편집 모드(클릭 멈춤) 방지 유틸리티
// ==========================================
public static class ConsoleHelper
{
    private const int STD_INPUT_HANDLE = -10;
    private const uint ENABLE_QUICK_EDIT_MODE = 0x0040;
    private const uint ENABLE_EXTENDED_FLAGS = 0x0080;

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr GetStdHandle(int nStdHandle);

    [DllImport("kernel32.dll")]
    private static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);

    [DllImport("kernel32.dll")]
    private static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);

    public static void DisableQuickEdit()
    {
        try
        {
            IntPtr consoleHandle = GetStdHandle(STD_INPUT_HANDLE);
            if (GetConsoleMode(consoleHandle, out uint consoleMode))
            {
                consoleMode &= ~ENABLE_QUICK_EDIT_MODE;
                consoleMode |= ENABLE_EXTENDED_FLAGS;
                SetConsoleMode(consoleHandle, consoleMode);
            }
        }
        catch { }
    }
}

// ==========================================
// 2. 실시간 키보드 & 마우스 감지기 (Windows API)
// ==========================================
public class InputManager
{
    [StructLayout(LayoutKind.Sequential)]
    private struct POINT
    {
        public int X;
        public int Y;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [DllImport("user32.dll")]
    private static extern short GetAsyncKeyState(int vKey);

    [DllImport("user32.dll")]
    private static extern bool GetCursorPos(out POINT lpPoint);

    [DllImport("user32.dll")]
    private static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    private static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

    private const int KeyCount = 256;
    private const int VK_LBUTTON = 0x01;

    private readonly bool[] _prevKeyState = new bool[KeyCount];
    private readonly bool[] _currKeyState = new bool[KeyCount];

    public double MouseDeltaX { get; private set; }
    private bool _firstMouseFrame = true;

    public void Update(bool captureMouse)
    {
        Array.Copy(_currKeyState, _prevKeyState, KeyCount);
        for (int i = 0; i < KeyCount; i++)
        {
            _currKeyState[i] = (GetAsyncKeyState(i) & 0x8000) != 0;
        }

        MouseDeltaX = 0;
        if (!captureMouse)
        {
            _firstMouseFrame = true;
            return;
        }

        IntPtr hwnd = GetForegroundWindow();
        if (hwnd != IntPtr.Zero && GetWindowRect(hwnd, out RECT rect))
        {
            int centerX = (rect.Left + rect.Right) / 2;
            int centerY = (rect.Top + rect.Bottom) / 2;

            if (GetCursorPos(out POINT currentPos))
            {
                if (_firstMouseFrame)
                {
                    SetCursorPos(centerX, centerY);
                    _firstMouseFrame = false;
                }
                else
                {
                    MouseDeltaX = currentPos.X - centerX;
                    SetCursorPos(centerX, centerY);
                }
            }
        }
    }

    public bool IsKeyDown(ConsoleKey key) => _currKeyState[(int)key];
    public bool IsKeyPressed(ConsoleKey key) => _currKeyState[(int)key] && !_prevKeyState[(int)key];
    public bool IsMouseLeftDown() => _currKeyState[VK_LBUTTON];
}

// ==========================================
// 3. 한국식 아파트 구조 맵 (2D 그리드 데이터)
// ==========================================
public class ApartmentMap
{
    private readonly int[,] _grid = new int[,]
    {
        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 },
        { 1,3,3,3,3,3,1,3,3,3,3,3,3,3,3,1 },
        { 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 },
        { 1,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1 },
        { 1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1 },
        { 1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1 },
        { 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 },
        { 1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1 },
        { 1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1 },
        { 1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1 },
        { 1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,1 },
        { 1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1 },
        { 1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1 },
        { 1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1 },
        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 },
        { 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 }
    };

    public int Width => _grid.GetLength(1);
    public int Height => _grid.GetLength(0);

    public int GetTile(int x, int y)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) return 1;
        return _grid[y, x];
    }

    public bool IsWalkable(double x, double y)
    {
        int tile = GetTile((int)x, (int)y);
        return tile == 0;
    }

    public string GetZoneName(double x, double y)
    {
        if (y >= 11 && x <= 4) return "ENTRANCE (Hyungwan)";
        if (y >= 8 && y <= 10 && x <= 4) return "BATHROOM (Hwajangsil)";
        if (y >= 4 && y <= 6 && x <= 5) return "MASTER ROOM (Anbang)";
        if (y >= 8 && y <= 10 && x >= 12) return "SMALL ROOM (Jageunbang)";
        if (y >= 4 && y <= 6 && x >= 12) return "KITCHEN (Jubang)";
        if (y <= 2) return "VERANDA (Beranda)";
        return "LIVING ROOM (Geosil)";
    }
}

// ==========================================
// 4. 플레이어 상태 및 3D 물리(이동, 시야, 점프)
// ==========================================
public class Player
{
    public double X { get; private set; }
    public double Y { get; private set; }
    public double Angle { get; private set; } = -Math.PI / 2;
    public double ZHeight { get; private set; } = 0;

    private double _verticalVelocity = 0;
    private bool _isGrounded = true;

    private double _inputForward;
    private double _inputRight;
    private double _inputKeyRotate;
    private double _inputMouseDeltaX;

    private const double MoveSpeed = 4.5;
    private const double KeyRotateSpeed = 2.6;
    private const double MouseSensitivity = 0.0045;
    private const double Gravity = 18.0;
    private const double JumpForce = 6.5;

    public Player(double startX, double startY)
    {
        X = startX;
        Y = startY;
    }

    public void SetMoveInput(double forward, double right, double keyRotate, double mouseDeltaX)
    {
        _inputForward = forward;
        _inputRight = right;
        _inputKeyRotate = keyRotate;
        _inputMouseDeltaX = mouseDeltaX;
    }

    public void Jump()
    {
        if (_isGrounded)
        {
            _verticalVelocity = JumpForce;
            _isGrounded = false;
        }
    }

    public void Update(float deltaTime, ApartmentMap map)
    {
        Angle += (_inputKeyRotate * KeyRotateSpeed * deltaTime) + (_inputMouseDeltaX * MouseSensitivity);

        double dirX = Math.Cos(Angle);
        double dirY = Math.Sin(Angle);
        double rightX = -dirY;
        double rightY = dirX;

        double moveX = (dirX * _inputForward + rightX * _inputRight) * MoveSpeed * deltaTime;
        double moveY = (dirY * _inputForward + rightY * _inputRight) * MoveSpeed * deltaTime;

        if (map.IsWalkable(X + moveX, Y)) X += moveX;
        if (map.IsWalkable(X, Y + moveY)) Y += moveY;

        if (!_isGrounded)
        {
            ZHeight += _verticalVelocity * deltaTime;
            _verticalVelocity -= Gravity * deltaTime;

            if (ZHeight <= 0)
            {
                ZHeight = 0;
                _verticalVelocity = 0;
                _isGrounded = true;
            }
        }
    }
}

// ==========================================
// 5. AK-47 무기 시스템 (발사, 화염, 장전, 사운드)
// ==========================================
public class Weapon
{
    public string Name { get; }
    public int MaxAmmo { get; }
    public int CurrentAmmo { get; private set; }
    public bool IsFiringFlash { get; private set; }
    public bool IsReloading { get; private set; }

    private float _fireCooldown = 0f;
    private float _flashTimer = 0f;
    private float _reloadTimer = 0f;

    private const float FireRate = 0.12f;
    private const float ReloadDuration = 1.2f;

    public Weapon(string name, int maxAmmo)
    {
        Name = name;
        MaxAmmo = maxAmmo;
        CurrentAmmo = maxAmmo;
    }

    public void Fire()
    {
        if (IsReloading || _fireCooldown > 0f || CurrentAmmo <= 0) return;

        CurrentAmmo--;
        _fireCooldown = FireRate;
        IsFiringFlash = true;
        _flashTimer = 0.08f;

        ThreadPool.QueueUserWorkItem(_ =>
        {
            try { Console.Beep(180, 45); } catch { }
        });
    }

    public void Reload()
    {
        if (IsReloading || CurrentAmmo >= MaxAmmo) return;

        IsReloading = true;
        _reloadTimer = ReloadDuration;

        ThreadPool.QueueUserWorkItem(_ =>
        {
            try
            {
                Console.Beep(400, 60);
                Thread.Sleep(80);
                Console.Beep(600, 80);
            }
            catch { }
        });
    }

    public void Update(float deltaTime)
    {
        if (_fireCooldown > 0f) _fireCooldown -= deltaTime;

        if (_flashTimer > 0f)
        {
            _flashTimer -= deltaTime;
            if (_flashTimer <= 0f) IsFiringFlash = false;
        }

        if (IsReloading)
        {
            _reloadTimer -= deltaTime;
            if (_reloadTimer <= 0f)
            {
                IsReloading = false;
                CurrentAmmo = MaxAmmo;
            }
        }
    }
}

// ==========================================
// 6. 2D -> 3D 레이캐스팅 렌더러 & 3D 원근 UI
// ==========================================
public class Renderer3D
{
    private readonly int _width;
    private readonly int _height;
    private readonly char[,] _frameBuffer;
    private const double Fov = Math.PI / 3.0;

    public Renderer3D(int width, int height)
    {
        _width = width;
        _height = height;
        _frameBuffer = new char[height, width];
    }

    public void RenderFrame(Player player, ApartmentMap map, Weapon weapon)
    {
        int horizonOffset = (int)(player.ZHeight * 8);
        int prevHitX = -1;
        int prevHitY = -1;

        for (int x = 0; x < _width; x++)
        {
            double rayAngle = (player.Angle - Fov / 2.0) + ((double)x / _width) * Fov;
            double eyeX = Math.Cos(rayAngle);
            double eyeY = Math.Sin(rayAngle);

            double distanceToWall = 0;
            bool hitWall = false;
            int hitTileType = 1;
            int hitX = 0, hitY = 0;

            while (!hitWall && distanceToWall < 16.0)
            {
                distanceToWall += 0.04;
                hitX = (int)(player.X + eyeX * distanceToWall);
                hitY = (int)(player.Y + eyeY * distanceToWall);

                int tile = map.GetTile(hitX, hitY);
                if (tile > 0)
                {
                    hitWall = true;
                    hitTileType = tile;
                }
            }

            bool isCornerEdge = (hitX != prevHitX || hitY != prevHitY);
            prevHitX = hitX;
            prevHitY = hitY;

            double correctedDist = distanceToWall * Math.Cos(rayAngle - player.Angle);
            if (correctedDist < 0.1) correctedDist = 0.1;

            int ceiling = (int)(_height / 2.0 - _height / correctedDist) + horizonOffset;
            int floor = _height - ceiling + (horizonOffset * 2);

            char wallShade = isCornerEdge ? '|' : GetWallShader(correctedDist, hitTileType);

            for (int y = 0; y < _height; y++)
            {
                if (y <= ceiling)
                {
                    _frameBuffer[y, x] = (y % 4 == 0 && x % 10 == 0) ? '+' : ' ';
                }
                else if (y > ceiling && y <= floor)
                {
                    if (y == ceiling + 1 || y == floor)
                        _frameBuffer[y, x] = '-';
                    else
                        _frameBuffer[y, x] = wallShade;
                }
                else
                {
                    double b = 1.0 - (((double)y - _height / 2.0 - horizonOffset) / (_height / 2.0));
                    if (b < 0.25) _frameBuffer[y, x] = '=';
                    else if (b < 0.5) _frameBuffer[y, x] = '-';
                    else if (b < 0.75) _frameBuffer[y, x] = '.';
                    else _frameBuffer[y, x] = ' ';
                }
            }
        }

        int cx = _width / 2;
        int cy = _height / 2;
        if (weapon.IsFiringFlash)
            DrawText(cx - 2, cy, "< + >", overwriteSpace: false);
        else
            DrawText(cx - 1, cy, "-+-", overwriteSpace: false);

        Draw3DPerspectiveUI(player, map, weapon);
        DrawFirstPersonAK47(weapon);

        StringBuilder sb = new StringBuilder();
        for (int y = 0; y < _height; y++)
        {
            for (int x = 0; x < _width; x++)
            {
                sb.Append(_frameBuffer[y, x]);
            }
            sb.AppendLine();
        }

        Console.SetCursorPosition(0, 0);
        Console.Write(sb.ToString());
    }

    private char GetWallShader(double distance, int tileType)
    {
        if (tileType == 3) return distance < 6 ? '/' : ':';

        if (distance <= 2.0) return '#';
        if (distance <= 3.5) return '@';
        if (distance <= 5.5) return '%';
        if (distance <= 8.0) return '+';
        if (distance <= 11.0) return ':';
        return '.';
    }

    private void Draw3DPerspectiveUI(Player player, ApartmentMap map, Weapon weapon)
    {
        string zone = map.GetZoneName(player.X, player.Y);
        DrawText(2, 1,  @"+--------------------------------+", overwriteSpace: true);
        DrawText(3, 2, $@"| LOC : {zone,-24} |\", overwriteSpace: true);
        DrawText(4, 3,  @"| [WASD]Move [Mouse]Look [Spc]Jmp| \", overwriteSpace: true);
        DrawText(5, 4,  @"+--------------------------------+  \", overwriteSpace: true);
        DrawText(6, 5,  @" \__________________________________\", overwriteSpace: false);

        int rx = _width - 35;
        string status = weapon.IsReloading ? "RELOADING..." : (weapon.CurrentAmmo == 0 ? "PRESS [R]!" : "READY");
        DrawText(rx, 1,      @"+----------------------------+", overwriteSpace: true);
        DrawText(rx - 1, 2, $@"/| WEAPON : {weapon.Name,-16} |", overwriteSpace: true);
        DrawText(rx - 2, 3, $@"/ | AMMO   : {weapon.CurrentAmmo,2} / {weapon.MaxAmmo} (INF)   |", overwriteSpace: true);
        DrawText(rx - 3, 4, $@"/  | STATUS : {status,-16} |", overwriteSpace: true);
        DrawText(rx - 4, 5,  @"   +----------------------------+", overwriteSpace: true);
    }

    private void DrawFirstPersonAK47(Weapon weapon)
    {
        int gunX = _width / 2 + 4;
        int gunY = _height - 10;

        if (weapon.IsFiringFlash)
        {
            gunY += 1;
            gunX += 1;
        }
        else if (weapon.IsReloading)
        {
            gunY += 3;
        }

        if (weapon.IsFiringFlash)
        {
            DrawText(gunX - 7, gunY - 3, @"    \  |  /    ", overwriteSpace: false);
            DrawText(gunX - 9, gunY - 2, @"  --== ( * ) ==--", overwriteSpace: false);
            DrawText(gunX - 7, gunY - 1, @"    /  |  \    ", overwriteSpace: false);
        }

        string[] akModel =
        {
            @"       /===[_]==\           ",
            @"      /==========\          ",
            @"     /[AK-47]=====\____     ",
            @"    ( (L-HAND) )===|____|   ",
            @"     \________/   /  /      ",
            @"        |  |     /  /       ",
            @"       (WRIST)  (R-HAND)    ",
            @"      /      \  /      \    "
        };

        for (int i = 0; i < akModel.Length; i++)
        {
            DrawText(gunX, gunY + i, akModel[i], overwriteSpace: false);
        }
    }

    private void DrawText(int startX, int startY, string text, bool overwriteSpace)
    {
        if (startY < 0 || startY >= _height) return;
        for (int i = 0; i < text.Length; i++)
        {
            int px = startX + i;
            if (px >= 0 && px < _width)
            {
                if (overwriteSpace || text[i] != ' ')
                {
                    _frameBuffer[startY, px] = text[i];
                }
            }
        }
    }
}
