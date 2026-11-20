# 07. 확장 메서드와 LINQ

## 기존 형식에 편의 기능을 연결하기

확장 메서드는 기존 형식의 소스를 바꾸지 않고 인스턴스 메서드처럼 호출할 수 있는 **정적 메서드**입니다. 정적 클래스의 정적 메서드에서 첫 매개변수에 `this`를 붙입니다. 실제로 기존 클래스에 새 멤버가 저장되는 것은 아니며 private 멤버 접근 권한이 생기지도 않습니다.

LINQ는 컬렉션의 필터링·변환·정렬 같은 데이터 처리를 표현하는 기능입니다. 여기서는 `System.Linq`의 확장 메서드를 사용하는 방식을 배웁니다. LINQ가 곧 데이터베이스라는 뜻은 아닙니다.

| 메서드 | 역할 |
| --- | --- |
| `Where` | 조건에 맞는 요소만 선택 |
| `Select` | 각 요소를 다른 값으로 변환 |
| `OrderBy` | 기준에 따라 정렬 |
| `Any` | 조건에 맞는 요소가 하나라도 있는지 확인 |
| `ToArray`, `ToList` | 그 시점에 열거하고 결과 컨테이너 생성 |

## 실행 예제

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        List<int> scores = new List<int> { 50, 80 };
        var passed = scores.Where(score => score >= 60);
        int[] snapshot = passed.ToArray();
        scores.Add(90);
        Console.WriteLine(string.Join(",", passed));
        Console.WriteLine(string.Join(",", snapshot));
        Console.WriteLine("민수".WithPrefix());
    }
}

static class TextExtensions
{
    public static string WithPrefix(this string text) => "이름: " + text;
}
```

```text
80,90
80
이름: 민수
```

## 지연 실행과 결과 고정

`Where`는 보통 호출 즉시 결과 목록을 만들지 않고, **나중에 열거할 때 원본을 읽습니다**. 따라서 `passed`를 출력할 때 추가된 90도 보입니다. 반면 `snapshot`은 90을 추가하기 전에 `ToArray`로 확정한 결과이므로 80만 들어 있습니다.

참조 형식 요소를 `ToList`로 모았다고 각 객체가 깊은 복사되는 것은 아닙니다. 컨테이너는 새로 만들어져도 요소가 가리키는 객체는 같을 수 있습니다.

## 실수 점검과 연습

- 결과를 여러 번 열거하면 필터 계산도 여러 번 수행될 수 있습니다.
- LINQ가 항상 반복문보다 빠르거나 느리다고 단정하지 말고 호출 빈도와 할당을 측정하세요.
- 원본이 바뀌기 전과 후에 `ToArray`를 호출하여 결과 차이를 설명하세요.
