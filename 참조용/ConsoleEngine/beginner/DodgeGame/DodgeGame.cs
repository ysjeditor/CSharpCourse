using ConsoleEngine;

// 피하기 게임 — 입문판. 규칙은 표준판과 같고, 시간을 '초' 대신 '프레임'으로 센다.
// 초당 10프레임이므로: 돌은 프레임마다 1칸(초당 10칸), 3프레임마다 생성(0.3초),
// 600프레임(60초)을 버티면 승리.
class DodgeGame : GameBase
{
    private const int SpawnEveryFrames = 3;   // 규칙 3: 0.3초마다 돌 하나
    private const int GoalSeconds = 60;       // 최종 목표: 60초 버티기

    private readonly List<Rock> _rocks = new List<Rock>();
    private int _playerX;
    private int _frame;                       // 지금까지 지난 프레임 수
    private GameState _state = GameState.Playing;

    public DodgeGame() : base(30, 20)         // 규칙 1: 30×20칸, 초당 10프레임
    {
        _playerX = Width / 2;                 // 맨 아래 줄 가운데
    }

    protected override void Input(ConsoleKey key)
    {
        if (key == ConsoleKey.Escape) Quit();            // 규칙 6
        if (_state != GameState.Playing)
        {
            if (key == ConsoleKey.R) Restart();
            return;
        }
        if (key == ConsoleKey.LeftArrow && _playerX > 0) _playerX--;
        if (key == ConsoleKey.RightArrow && _playerX < Width - 1)
            _playerX++;                                   // 규칙 2
    }

    private void Restart()
    {
        _rocks.Clear();
        _playerX = Width / 2;
        _frame = 0;
        _state = GameState.Playing;
    }

    protected override void Update()
    {
        if (_state != GameState.Playing) return;
        _frame++;
        if (_frame >= GoalSeconds * FramesPerSecond)     // 규칙 5
        {
            _state = GameState.Clear;
            return;
        }
        if (_frame % SpawnEveryFrames == 0)
            _rocks.Add(new Rock(Random.Shared.Next(Width)));
        for (int i = _rocks.Count - 1; i >= 0; i--)
        {
            Rock rock = _rocks[i];
            rock.Y++;                                     // 한 프레임에 한 칸
            if (rock.Y == Height - 1 && rock.X == _playerX)
                _state = GameState.GameOver;              // 규칙 4
            if (rock.Y >= Height) _rocks.RemoveAt(i);
        }
    }

    protected override void Render()
    {
        foreach (Rock rock in _rocks)
            Draw(rock.X, rock.Y, '*');
        Draw(_playerX, Height - 1, '@');

        // 한글은 화면에서 2칸을 차지한다(이슈 #9). 그래서 글은 맨 나중에,
        // 그 줄의 오른쪽에 아무것도 그리지 않는 자리에만 쓴다.
        DrawText(0, 0, $"시간 {_frame / FramesPerSecond} / {GoalSeconds}초");
        if (_state == GameState.GameOver)
            DrawText(5, 9, "게임 오버 - R: 다시");
        if (_state == GameState.Clear)
            DrawText(6, 9, "성공! - R: 다시");
    }
}
