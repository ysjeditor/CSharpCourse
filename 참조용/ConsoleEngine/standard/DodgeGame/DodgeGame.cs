using ConsoleEngine;

// 게임 v1.0 (태그 game-v1.0.0) — docs/system-plan.md의 규칙 ↔ 구현 대응표를 따른다
class DodgeGame : GameBase
{
    private const int Width = 30;             // 규칙 1: 30×20칸
    private const int Height = 20;
    private const float SpawnInterval = 0.3f; // 규칙 3
    private const float RockSpeed = 10f;
    private const float GoalSeconds = 60f;    // 최종 목표

    private readonly List<Rock> _rocks = new List<Rock>();
    private int _playerX = Width / 2;         // 맨 아래 줄 가운데
    private float _spawnTimer;
    private float _time;
    private GameState _state = GameState.Playing;

    public DodgeGame() : base(Width, Height) { }

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
        _spawnTimer = 0f;
        _time = 0f;
        _state = GameState.Playing;
    }

    protected override void Update(float deltaTime)
    {
        if (_state != GameState.Playing) return;
        _time += deltaTime;
        if (_time >= GoalSeconds)
        {
            _state = GameState.Clear;
            return;
        }
        _spawnTimer -= deltaTime;
        if (_spawnTimer <= 0f)
        {
            _rocks.Add(new Rock(Random.Shared.Next(Width)));
            _spawnTimer = SpawnInterval;
        }
        for (int i = _rocks.Count - 1; i >= 0; i--)
        {
            Rock rock = _rocks[i];
            rock.Y += RockSpeed * deltaTime;             // 초당 10칸
            if ((int)rock.Y == Height - 1 && rock.X == _playerX)
                _state = GameState.GameOver;              // 규칙 4
            if (rock.Y >= Height) _rocks.RemoveAt(i);
        }
    }

    protected override void Render(Screen screen)
    {
        foreach (Rock rock in _rocks)
            screen.Draw(rock.X, (int)rock.Y, '*');
        screen.Draw(_playerX, Height - 1, '@');
        screen.DrawText(0, 0, $"TIME {(int)_time}/{(int)GoalSeconds}");
        if (_state == GameState.GameOver)
            screen.DrawText(5, 9, "GAME OVER - R: retry");
        if (_state == GameState.Clear)
            screen.DrawText(6, 9, "CLEAR! - R: retry");
    }
}
