# 5장. 컬렉션

### 학습 목표

List와 Dictionary를 데이터의 변화·검색 기준에 맞게 사용합니다.

### 개념 읽기

#### 기본 구조 — List와 Dictionary

```csharp
using System.Collections.Generic;

var names = new List<string>();   // List<요소형식> 생성
names.Add("지수");                // 끝에 추가
string first = names[0];         // 0부터 시작하는 위치로 읽기
names.Remove("지수");             // 값이 같은 첫 요소 제거

var students = new Dictionary<int, string>(); // Dictionary<키형식, 값형식>
students.Add(101, "지수");         // 키와 값을 연결, 중복 키는 예외
students[102] = "현우";            // 없으면 추가, 있으면 값 교체
if (students.TryGetValue(101, out string? name)) // 키 존재와 값을 함께 확인
{
    Console.WriteLine(name);
}
foreach (var entry in students)  // 각 항목은 키와 값의 쌍
{
    Console.WriteLine($"{entry.Key}: {entry.Value}");
}
```

#### 개수가 바뀌는 목록

수강생이 등록하거나 취소하면 명단 길이가 바뀝니다. `List<string>`은 문자열 요소를 추가·삭제할 수 있는 목록입니다. `T`는 저장할 형식을 정하는 자리로, `List<int>`는 정수 목록입니다. 형식 매개변수를 사용하는 제네릭은 여러 형식에 같은 자료구조를 재사용하게 합니다.

`Add`는 끝에 추가하고 `Remove`는 처음 일치하는 값을 제거합니다. `RemoveAt`은 인덱스로 제거합니다. 삭제 후 뒤쪽 인덱스가 달라지므로 인덱스를 고유 번호로 쓰지 않습니다. `Contains`, `Find`, `FindAll`로 검색할 수 있습니다. 조건을 받는 메서드에는 뒤에서 배울 람다 식을 넣습니다. 지금은 `x => x >= 60`을 각 x가 60 이상인지 검사하는 함수로 읽으세요.

#### 고유한 키로 찾기

`Dictionary<int, string>`은 학생 번호와 이름을 연결합니다. 키는 중복될 수 없고 서로 다른 키의 값은 같아도 됩니다. `Add`는 중복 키에서 예외가 나며 `TryAdd`는 실패를 `false`로 알려줍니다. 인덱서에 값을 대입하면 기존 키의 값을 바꾸거나 새 키를 추가합니다.

| 작업 | 목록 | 사전 |
| --- | --- | --- |
| 개수 | `Count` | `Count` |
| 조회 기준 | 0부터 시작하는 위치 | 직접 정한 키 |
| 안전한 조회 | 인덱스 범위 확인 | `TryGetValue` |
| 순회 중 값 읽기 | 각 요소 | `Key`, `Value` |

#### 정렬·삭제 시 주의

`List.Sort`는 목록 자체를 정렬합니다. 기본 정렬이 목적과 맞는지 확인하고 필요하면 비교 함수를 지정합니다. `foreach`로 순회하면서 같은 List를 추가·삭제하면 문제가 생깁니다. 조건 삭제에는 `RemoveAll`, 인덱스로 삭제할 때는 뒤에서 앞으로 순회하는 방식 등을 고려합니다. Dictionary의 열거 순서를 업무상의 정렬 규칙으로 삼지 않습니다.

### 따라 하기

```csharp
using System;
using System.Collections.Generic;

var names = new List<string> { "지수", "현우" };
names.Add("민수");
names.Remove("현우");
Console.WriteLine(names.Count);
var students = new Dictionary<int, string> { { 101, "지수" } };
Console.WriteLine(students.TryAdd(101, "민수"));
if (students.TryGetValue(101, out string? name))
    Console.WriteLine(name);
```

### 결과 확인

```text
2
False
지수
```

중복 추가는 거절되며 101번의 기존 값은 바뀌지 않습니다.

### 자주 하는 실수

없는 키를 인덱서로 바로 읽으면 예외가 납니다. `ContainsKey`로 확인할 수도 있지만 값을 함께 읽으려면 `TryGetValue`가 편리합니다. 키의 존재와 값의 존재를 혼동하지 않습니다.

### 직접 해보기

101번은 지수, 102번은 현우입니다. 번호를 한 줄 입력받아 이름을 출력하고, 없는 번호나 문자에는 `없음`을 출력하세요.

### 힌트와 해설

숫자 변환 성공 여부를 먼저 확인하고 `TryGetValue`로 찾습니다. 번호 101·102·999와 문자 abc를 각각 시험합니다.

