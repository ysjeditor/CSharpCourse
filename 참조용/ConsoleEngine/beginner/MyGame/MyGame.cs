using ConsoleEngine;

// 시작용 게임 — 이 클래스를 채워 우리 팀의 게임을 만든다.
// 엔진 사용법: docs/engine-guide.md · 완성 예시: DodgeGame 프로젝트
class MyGame : GameBase
{
    private int _playerX;

    public MyGame() : base(30, 20)   // TODO: 기획서의 화면 크기
    {
        _playerX = Width / 2;
    }

    protected override void Input(ConsoleKey key)
    {
        if (key == ConsoleKey.Escape) Quit();
        // TODO: 기획서의 조작 규칙. 지금은 ←/→ 이동만 있다
        if (key == ConsoleKey.LeftArrow && _playerX > 0) _playerX--;
        if (key == ConsoleKey.RightArrow && _playerX < Width - 1)
            _playerX++;
    }

    protected override void Update()
    {
        // TODO: 매 프레임 바뀌는 것 (시간, 적 이동, 충돌 검사)
    }

    protected override void Render()
    {
        Draw(_playerX, Height - 1, '@');
        // TODO: 기획서의 화면 배치도대로 그리기
        DrawText(0, 0, "내 게임 - Esc: 끝");   // 한글 글은 맨 나중에, 줄 끝에
    }
}
