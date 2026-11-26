using System.Diagnostics;

namespace ConsoleEngine;

/// <summary>콘솔 게임의 뼈대. 상속해서 Input·Update·Render를 채운다.</summary>
public abstract class GameBase
{
    private readonly Screen _screen;
    private readonly int _frameMs;
    private bool _quitRequested;

    protected GameBase(int width, int height, int framesPerSecond = 20)
    {
        _screen = new Screen(width, height);
        _frameMs = 1000 / framesPerSecond;
    }

    public void Run()
    {
        Console.CursorVisible = false;
        Console.Clear();
        var watch = new Stopwatch();
        float deltaTime = _frameMs / 1000f;      // 고정 프레임 시간(초)
        while (true)
        {
            watch.Restart();
            while (Console.KeyAvailable)           // ① 입력: 쌓인 키를 모두
                Input(Console.ReadKey(true).Key);
            if (_quitRequested) break;
            Update(deltaTime);                     // ② 갱신
            _screen.Clear();                       // ③ 렌더링
            Render(_screen);
            _screen.Present();
            int wait = _frameMs - (int)watch.ElapsedMilliseconds;
            if (wait > 0) Thread.Sleep(wait);      // 프레임 속도 맞추기
        }
        Console.CursorVisible = true;
    }

    protected void Quit() { _quitRequested = true; }

    /// <summary>키가 눌릴 때마다 엔진이 부른다. 한 프레임에 여러 번 올 수 있다.</summary>
    /// <param name="key">눌린 키. 예: ConsoleKey.LeftArrow</param>
    protected abstract void Input(ConsoleKey key);

    /// <summary>매 프레임 한 번. 게임 상태(위치·점수·충돌)를 바꾼다.</summary>
    /// <param name="deltaTime">한 프레임의 시간(초). 기본 0.05</param>
    protected abstract void Update(float deltaTime);

    /// <summary>매 프레임 한 번. 지금 상태를 screen에 그린다.</summary>
    /// <param name="screen">이번 프레임의 화면 버퍼</param>
    protected abstract void Render(Screen screen);
}
