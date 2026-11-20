# 02. Interface — 구현과 사용 사이의 계약

## 구체적인 클래스 이름보다 할 수 있는 일에 의존하기

보고서를 보내는 프로그램을 만든다고 생각해봅시다. 화면에 출력할 때도 있고 파일에 저장할 때도 있습니다. 보고서를 만드는 코드가 각각의 출력 클래스 내부까지 알면, 출력 방식이 바뀔 때마다 수정해야 합니다.

**인터페이스는 어떤 기능을 제공하는지 정하는 계약**입니다. `IMessageWriter`에 `Write(string message)`를 선언하면 사용 코드는 그 기능이 있다는 전제로 호출합니다. 구현 클래스는 실제 처리 방법을 책임집니다.

## 선언과 구현

인터페이스 이름은 관례적으로 `I`로 시작합니다. `class ConsoleWriter : IMessageWriter`에서 콜론은 이 클래스가 계약을 구현한다는 의미입니다. 일반적인 암묵적 구현 메서드는 `public`이어야 하고 이름·매개변수·반환형이 계약과 일치해야 합니다.

클래스는 여러 인터페이스를 구현할 수 있지만 여러 클래스를 상속할 수는 없습니다. 인터페이스는 객체를 생성하는 설계도가 아니므로 `new IMessageWriter()`로 직접 만들 수 없습니다.

## 실행 예제

```csharp
using System;

class Program
{
    static void Main()
    {
        IMessageWriter writer = new ConsoleWriter();
        PrintReport(writer);
    }

    static void PrintReport(IMessageWriter writer)
    {
        writer.Write("보고서 완료");
    }
}

interface IMessageWriter
{
    void Write(string message);
}

class ConsoleWriter : IMessageWriter
{
    public void Write(string message)
    {
        Console.WriteLine(message);
    }
}
```

```text
보고서 완료
```

`writer`의 선언형은 인터페이스이고 실제 객체는 `ConsoleWriter`입니다. 호출 시 실제 구현이 실행됩니다. 같은 인터페이스를 구현한 다른 클래스를 전달해도 `PrintReport`의 코드는 유지할 수 있습니다. 이것이 다형성을 활용하는 한 방법입니다.

## 상속·추상 클래스와의 비교

| 선택 | 주요 목적 | 판단 기준 |
| --- | --- | --- |
| 인터페이스 | 공통으로 제공할 기능의 계약 | 관련 없는 여러 형식에 같은 사용 방법 제공 |
| 추상 클래스 | 공통 상태·구현을 공유하는 기반 | 실제로 같은 계열이며 공유할 구현이 있음 |
| 일반 클래스 | 바로 생성 가능한 구현 | 독립된 상태와 동작을 정의 |

충돌하는 계약이나 공개 범위를 조정할 때는 `void IMessageWriter.Write(string message)`와 같은 **명시적 인터페이스 구현**도 사용할 수 있습니다. 이때 해당 멤버는 인터페이스 참조를 통해 호출하며 일반적인 `public` 구현과 구분합니다.

## 실수 점검과 연습

- 인터페이스로 전달한다고 서로 다른 객체가 자동으로 독립 복제되는 것은 아닙니다.
- 모든 클래스에 습관적으로 인터페이스를 만들기보다 구현 교체나 공통 사용의 필요성을 확인하세요.
- `PrefixWriter`를 추가해 `"[알림] "`을 붙이세요. `PrintReport`는 수정하지 않고 같은 호출로 출력이 바뀌는지 확인합니다.
- 이 과정에서는 구현 없는 전통적인 계약만 사용합니다. 기본 인터페이스 구현과 정적 추상 멤버는 다루지 않습니다.
