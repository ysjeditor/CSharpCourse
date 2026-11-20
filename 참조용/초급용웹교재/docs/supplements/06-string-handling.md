# 6장. 문자열 처리

### 학습 목표

문자열의 불변성을 이해하고 검색·분리·정규화·누적을 수행합니다.

### 개념 읽기

#### 기본 구조 — 반환된 문자열 저장하기

```csharp
using System.Text;

string text = " apple, banana ";
string cleaned = text.Trim();           // 앞뒤 공백을 없앤 새 문자열
string changed = cleaned.Replace("apple", "pear"); // 치환 결과 반환
string part = changed.Substring(0, 4);  // 시작 위치 0에서 길이 4: pear
string[] words = changed.Split(',');    // 구분자로 나눈 문자열 배열
bool same = "A".Equals("a", StringComparison.OrdinalIgnoreCase); // 비교 기준

var builder = new StringBuilder();      // 수정 가능한 누적 버퍼
builder.Append("첫 문장");               // 줄바꿈 없이 추가
builder.AppendLine(" 끝");               // 추가 후 줄바꿈
string result = builder.ToString();     // 누적 내용을 문자열로 얻기
```

#### 문자열을 바꾼다는 말의 의미

사용자가 이름 앞뒤에 공백을 넣었다면 등록 전에 제거할 수 있습니다. `Trim()`은 새 문자열을 반환하며 원래 객체를 수정하지 않습니다. `text.Trim();`만 호출하고 반환값을 버리면 변수는 원래 문자열을 계속 가리킵니다. `text = text.Trim();`처럼 결과를 저장하세요.

`Length`는 UTF-16 코드 단위 개수입니다. 화면에 보이는 글자 수와 항상 같지는 않습니다. `Substring(start, length)`와 범위 `text[start..end]`는 유효한 경계가 필요합니다. 마지막 경계는 포함하지 않습니다. `Replace`도 새 문자열을 반환합니다.

#### 비교 목적을 먼저 정하기

식별자나 확장자처럼 문화권에 좌우되지 않을 비교에는 `StringComparison.Ordinal` 또는 `OrdinalIgnoreCase`를 명시할 수 있습니다. 사람 이름을 사전식으로 정렬하는 경우와 비교 기준이 다릅니다. 대소문자 무시 비교를 위해 무조건 `ToLower()`로 바꾸기보다 비교 옵션을 선택하세요. 출력용 변환에는 `ToUpperInvariant`, `ToLowerInvariant`도 있습니다.

`Split`은 구분자로 문자열을 나눕니다. 연속된 쉼표에서 빈 항목을 보존할지 버릴지는 데이터 의미에 따라 정합니다. 단순한 `Split(',')`은 따옴표 안의 쉼표를 처리하는 완전한 CSV 파서가 아닙니다.

#### StringBuilder로 누적하기

반복적으로 긴 문자열을 이어 붙이면 중간 문자열이 많이 생길 수 있습니다. `StringBuilder`는 변경 가능한 버퍼에 `Append`, `AppendLine`으로 누적하고 마지막에 `ToString()`으로 문자열을 만듭니다. 짧은 보간 문자열까지 모두 대체할 필요는 없습니다.

### 따라 하기

```csharp
using System;
using System.Text;

string raw = " apple, , banana ";
string[] words = raw.Split(',',
    StringSplitOptions.TrimEntries | StringSplitOptions.RemoveEmptyEntries);
var builder = new StringBuilder();
foreach (string word in words)
{
    if (builder.Length > 0) builder.Append("/");
    builder.Append(word.ToUpperInvariant());
}
Console.WriteLine(builder.ToString());
Console.WriteLine("FILE".Equals("file", StringComparison.OrdinalIgnoreCase));
```

### 결과 확인

```text
APPLE/BANANA
True
```

각 조각의 앞뒤 공백을 제거하고 빈 항목은 버립니다. `|`는 여기서 두 열거형 옵션을 조합합니다.

### 자주 하는 실수

`Trim`은 문자열 내부의 모든 공백을 지우지 않습니다. `Substring`의 두 번째 인수는 끝 위치가 아니라 길이입니다. `Contains("@")`만으로 이메일 주소 전체의 유효성을 보장할 수는 없습니다.

### 직접 해보기

쉼표로 구분한 한 줄을 읽고 앞뒤 공백과 빈 항목을 제거한 뒤 영문을 대문자로 바꾸어 `/`로 연결하세요. 모든 항목이 비면 `없음`을 출력합니다.

### 힌트와 해설

예제의 `Split` 옵션을 사용합니다. 결과 길이가 0인지 먼저 판단하세요. 입력 ` a,, b `의 출력은 `A/B`입니다.

