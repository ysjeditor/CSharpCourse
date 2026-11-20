# 8장. 고급 메서드 활용

### 학습 목표

람다·델리게이트·확장 메서드·재귀를 작은 기능에 적용합니다.

### 개념 읽기

#### 기본 구조 — 람다·확장 메서드·재귀

```csharp
Func<int, int> twice = x => x * 2;    // 입력 => 반환할 식
Action<string> print = text =>       // 반환값이 없는 동작
{
    Console.WriteLine(text);         // 여러 문장이면 블록 사용
};
print(twice(3).ToString());           // 델리게이트를 함수처럼 호출
Console.WriteLine(60.IsPassed());    // 확장 메서드를 인스턴스 문법으로 호출
Console.WriteLine(Factorial(3));

static long Factorial(int n)         // 이 예시는 0~12 입력을 전제로 함
{
    if (n == 0) return 1;            // 종료 조건
    return n * Factorial(n - 1);     // 더 작은 문제로 재귀 호출
}
static class ScoreExtensions         // 확장 메서드를 담는 정적 클래스
{
    public static bool IsPassed(this int score) // 첫 매개변수가 확장 대상
        => score >= 60;
}
```

#### 동작도 값처럼 전달하기

점수 목록에서 합격자를 고르는 규칙을 바꾸려면 검사 함수를 전달할 수 있습니다. `x => x >= 60`은 정수 x를 받아 논리값을 반환하는 람다 식입니다. `Func<int, bool>`에서 마지막 형식은 반환형이고 앞의 형식들은 입력입니다. `Action<string>`은 문자열을 받고 반환값이 없습니다.

람다는 외부 지역 변수를 캡처할 수 있습니다. 이때 항상 생성 당시의 값이 고정 복사되는 것은 아닙니다. 나중에 변수를 바꾸면 람다가 보는 값도 달라질 수 있으므로 숨은 의존성을 줄이세요.

#### 기존 형식에 호출 문법 더하기

확장 메서드는 정적 클래스 안의 정적 메서드로 정의하고 첫 매개변수에 `this`를 붙이는 문법을 사용할 수 있습니다. `public static bool IsPassed(this int score)`를 정의하면 `score.IsPassed()`로 호출할 수 있습니다. 원래 형식의 소스나 멤버를 실제로 바꾸는 것은 아닙니다. 사용할 네임스페이스가 범위 안에 있어야 합니다.

#### 재귀는 더 작은 문제로 이동하기

팩토리얼은 `n! = n × (n-1)!`로 나눌 수 있습니다. 자기 자신을 호출하는 재귀에는 **종료 조건**과 그 조건에 가까워지는 인수가 필요합니다. 0!은 1입니다. 음수나 너무 큰 값을 허용하면 끝나지 않거나 숫자 범위와 호출 스택의 한계를 만날 수 있습니다. 반복문으로 더 단순하게 표현할 수 있는지도 비교하세요.

### 따라 하기

```csharp
using System;

Func<int, int> twice = x => x * 2;
Action<string> print = text => Console.WriteLine(text);
print(twice(4).ToString());
Console.WriteLine(60.IsPassed());
Console.WriteLine(Factorial(5));

static long Factorial(int n)
{
    if (n == 0) return 1;
    return n * Factorial(n - 1);
}
static class ScoreExtensions
{
    public static bool IsPassed(this int score) => score >= 60;
}
```

### 결과 확인

```text
8
True
120
```

팩토리얼은 5→4→3→2→1→0으로 호출하고, 반환하면서 차례대로 곱합니다.

### 자주 하는 실수

`Func<int, int>`와 `Action<int>`의 반환 유무를 구분하세요. 재귀 함수에 종료 조건만 있고 인수가 줄어들지 않으면 종료되지 않습니다. 확장 메서드가 원래 형식의 private 멤버에 특별히 접근할 권한을 얻는 것도 아닙니다.

### 직접 해보기

0~12의 정수 n을 입력받아 재귀 함수로 n!을 출력하세요. 범위 밖 값과 문자는 `입력오류`입니다. 추가로 60점 이상 판정 람다를 함수의 인수로 전달해보세요.

### 힌트와 해설

입력 검증은 재귀 호출 전에 합니다. n=0이면 1, n=5이면 120입니다. 반환형을 `long`으로 두고 종료 조건에서 1을 반환하세요.

