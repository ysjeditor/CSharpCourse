# 13. Reflection — 실행 중 코드의 정보 읽기

## 자료의 값뿐 아니라 자료형의 구조 확인하기

일반적인 코드에서는 `student.Name`처럼 사용할 멤버를 미리 알고 접근합니다. 반면 문서 생성기나 데이터 점검 도구는 형식에 어떤 프로퍼티가 있는지 실행 중에 조사해야 할 수 있습니다. **리플렉션은 로드된 형식과 멤버의 메타데이터를 조회하고 사용하는 기능**입니다.

`typeof(Student)`는 코드에서 알고 있는 형식의 `Type`을 얻고, `instance.GetType()`은 객체의 실제 런타임 형식을 얻습니다. `Type`을 바탕으로 프로퍼티·필드·메서드·특성을 조회할 수 있습니다. 리플렉션은 형식 정보를 읽는 기능이지, 문자열을 자동으로 안전한 코드로 바꾸는 기능이 아닙니다.

## 특성(Attribute)은 메타데이터입니다

`[Label("표시 이름")]`처럼 선언에 붙이는 특성은 추가 정보를 나타냅니다. 이를 붙였다는 이유만으로 자동으로 화면이 생기지는 않습니다. 리플렉션으로 읽고 처리하는 코드나 도구가 있어야 의미 있는 동작이 연결됩니다.

## 실행 예제

```csharp
using System;
using System.Reflection;

class Program
{
    static void Main()
    {
        Student student = new Student();
        Type type = typeof(Student);
        PropertyInfo? property = type.GetProperty(nameof(Student.Name));
        if (property == null) throw new InvalidOperationException("프로퍼티 없음");

        LabelAttribute? label = property.GetCustomAttribute<LabelAttribute>();
        Console.WriteLine(label?.Text ?? property.Name);
        Console.WriteLine(property.GetValue(student));
    }
}

class Student
{
    [Label("표시 이름")]
    public string Name { get; set; } = "민수";
}

[AttributeUsage(AttributeTargets.Property)]
class LabelAttribute : Attribute
{
    public string Text { get; }
    public LabelAttribute(string text) { Text = text; }
}
```

```text
표시 이름
민수
```

`nameof`로 이름을 얻지만, 조회 결과는 여전히 존재하지 않을 수 있는 계약이므로 null을 확인합니다. `GetValue`는 해당 객체의 프로퍼티 값을 읽습니다. 프로퍼티 getter에 작업이 있다면 단순 조회도 그 작업을 실행할 수 있습니다.

## 주요 API와 적용 판단

| 기능 | 대표 API | 확인할 사항 |
| --- | --- | --- |
| 형식 조회 | `typeof`, `GetType` | 선언형과 실제 형식의 차이 |
| 프로퍼티 조회 | `GetProperty` | 이름, 공개 범위, null 결과 |
| 메서드 조회 | `GetMethod` | 오버로드와 매개변수 형식 |
| 동적 호출 | `MethodInfo.Invoke` | 인수·대상 객체·반환형·호출 예외 |
| 생성 | `Activator.CreateInstance` | 생성자 존재 여부와 접근 가능성 |
| 조회 범위 | `BindingFlags` | public/private, instance/static 구별 |

직접 호출할 수 있는 기능이라면 보통 직접 호출이나 인터페이스를 우선 사용합니다. 리플렉션은 이름·형식 오류를 실행 중에 발견하게 하고 조회·호출 비용을 추가할 수 있습니다. 반복 조회가 필요하다면 메타데이터를 캐시할 수 있지만, 호출 대상의 올바름과 자원 수명도 함께 관리해야 합니다.

## 호환성과 실수 점검

- 리플렉션 조회와 `Reflection.Emit` 같은 런타임 코드 생성은 다릅니다. AOT 환경에서는 코드 생성이나 특정 동적 사용에 제한이 있습니다.
- 코드 제거가 적용되는 빌드에서는 정적 참조가 없는 멤버가 제거될 수 있으므로 실제 배포 환경에서 검증해야 합니다.
- 외부 입력으로 받은 임의의 형식·메서드를 무제한 호출하는 구조를 만들지 않습니다. 허용할 대상과 입력 규칙을 명시합니다.
- `Score` 프로퍼티에 표시 이름 특성을 붙여 두 프로퍼티의 정보를 출력하도록 확장하세요. 조회 순서가 항상 선언 순서라고 가정하지 않습니다.
