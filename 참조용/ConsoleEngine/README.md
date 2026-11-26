# 3인 협동 실습 샘플 — C# 콘솔 피하기 게임

게임 개발 개념 라이브러리의 **3인 협동 실습: C# 콘솔 게임** 시리즈(개요 · 기획 · 엔진 · 시스템 · 통합 · 회고)에서 쓰는 실제 코드와 문서입니다.
폴더 이름, 파일 경로, 엔진 API, 피하기 게임 규칙은 시리즈 페이지와 같습니다.

## 들어 있는 것

| 폴더·파일 | 내용 | 주로 쓰는 역할 |
|---|---|---|
| `beginner/` | **입문판** 엔진(파일 하나) + 시작용 `MyGame` + 피하기 게임 예시 `DodgeGame` + 사용 문서 | 엔진 · 시스템 |
| `standard/` | **표준판** 엔진(시리즈 '엔진 담당' 페이지와 같은 코드) + `MyGame` + `DodgeGame` v1.0 + 사용 문서 | 엔진 · 시스템 |
| `docs/templates/` | 빈 기획설계문서 `design/README.md`, 빈 시스템 계획문서 `docs/system-plan.md` | 기획 · 시스템 |
| `docs/examples/` | 피하기 게임으로 채운 기획설계문서(+ 화면 배치도·흐름도 SVG)와 시스템 계획문서 | 기획 · 시스템 |
| `prompts/` | 역할별 AI 검토 프롬프트 7개와 쓰는 법 | 모두 |
| `prompt-builder.html` | 문서·코드를 붙여 넣으면 프롬프트를 완성해 주는 도구 (인터넷 없이 열림) | 모두 |

## 입문판과 표준판 고르기

| | 입문판 `beginner/` | 표준판 `standard/` |
|---|---|---|
| 엔진 파일 | `GameBase.cs` 하나 | `GameBase.cs` + `Screen.cs` |
| 채우는 메서드 | `Input(ConsoleKey)` · `Update()` · `Render()` — 필요한 것만 override (`virtual`) | `Input(ConsoleKey)` · `Update(float deltaTime)` · `Render(Screen)` — 셋 다 override (`abstract`) |
| 시간 | 프레임 수로 센다 (기본 초당 10프레임) | 델타 타임(초)으로 센다 |
| 그리기 | `Draw` · `DrawText`가 바로 콘솔에 쓴다 (조금 깜빡일 수 있음) | `Screen` 버퍼에 그린 뒤 한 번에 출력 (깜빡임 없음) |
| 필요한 C# | 클래스, 상속, override | 위 + 추상 클래스, 실수 시간 계산 |

처음 해 보는 팀은 입문판으로 시작하고, 익숙해지면 표준판의 `Screen`과 델타 타임을 비교해 보세요. 두 판의 차이는 `beginner/docs/engine-guide.md`의 "표준판과 다른 점"에 정리돼 있습니다.

## 여는 법 (Visual Studio)

1. `beginner/ConsoleEngineCoop.sln` 또는 `standard/ConsoleEngineCoop.sln`을 엽니다.
2. 시작 프로젝트는 `MyGame`입니다. <kbd>Ctrl</kbd>+<kbd>F5</kbd>로 실행하면 `@`가 ←/→로 움직이고, <kbd>Esc</kbd>로 끝납니다.
3. 완성 예시를 보려면 솔루션 탐색기에서 `DodgeGame`을 오른쪽 클릭 → **시작 프로젝트로 설정** → <kbd>Ctrl</kbd>+<kbd>F5</kbd>. 60초 동안 떨어지는 돌을 피하면 성공, <kbd>R</kbd>로 다시 시작합니다.

명령줄에서는 `dotnet run --project MyGame`(또는 `DodgeGame`)으로 실행합니다.

- **필요한 것:** .NET 10 SDK (프로젝트의 `TargetFramework`가 `net10.0`).
  .NET 10을 설치할 수 없는 PC에서는 각 `.csproj`의 `net10.0`을 `net8.0`으로 바꾸면 됩니다 (두 판 모두 .NET 8로도 경고 없이 빌드되는 것을 확인했습니다).
