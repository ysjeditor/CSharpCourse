using System.Text;

namespace ConsoleEngine;

/// <summary>
/// 입문판 엔진. 상속해서 Input·Update·Render 중 필요한 것만 override하면 게임이 된다.
/// 한 프레임 = ① 입력 → ② 갱신 → ③ 지우기 → ④ 그리기 → ⑤ 쉬기
/// </summary>
public class GameBase
{
    protected readonly int Width;            // 화면 가로 칸 수
    protected readonly int Height;           // 화면 세로 칸 수
    protected readonly int FramesPerSecond;  // 1초에 Update가 불리는 횟수
    private bool _quit;

    public GameBase(int width, int height, int framesPerSecond = 10)
    {
        Width = width;
        Height = height;
        FramesPerSecond = framesPerSecond;
    }

    /// <summary>게임 루프를 시작한다. Quit()을 부를 때까지 돈다.</summary>
    public void Run()
    {
        Console.OutputEncoding = Encoding.UTF8;    // 한글 출력
        Console.CursorVisible = false;
        Console.Clear();
        string blankLine = new string(' ', Width);
        while (!_quit)
        {
            while (Console.KeyAvailable)           // ① 입력: 쌓인 키를 모두
                Input(Console.ReadKey(true).Key);
            if (_quit) break;
            Update();                              // ② 갱신
            for (int y = 0; y < Height; y++)       // ③ 지우기: 줄마다 빈칸으로 덮기
            {
                Console.SetCursorPosition(0, y);
                Console.Write(blankLine);
            }
            Render();                              // ④ 그리기
            Thread.Sleep(1000 / FramesPerSecond);  // ⑤ 쉬기 (대략 맞춘다)
        }
        Console.SetCursorPosition(0, Height);
        Console.CursorVisible = true;
    }

    /// <summary>이번 프레임이 끝나면 루프를 멈춘다.</summary>
    protected void Quit() { _quit = true; }

    /// <summary>(x, y)에 글자 하나를 쓴다. 화면 밖은 무시.</summary>
    protected void Draw(int x, int y, char c)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) return;
        Console.SetCursorPosition(x, y);
        Console.Write(c);
    }

    /// <summary>(x, y)부터 글을 쓴다. 한글은 2칸을 차지하니 그 줄의 맨 끝 글로만 쓴다.</summary>
    protected void DrawText(int x, int y, string text)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) return;
        Console.SetCursorPosition(x, y);
        Console.Write(text);
    }

    /// <summary>키가 눌릴 때마다 불린다. 한 프레임에 여러 번 올 수 있다.</summary>
    protected virtual void Input(ConsoleKey key) { }

    /// <summary>매 프레임 한 번. 위치·시간·충돌 같은 상태를 바꾼다.</summary>
    protected virtual void Update() { }

    /// <summary>매 프레임 한 번. 지금 상태를 Draw·DrawText로 그린다.</summary>
    protected virtual void Render() { }
}
