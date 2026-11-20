# GitHub README 작성 입문

[index.html](index.html)을 더블 클릭하면 학습 문서가 열립니다. 기존 프로그램의 흐름 문서처럼 버튼에 따라 수정 대상 줄과 해당 구역이 강조됩니다. Markdown 원문과 GitHub 스타일 미리보기를 비교하며 읽습니다.

## 주요 기능

- assets·docs·src·루트 README 역할 선택과 폴더 강조
- 제목·강조·목록·체크·링크·이미지·표·코드 블록의 원문/표시 예시
- 실제 `templates/1_Project/README.md` 원본과 완성 예시 비교
- README 작업 버튼 9개: 수정 위치 자동 스크롤, 줄 강조, 정확한 추가·교체 지시, 복사할 Markdown
- 루트·docs·날짜 하위 문서를 기준으로 상대경로 계산
- 게시 전 직접 확인 체크리스트

문서와 예시 그림은 HTML에 내장되어 있어 읽기에는 인터넷·Python·서버가 필요하지 않습니다. 실제 GitHub 저장소를 수정하거나 게시하는 기능은 없습니다. 미리보기의 문서 링크는 대상 경로를 설명하며 외부로 이동하지 않습니다.

## 실제 파일로 비교

`samples/완성예시`에 README와 assets·docs·src를 함께 두었습니다. 예시 날짜는 2026-11-19입니다. 자신의 작업으로 활용할 때 이름·날짜·내용·PR 상태를 실제 사실로 바꾸세요. 예시 콘솔 프로젝트는 .NET 10 SDK로 실행합니다.

```bash
dotnet run --project ./src/HelloReadme/HelloReadme.csproj -c Release
```

이 명령은 **samples/완성예시 폴더를 현재 폴더로 둔 상태**에서 실행합니다. 예상 출력은 `안녕하세요, GitHub!`입니다. 원본 templates/1_Project는 수정하지 않습니다.

## 유지관리

`교재.md`는 9개 단원의 원본입니다. `python build.py`로 HTML을 재생성합니다. 기존 입문웹교재의 변환기·스타일과 templates/1_Project 원본이 필요합니다. 제목이나 표 위치를 기준으로 강조 줄을 다시 계산합니다. 원본 스냅샷 해시는 `template-manifest.json`에 기록합니다.

`python 검증.py`는 강조 범위·상대경로·완성 예시 링크·문법·샘플 실행을 검사합니다. 검증에는 Python·Node.js·.NET 10 SDK가 필요하지만 학생이 HTML을 읽는 데는 필요하지 않습니다. Markdown 미리보기는 이 문서에서 다루는 기본 문법용이며 전체 GitHub 렌더러를 대체하지 않습니다.
