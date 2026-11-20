# 11. Exception — 실패 처리와 자원 정리

## 실패를 호출한 쪽에 전달하기

파일을 읽는데 파일이 없거나, 허용되지 않는 값으로 작업을 요청할 수 있습니다. **예외는 작업을 정상적으로 완료할 수 없음을 호출 흐름으로 전달하는 방법**입니다. 모든 오류가 예외는 아닙니다. 컴파일 오류는 실행 전에 수정해야 하고, 잘못된 계산 결과 같은 논리 오류는 예외 없이도 생깁니다.

`throw`로 예외를 발생시키면 현재 작업의 정상 흐름을 중단하고, 호출 경로에서 일치하는 `catch`를 찾습니다. 처리 가능한 경계에서 문제를 알리거나 복구할 수 있습니다. 아무 곳에서나 잡아 무시하면 실패한 상태를 정상으로 오해할 수 있습니다.

## 역할 구분

| 문법 | 역할 |
| --- | --- |
| `try` | 예외가 발생할 수 있고 여기서 처리할 작업 범위 |
| `catch` | 지정한 종류의 예외 처리 |
| `finally` | 정상 완료나 예외 전파 시 실행할 정리 |
| `throw new ...` | 새 예외 발생 |
| `throw;` | catch 안에서 원래 예외 다시 전달 |
| `using` | `IDisposable` 자원을 범위 종료 시 정리 |

`finally`는 일반적인 제어 흐름을 벗어날 때 정리를 보장하는 구조입니다. 프로세스 강제 종료 같은 상황까지 항상 실행되는 것은 아닙니다. `using` 선언은 C# 8 문법이며 해당 범위가 끝날 때 `Dispose`를 호출합니다. GC의 메모리 회수와 자원 정리는 같은 작업이 아닙니다.

## 실행 예제

```csharp
using System;
using System.IO;

class Program
{
    static void Main()
    {
        try
        {
            using StringReader reader = new StringReader("-1");
            int amount = int.Parse(reader.ReadLine()!);
            ValidateAmount(amount);
            Console.WriteLine("처리 성공");
        }
        catch (ArgumentOutOfRangeException)
        {
            Console.WriteLine("금액 오류");
        }
        finally
        {
            Console.WriteLine("처리 종료");
        }
    }

    static void ValidateAmount(int amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount), "양수여야 합니다.");
    }
}
```

```text
금액 오류
처리 종료
```

`ValidateAmount`가 실패하므로 성공 문장은 실행되지 않습니다. `using`의 자원 정리가 수행되고 해당 예외를 처리하는 `catch`로 이동합니다. 예제의 `!`는 입력 내용을 고정했기 때문에 사용했으며, 임의 입력을 받는 경우에는 null과 변환 실패를 따로 검증해야 합니다.

## 실수 점검과 연습

- 예상 가능한 사용자 숫자 입력 실패는 보통 `TryParse`로 처리합니다. 반복적인 정상 분기를 위해 예외를 만들지 않습니다.
- 더 구체적인 `catch`를 먼저 배치합니다. 무조건적인 `catch (Exception)`으로 모든 문제를 덮지 않습니다.
- 재전달할 때 `throw ex;`는 스택 추적 정보를 바꾸므로 특별한 이유가 없다면 `throw;`를 사용합니다.
- 문자열을 `"10"`으로 바꿔 성공 경로를 확인하세요. `"abc"`로 바꾸면 어떤 종류의 예외가 발생하고 현재 catch가 처리할 수 있는지 확인합니다.
