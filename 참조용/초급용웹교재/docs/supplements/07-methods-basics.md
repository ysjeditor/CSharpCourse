# 7장. 메서드 기초

### 학습 목표

매개변수 전달, 반환, 오버로딩과 선택적 인수를 구분합니다.

### 개념 읽기

#### 기본 구조 — 정의·호출·반환

```csharp
int result = Calculator.Add(10, 20); // 형식이름.메서드이름(인수들)
Console.WriteLine(result);           // 반환받은 값을 호출자가 사용
int value = 3;
Calculator.Increase(ref value);     // 호출자 변수 자체를 바꾸도록 전달
bool success = int.TryParse("42", out int number); // out으로 결과 받기
Calculator.Print(text: "안녕");      // 명명된 인수, times는 기본값 1

static class Calculator
{
    // 접근제한자 static 반환형 메서드이름(매개변수 목록)
    public static int Add(int left, int right)
    {
        return left + right;        // 결과를 반환하며 이 호출 종료
    }
    public static double Add(double left, double right) // 형식이 다른 오버로드
        => left + right;
    public static void Increase(ref int target) // 반환값이 없으므로 void
    {
        target++;                   // 호출자의 변수 값 증가
    }
    public static void Print(string text, int times = 1) // 선택적 매개변수
    {
        for (int i = 0; i < times; i++) Console.WriteLine(text);
    }
}
```

#### 입력과 출력을 계약으로 만들기

가격 계산을 여러 곳에서 반복한다면 계산 부분을 함수로 묶습니다. 호출할 때 전달하는 값은 **인수**, 선언에서 받는 변수는 **매개변수**입니다. 반환형은 호출한 쪽이 받을 결과의 형식이고 `void`는 반환값이 없다는 뜻입니다. 화면에 출력하는 것과 값을 반환하는 것은 서로 다른 동작입니다.

최상위 문 안에 선언한 함수는 지역 함수입니다. 클래스 안에 선언하면 메서드입니다. 예제에서는 클래스의 정적 메서드를 사용하므로 `Calculator.Total(...)`처럼 형식 이름으로 호출합니다. `static` 지역 함수는 바깥 지역 변수를 캡처하지 않습니다.

#### 기본 전달은 값 복사

정수 매개변수를 바꿔도 호출자의 정수 변수가 바뀌지 않습니다. 배열이나 클래스도 기본적으로 **참조 값이 복사되어 전달**됩니다. 복사한 참조로 같은 객체의 상태는 수정할 수 있지만 매개변수에 새 객체를 대입하는 것만으로 호출자의 변수가 교체되지는 않습니다.

`ref`는 호출자의 변수 저장 위치를 전달하고 호출 전에 초기화가 필요합니다. `out`은 메서드가 값을 설정해 돌려주는 자리이며 메서드의 정상 반환 전에 대입해야 합니다. `TryParse`가 대표적인 `out` 사용 예입니다. 호출하는 쪽에도 해당 키워드를 적습니다.

#### 같은 이름과 다른 인수

오버로딩은 같은 이름에 매개변수의 개수나 형식 등을 다르게 정의하는 것입니다. 반환형만 다르게 하여 구분할 수는 없습니다. 지역 함수끼리는 같은 범위에서 이름을 중복해 오버로딩하지 않으므로 이 연습은 클래스 메서드로 합니다.

선택적 매개변수는 기본값을 가지며 필수 매개변수 뒤에 놓습니다. 명명된 인수는 `quantity: 3`처럼 의미를 드러냅니다. 과도한 선택적 인수로 함수의 역할이 모호해지지 않도록 합니다.

### 따라 하기

```csharp
using System;

Console.WriteLine(Calculator.Total(100));
Console.WriteLine(Calculator.Total(price: 100, quantity: 3));
Console.WriteLine(Calculator.Total(1.5, 2));

static class Calculator
{
    public static int Total(int price, int quantity = 1)
        => price * quantity;
    public static double Total(double price, int quantity)
        => price * quantity;
}
```

### 결과 확인

```text
100
300
3
```

마지막 줄은 소수 리터럴 때문에 `double` 매개변수를 받는 오버로드가 선택됩니다.

### 자주 하는 실수

반환형이 `int`이면 정상적으로 끝나는 각 경로에서 정수를 반환해야 합니다. `ref`가 없어도 객체 내부를 바꿀 수 있다는 사실과 호출자 변수 자체를 바꾸는 일을 구분합니다.

### 직접 해보기

가격과 수량을 두 줄로 입력받아 `Total` 메서드로 곱을 반환하고 출력하세요. 테스트의 각 입력은 0~10000의 정수입니다. 추가로 `Swap(ref int a, ref int b)`를 작성해 두 변수의 교환 전후를 확인하세요.

### 힌트와 해설

`static int Total(int price, int quantity)` 안에서 곱을 반환하고 호출자가 출력합니다. Swap에서는 임시 변수에 a를 저장하고 a에 b를 넣은 뒤 b에 임시 값을 넣습니다.

