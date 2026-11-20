# 4장. 배열

### 학습 목표

고정 길이 배열을 순회하고 다차원 배열과 가변 배열을 구분합니다.

### 개념 읽기

#### 기본 구조 — 배열의 선언과 접근

```csharp
int[] scores = { 70, 80, 90 };    // 요소로 초기화하는 1차원 배열
int[] emptySlots = new int[3];    // 길이 3, 각 요소의 기본값은 0
scores[0] = 75;                  // 배열이름[인덱스]로 요소 수정
for (int i = 0; i < scores.Length; i++) // 마지막 인덱스는 Length - 1
{
    Console.WriteLine(scores[i]);
}

int[,] board = new int[2, 3];     // 자료형[행, 열]인 직사각형 배열
board[0, 1] = 5;                 // 첫 행, 두 번째 열
int[][] rows = new int[2][];      // 배열을 요소로 갖는 가변 배열
rows[0] = new int[] { 1 };        // 각 행의 배열을 따로 생성
rows[1] = new int[] { 2, 3 };     // 행마다 길이가 달라도 됨
Array.Sort(scores);              // 전달한 배열 자체를 오름차순 정렬
Array.Reverse(scores);           // 현재 요소 순서를 뒤집음
int index = Array.IndexOf(scores, 80); // 없으면 -1
```

#### 개수와 위치를 구분하기

한 반의 점수를 같은 자료형의 배열에 넣으면 하나의 반복문으로 처리할 수 있습니다. `int[] scores = { 70, 80, 90 };`에서 길이는 3이고 마지막 인덱스는 2입니다. `Length`는 마지막 위치가 아닙니다. 배열 요소는 기본값을 받지만, 선언만 한 지역 변수는 사용 전에 대입이 필요합니다.

배열을 만들면 그 객체의 길이는 고정됩니다. 다른 배열을 만들어 변수에 대입할 수는 있지만 기존 배열이 늘어난 것은 아닙니다. 배열 변수 대입은 참조 복사입니다. 두 변수가 같은 배열을 가리킬 때 한쪽의 요소를 수정하면 다른 쪽에서도 보입니다.

#### 두 가지 표 표현

바둑판처럼 행과 열 크기가 일정하면 `int[,] board = new int[2, 3];`을 사용합니다. `board[0, 1]`로 접근하고 행은 `GetLength(0)`, 열은 `GetLength(1)`로 확인합니다. `Length`는 전체 요소 수 6입니다.

행마다 길이가 다르면 `int[][] rows` 같은 **가변 배열**을 사용합니다. 바깥 배열의 각 요소가 별도의 배열 참조이며 `rows[r][c]`로 접근합니다. 안쪽 배열을 만들지 않았다면 해당 요소는 `null`입니다. 한 행의 길이를 다른 행에도 적용하지 마세요.

#### 정렬과 검색의 영향

`Array.Sort`와 `Array.Reverse`는 전달한 배열의 순서를 직접 바꿉니다. 원본 순서가 필요하면 먼저 복사하세요. `Array.IndexOf`는 처음 일치하는 인덱스를 반환하고 없으면 -1을 반환합니다. 검색 결과가 유효한지 검사한 뒤에만 인덱스로 사용합니다.

### 따라 하기

```csharp
using System;

int[] original = { 30, 10, 20 };
int[] sorted = (int[])original.Clone();
Array.Sort(sorted);
Console.WriteLine(string.Join(",", sorted));
Console.WriteLine(string.Join(",", original));
Console.WriteLine(Array.IndexOf(sorted, 99));
int[,] table = { { 1, 2 }, { 3, 4 } };
Console.WriteLine(table.GetLength(0));
int[][] rows = { new[] { 1 }, new[] { 2, 3 } };
Console.WriteLine(rows[1].Length);
```

### 결과 확인

```text
10,20,30
30,10,20
-1
2
2
```

정수 배열을 복제했으므로 정렬해도 원본의 순서는 유지됩니다. 참조 형식 요소를 복제하면 요소가 가리키는 객체까지 깊게 복제되는 것은 아닙니다.

### 자주 하는 실수

최댓값을 0으로 초기화하면 모든 값이 음수인 배열에서 틀립니다. 비어 있지 않은 배열의 첫 값으로 시작하세요. 비어 있는 경우에는 먼저 처리 방침을 정합니다.

### 직접 해보기

세 줄의 정수를 배열에 저장하고 가장 큰 값을 출력하세요. 음수와 같은 값도 허용합니다. 추가로 2차원 배열의 모든 값을 중첩 반복문으로 출력해보세요.

### 힌트와 해설

첫 요소를 `max`로 잡고 나머지 요소가 더 클 때만 갱신합니다. 입력 -8, -2, -5의 답은 -2입니다. 2차원 배열은 각 차원의 `GetLength`를 경계로 씁니다.

