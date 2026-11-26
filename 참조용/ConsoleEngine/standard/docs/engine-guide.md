# 엔진 가이드 (v0.2.0)

입력 · 갱신 · 렌더링만 하는 아주 작은 콘솔 게임 엔진입니다.
게임은 `GameBase`를 상속하고 `Input` · `Update` · `Render`를 채웁니다.

## 5분 시작

1. 게임 프로젝트 우클릭 › 추가 › 프로젝트 참조 › `ConsoleEngine` 체크
2. `GameBase`를 상속하고 세 메서드를 `protected override`로 채운다
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

    protected override void Update(float deltaTime) { }

    protected override void Render(Screen screen)
    {
        screen.Draw(_x, 5, '@');
    }
}
```

## 루프 순서 (한 프레임)

1. 입력: 쌓인 키를 모두 `Input`으로 (키마다 한 번)
2. `Quit()`을 불렀다면 여기서 끝
3. `Update(deltaTime)`
4. 화면 버퍼를 지우고 `Render(screen)`
5. 버퍼를 한 번에 출력, 남은 시간만큼 대기

## API

| 멤버 | 하는 일 |
|---|---|
| `GameBase(width, height, framesPerSecond = 20)` | 화면 크기와 프레임 속도 |
| `Run()` | 게임 루프 시작. `Quit()`을 부를 때까지 돈다 |
| `Quit()` | 이번 프레임의 입력 처리 뒤 루프를 끝낸다 |
| `Input(ConsoleKey key)` | 키가 눌릴 때마다. 한 프레임에 여러 번 올 수 있다 |
| `Update(float deltaTime)` | 매 프레임 한 번. 상태(위치·점수·충돌)를 바꾼다 |
| `Render(Screen screen)` | 매 프레임 한 번. 지금 상태를 그린다 |
| `screen.Draw(x, y, c)` | 글자 하나. 화면 밖은 무시 |
| `screen.DrawText(x, y, text)` | (x, y)부터 오른쪽으로 한 글자씩. 화면 밖 글자는 무시 (v0.2.0, #6) |
| `screen.Width`, `screen.Height` | 화면 크기 |

## 좌표계

- 왼쪽 위가 (0, 0). x는 오른쪽, y는 아래로 커진다
- 화면 밖 좌표의 `Draw`는 조용히 무시된다

## 프레임 속도

- 기본 20 FPS: `deltaTime` = 0.05초 (늘 같은 값)
- 바꾸기: `base(30, 20, 30)` → 30 FPS
- 느린 프레임에도 `deltaTime`은 그대로 (입문용 단순화)

## 입력 규칙

- 키를 누를 때마다 `Input`이 한 번 불린다
- 누르고 있는 상태는 알 수 없다 (키 반복만 들어온다)

## 제약

- 콘솔 창이 Width × Height보다 커야 한다
- ASCII 문자만: 한글은 2칸을 차지해 줄이 밀린다 (이슈 #9 → PR #10, ADR 0002)
