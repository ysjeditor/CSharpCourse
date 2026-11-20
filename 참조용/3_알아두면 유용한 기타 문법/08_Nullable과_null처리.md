# 08. Nullable과 null 처리

## 값이 없는 상태와 0을 구분하기

시험을 아직 보지 않은 학생과 0점을 받은 학생은 다릅니다. `int?`는 정수 값뿐 아니라 **값 없음인 null**도 표현합니다. 이는 `Nullable<int>`의 축약 표기이며 값 형식의 표현 범위를 확장합니다.

`string?` 같은 **Nullable 참조 형식**은 다른 목적입니다. 참조가 null일 가능성을 컴파일러 분석에 표시합니다. 새로운 문자열 컨테이너를 만드는 것이 아니며, 실행 중 null 검사를 자동으로 삽입하지도 않습니다. 경고의 도움을 받으려면 Nullable 분석을 활성화해야 합니다.

## 실행 예제

```csharp
#nullable enable
using System;

class Program
{
    static void Main()
    {
        int? score = null;
        Console.WriteLine(score.HasValue);
        Console.WriteLine(score ?? -1);
        score = 0;
        Console.WriteLine(score.HasValue);

        string? nickname = null;
        Console.WriteLine(nickname?.Length ?? 0);
        nickname ??= "미등록";
        Console.WriteLine(nickname);
    }
}
```

```text
False
-1
True
0
미등록
```

## 연산자 구분하기

| 표현 | 역할 | 주의점 |
| --- | --- | --- |
| `score.HasValue` | 값 존재 여부 확인 | 0도 값이 있는 상태 |
| `score.Value` | 실제 값 읽기 | 값이 없으면 예외 |
| `value ?? fallback` | null일 때 대체값 사용 | 대체값을 원래 변수에 자동 저장하지 않음 |
| `value?.Member` | null이면 멤버 접근 생략 | 뒤의 일반 접근까지 항상 안전해지는 것은 아님 |
| `value ??= fallback` | null인 경우에만 대입 | 이미 값이 있으면 유지 |
| `value!` | 컴파일러 null 경고 억제 | 실행 중 안전성을 보장하지 않음 |

`!`를 사용해 경고를 없애기 전에 실제로 null일 수 없는 이유를 설명할 수 있어야 합니다. `?.`도 오류를 고치는 대신 필요한 동작을 조용히 생략하는 결과가 될 수 있으므로, null이면 실패해야 하는 계약인지부터 결정합니다.

## 실수 점검과 연습

- `int?`를 `int`로 사용할 때는 값 없음 처리 방법을 정합니다.
- `string?`와 `string`의 차이는 참조 형식에 대한 정적 분석 약속입니다. 경고를 무시하면 null 관련 예외가 여전히 발생합니다.
- 예제의 `score`를 0으로 설정하기 전 `.Value`를 읽으면 어떤 예외가 발생하는지 확인하세요.
- 닉네임이 빈 문자열인 경우도 미등록으로 취급하려면 null 검사 외에 어떤 조건이 필요한지 생각해보세요.
