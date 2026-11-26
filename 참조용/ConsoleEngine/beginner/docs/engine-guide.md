# 엔진 가이드 — 입문판

클래스와 상속만 알면 쓸 수 있는 아주 작은 콘솔 게임 엔진입니다.
`GameBase`를 상속하고 `Input` · `Update` · `Render` 중 필요한 것만 `override`합니다.

## 5분 시작

1. 게임 프로젝트 우클릭 › 추가 › 프로젝트 참조 › `ConsoleEngine` 체크
2. `GameBase`를 상속한 클래스를 만든다
3. `Program.cs`에 `new 내게임().Run();` 한 줄 → Ctrl+F5

```csharp
using ConsoleEngine;

new HelloGame().Run();

class HelloGame : GameBase
{
    private int _x = 10;

    public HelloGame() : base(30, 10) { }

    protected override void Input(ConsoleKey key)
    {
        if (key == ConsoleKey.LeftArrow) _x--;
        if (key == ConsoleKey.RightArrow) _x++;
        if (key == ConsoleKey.Escape) Quit();
    }

    protected override void Render()
    {
        Draw(_x, 5, '@');
    }
}
```

## 한 프레임에 일어나는 일

1. 입력: 쌓인 키를 모두 `Input`으로 (키마다 한 번)
2. `Quit()`을 불렀다면 여기서 끝
3. `Update()`
4. 화면을 빈칸으로 지우고 `Render()`
5. 1초 ÷ 프레임 수만큼 쉬기 (기본 10프레임 → 0.1초)

## 쓸 수 있는 것

| 멤버 | 하는 일 |
|---|---|
| `GameBase(width, height, framesPerSecond = 10)` | 화면 크기와 1초에 몇 프레임인지 |
| `Width`, `Height`, `FramesPerSecond` | 위 값을 자식 클래스에서 읽기 |
| `Run()` | 게임 시작. `Quit()`을 부를 때까지 돈다 |
| `Quit()` | 이번 프레임이 끝나면 멈춘다 |
| `Draw(x, y, c)` | 글자 하나. 화면 밖은 무시 |
| `DrawText(x, y, text)` | (x, y)부터 글 쓰기 |
| `Input(ConsoleKey key)` | 키가 눌릴 때마다 불린다 |
| `Update()` | 매 프레임 한 번. 상태를 바꾼다 |
| `Render()` | 매 프레임 한 번. 그린다 |

## 알아 둘 것

- 좌표: 왼쪽 위가 (0, 0). x는 오른쪽, y는 아래로 커진다.
- 시간: 입문판에는 델타 타임이 없다. 시간은 **프레임 수**로 센다.
  10프레임 = 1초. 예) 0.3초마다 → 3프레임마다, 60초 → 600프레임.
- 한글: 화면에서 2칸을 차지한다. 입문판은 글을 콘솔에 바로 쓰므로,
  한글 글은 `Render`의 맨 마지막에, 그 줄 오른쪽에 아무것도 그리지 않는 자리에만 쓴다.
- 깜빡임: 매 프레임 화면을 지웠다가 다시 그려서 조금 깜빡일 수 있다.
  표준판(`standard/`)은 버퍼에 다 그린 뒤 한 번에 출력해 깜빡이지 않는다.
- 콘솔 창은 Width × Height보다 커야 한다.

## 표준판과 다른 점

| | 입문판 | 표준판 |
|---|---|---|
| 메서드 | `virtual` — 필요한 것만 override | `abstract` — 셋 다 override |
| 시간 | 프레임 수 | `Update(float deltaTime)`의 초 |
| 그리기 | `Draw`로 콘솔에 바로 | `Screen` 버퍼에 그린 뒤 한 번에 |
| 한글 | 줄 끝에서는 쓸 수 있음 | ASCII만 (ADR 0002) |
