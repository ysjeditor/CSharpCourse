using System.Text;

namespace ConsoleEngine;

/// <summary>한 프레임을 그려 두는 문자 버퍼. Present 때 한 번에 출력한다.</summary>
public class Screen
{
    public readonly int Width;
    public readonly int Height;
    private readonly char[,] _cells;
    private readonly StringBuilder _frame = new StringBuilder();

    public Screen(int width, int height)
    {
        Width = width;
        Height = height;
        _cells = new char[height, width];
    }

    public void Clear()
    {
        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                _cells[y, x] = ' ';
    }

    public void Draw(int x, int y, char c)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) return;  // 화면 밖은 무시
        _cells[y, x] = c;
    }

    /// <summary>(x, y)부터 한 글자씩 오른쪽으로 그린다. 화면 밖 글자는 무시. (v0.2.0, #6)</summary>
    /// <param name="text">ASCII 문자만. 한글은 2칸을 차지해 줄이 밀린다 (ADR 0002)</param>
    public void DrawText(int x, int y, string text)
    {
        for (int i = 0; i < text.Length; i++) Draw(x + i, y, text[i]);
    }

    internal void Present()
    {
        _frame.Clear();
        for (int y = 0; y < Height; y++)
        {
            for (int x = 0; x < Width; x++) _frame.Append(_cells[y, x]);
            _frame.Append('\n');
        }
        Console.SetCursorPosition(0, 0);   // 지우지 않고 덮어써서 깜빡임 방지
        Console.Write(_frame.ToString());
    }
}
