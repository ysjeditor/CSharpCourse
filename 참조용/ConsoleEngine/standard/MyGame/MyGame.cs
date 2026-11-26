using ConsoleEngine;

// 시작용 게임 — 이 클래스를 채워 우리 팀의 게임을 만든다.
// 엔진 사용법: docs/engine-guide.md · 완성 예시: DodgeGame 프로젝트
class MyGame : GameBase
{
    private const int Width = 30;    // TODO: 기획서의 화면 크기
    private const int Height = 20;

    private int _playerX = Width / 2;

    public MyGame() : base(Width, Height) { }

    protected override void Input(ConsoleKey key)
    {
        if (key == ConsoleKey.Escape) Quit();
        // TODO: 기획서의 조작 규칙. 지금은 ←/→ 이동만 있다
        if (key == ConsoleKey.LeftArrow && _playerX > 0) _playerX--;
        if (key == ConsoleKey.RightArrow && _playerX < Width - 1)
            _playerX++;
    }

    protected override void Update(float deltaTime)
    {
        // TODO: 매 프레임 바뀌는 것 (시간, 적 이동, 충돌 검사)
    }

    protected override void Render(Screen screen)
    {
        // 화면 글자는 ASCII만 — 한글은 2칸을 차지해 줄이 밀린다 (ADR 0002)
        screen.DrawText(0, 0, "MY GAME - Esc: quit");
        screen.Draw(_playerX, Height - 1, '@');
        // TODO: 기획서의 화면 배치도대로 그리기
    }
}
