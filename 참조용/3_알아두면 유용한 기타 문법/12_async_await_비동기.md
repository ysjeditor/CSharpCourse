# 12. async·await — 비동기 작업의 완료 기다리기

## 기다리는 작업과 실행 스레드 구분하기

통신이나 파일 접근처럼 완료까지 시간이 걸리는 작업이 있습니다. 호출 스레드를 붙잡고 기다리기보다 **작업이 끝난 뒤 나머지 처리를 이어가도록** 표현하는 것이 비동기 프로그래밍의 중요한 목적입니다.

`Task`는 완료될 작업을, `Task<T>`는 완료 후 `T` 결과를 받을 작업을 나타냅니다. `async` 메서드의 `await`는 아직 끝나지 않은 작업을 만나면 호출 흐름을 양보하고, 완료 후 이어서 처리할 수 있게 합니다. 이미 완료한 작업이라면 중단 없이 계속할 수도 있습니다.

**async를 붙였다고 작업이 새 스레드에서 실행되지는 않습니다.** 완료 후 실행 위치는 동기화 컨텍스트와 await 대상 등에 영향을 받습니다. 여기서는 특정 UI나 엔진의 실행 컨텍스트 대신 순차적인 일반 콘솔 예제로 원리를 배웁니다.

## 실행 예제

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        using CancellationTokenSource source = new CancellationTokenSource();
        int result = await LoadNumberAsync(source.Token);
        Console.WriteLine(result);

        source.Cancel();
        try
        {
            await LoadNumberAsync(source.Token);
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("취소됨");
        }
    }

    static async Task<int> LoadNumberAsync(CancellationToken token)
    {
        await Task.Delay(10, token);
        return 42;
    }
}
```

```text
42
취소됨
```

첫 호출은 대기를 마친 후 42를 반환합니다. 두 번째 호출은 이미 취소된 토큰을 전달했으므로 `await`에서 취소 예외를 처리합니다. 취소는 강제로 스레드를 죽이는 기능이 아니라 **작업이 요청을 받아 협력적으로 중단하는 방식**입니다.

## 함께 배울 내용

| 주제 | 학습할 이유 |
| --- | --- |
| `Task.WhenAll` | 여러 작업이 완료되기를 기다림. 병렬 스레드 실행을 자동 보장하지 않음 |
| 취소 토큰 전달 | 하위 작업까지 취소 요청 전달 |
| await의 예외 전파 | 실패를 호출한 쪽에서 처리 |
| 작업 참조 유지 | 시작만 하고 실패를 관찰하지 않는 문제 방지 |
| `IDisposable` 정리 | 취소 토큰 소스 등 자원 수명 관리 |

## 실수 점검과 연습

- 일반적인 비동기 메서드는 `async void`보다 `Task` 또는 `Task<T>`로 반환합니다. 호출자가 완료와 실패를 기다릴 수 있어야 합니다.
- `.Result`나 `.Wait()`는 동기적으로 막기 때문에 UI 정지나 교착 문제를 만들 수 있습니다. 가능한 호출 흐름 전체를 await로 연결합니다.
- 모든 메서드에 `async`를 붙이지 않습니다. 단순히 다른 작업을 전달할 뿐이면 Task를 그대로 반환할 수도 있습니다.
- `Task.WhenAll`로 두 작업을 기다리는 예제로 확장하세요. 출력 순서를 보장하려면 출력하는 시점도 함께 설계해야 합니다.