- 콘솔 창에서 실행해야 합니다. 출력 창이나 입력을 파일로 돌린 상태에서는 키 입력을 읽을 수 없습니다.

## 역할별 시작점

시리즈의 팀 저장소 구조(`/ConsoleEngine`, 게임 프로젝트, `/design`, `/docs`)에 맞춰 필요한 파일을 복사해 씁니다.

- **기획 담당** — `docs/templates/design/README.md`를 팀 저장소의 `design/README.md`로 복사해 채웁니다. 막히면 `docs/examples/design/`의 예시와 SVG를 봅니다.
- **엔진 담당** — 고른 판의 `ConsoleEngine/`과 `docs/engine-guide.md`가 출발점입니다. 엔진 문서는 시스템 담당이 이것만 보고 게임을 만들 수 있어야 합니다 (`prompts/05-engine-doc-check.md`로 점검).
- **시스템 담당** — `docs/templates/docs/system-plan.md`를 팀 저장소의 `docs/system-plan.md`로 복사해 먼저 채운 뒤, `MyGame`에서 게임을 만듭니다. `DodgeGame`은 막혔을 때 비교해 보는 예시입니다.

## AI에게 물어보며 점검하기

`prompt-builder.html`을 더블클릭해 브라우저로 엽니다 (인터넷이 없어도 됩니다).

1. 상황에 맞는 프롬프트를 고릅니다. 예: 규칙 점검, 아이디어 시험, 시스템 계획 대조, 테스트 사례, 엔진 문서 점검, PR 리뷰, 버그 리포트.
2. 칸마다 자기 문서나 코드를 붙여 넣습니다.
3. 완성된 프롬프트를 복사해 쓰고 있는 AI 채팅에 붙여 넣습니다. `.md`로 저장해 두었다가 다시 쓸 수도 있습니다.

`prompts/*.md`를 직접 열어 `{{ }}` 자리를 채워 써도 됩니다. 자세한 사용법은 `prompts/README.md`에 있습니다.

- 모든 프롬프트는 AI가 **고쳐 주거나 대신 쓰지 않고, 문제를 질문과 지적으로 짚도록** 요청합니다. 생각은 우리가 하고 AI는 빈틈을 찾는 데 씁니다.
- AI의 답은 그대로 믿거나 커밋하지 말고, 실제로 빌드·실행해 보고 팀과 이야기한 뒤 반영합니다.
- 비밀번호, 토큰, 개인 정보는 붙여 넣지 않습니다.

## 강사용 메모

- 나눠 줄 때 `bin/`, `obj/` 폴더가 없는지 확인한 뒤 zip으로 묶습니다 (지금은 없습니다).
- 시스템 담당이 처음부터 직접 만들게 하려면 `DodgeGame` 폴더를 빼고 줍니다. 이때 솔루션에서도 빼야 열 때 오류가 나지 않습니다: Visual Studio에서 `DodgeGame` 오른쪽 클릭 → **제거**, 또는 `dotnet sln ConsoleEngineCoop.sln remove DodgeGame/DodgeGame.csproj`.
- 표준판 `DodgeGame`은 시리즈 페이지 코드와 같아서, 실수(`float`) 시간의 누적 오차가 그대로 있습니다.
  - 0.3초 타이머에서 0.05초를 여섯 번 빼도 아주 작은 값이 남아, 돌이 실제로는 7프레임(0.35초)마다 생깁니다.
  - 같은 이유로 60초 성공 판정이 한 프레임 늦은 60.05초에 납니다.
  - 플레이에는 거의 티가 나지 않지만, "실수 시간 비교"를 토론하는 재료로 쓸 수 있습니다. 입문판은 프레임 수(정수)로 세서 이 문제가 없습니다.
- `prompt-builder.html` 안의 프롬프트는 `prompts/*.md`의 사본입니다. md를 고친 뒤에는 도구의 **md 파일 불러오기**로 고친 파일을 바로 쓸 수 있습니다.
