# 시스템 계획문서 — 피하기 게임
기준: design/README.md v1.0 · 엔진 v0.1.0

<!-- 예시: PR #5로 병합된 판(2026-12-04, 기획 담당 리뷰 반영: 규칙 6에 "시간도 0"). 이후 기획서 v1.1(PR #11)에서 화면 문구가 ASCII로 바뀌었지만 이 문서의 내용에는 영향이 없다. -->

## 1. 클래스
| 형식 | 파일 | 하는 일 |
|---|---|---|
| DodgeGame : GameBase | DodgeGame.cs | 상태를 들고 Input·Update·Render를 채운다 |
| Rock | Rock.cs | 돌 하나의 위치 (X: 칸, Y: 실수) |
| GameState (enum) | GameState.cs | Playing / GameOver / Clear |

## 2. 상수 (기획서 숫자는 여기에만)
Width 30, Height 20 (규칙 1) ·
SpawnInterval 0.3f, RockSpeed 10f (규칙 3) ·
GoalSeconds 60f (최종 목표)

## 3. 상태와 데이터
- _state: Playing → (충돌) GameOver / (60초) Clear → (R) Playing
- _playerX = 15 · _rocks = 빈 목록 · _spawnTimer = 0 · _time = 0

## 4. 한 프레임에 하는 일
- Input  : Esc → Quit / 끝난 상태면 R → Restart /
  Playing이면 ←→ 이동(0~29)
- Update : Playing일 때만 — 시간 += dt → 60 이상이면 Clear /
  생성 타이머 / 돌 낙하 / 맨 아래 줄 같은 칸이면 GameOver /
  화면 밖 돌 제거
- Render : 돌 → @ → 상태 줄(0, 0) → 끝 메시지(가운데 줄 y=9)

## 5. 규칙 ↔ 구현 대응표
| 기획 규칙 | 구현 위치 | 확인 방법 |
|---|---|---|
| 1 30×20, 아래 가운데 | base(Width, Height), _playerX = Width / 2 | 실행 첫 화면 |
| 2 ←/→ 한 칸, 밖 금지 | Input | 왼쪽 끝에서 ← 연타 |
| 3 0.3초마다 생성, 초당 10칸 | Update, SpawnInterval, RockSpeed | 돌이 2초에 바닥까지 |
| 4 닿으면 GAME OVER | Update 충돌 검사 | 일부러 맞기 |
| 5 시간 표시, 60초 CLEAR | Update _time, Render 상태 줄 | 60초 버티기 |
| 6 R 다시(시간도 0), Esc 종료 | Input, Restart | 끝난 화면에서 R |
| 최종 목표 | GoalSeconds | 5번과 같음 |

## 6. 엔진에 필요한 것
글자 쓰기(상태 줄·끝 메시지) → 엔진에 없음 → 이슈 #6 DrawText 기능 요청

## 7. 작업 순서
게임 v0.1 움직이기: 규칙 1·2·6(Esc) →
게임 v0.2 장애물·충돌: 규칙 3·4 →
게임 v1.0 완성: 규칙 5·6(R)
