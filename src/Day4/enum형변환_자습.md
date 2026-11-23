# 트러블슈팅: enum switch 오류

---

## 문제상황

enum을 switch문에 사용하려고 하는데 `CS0119` 오류가 떴다.

## 문제요약

enum을 switch문에 적용하는 법을 몰랐음

---

```csharp
        enum Choice { ROCK, SCISSORS, PAPER }
        enum AttackStyle { ROCK, SCISSORS, PAPER }
```

```csharp
switch (Choice);
{
case Todo.Choice.ROCK:
break;
case Todo.Choice.SCISSORS:
break;
case Todo.Choice.PAPER:
break;
default:
break;
}
```

swith (Choice); 부분에서 <u>CS0119</u> 오류가 발생했다.

사실 enum의 개념을 모르고 오늘 따라 적어보기만 했는데

이 김에 오늘 한 번 해결을 해보려고 한다.

---

## <u>CS0119??</u> 무엇이었나?

아예 다른 타입을 넣었을 경우인 것 같다.

나의 문제 같은 경우에는 switch()에는 변수가 들어가야 하는데 타입 자체를 넣는 경우였다.

즉 Choice는 enum Choice { ROCK, SCISSORS, PAPER };에서 열거되어있는 3가지 자체를 가리키는

하나의 타입 그 자체로 정의되어 있는 것 같다.

---

**1차 추론 : 그렇다면 Choice라는 타입을 가리키는 변수를 하나 만들어서 넣으면 되지않을까?**

---

## 1차 수정

**enum 자료형을 변수로 바꿔보았다.**

```csharp
Choice choiceTransion = Todo.Choice.ROCK;

switch (choiceTransion)
{
    case Todo.Choice.ROCK:
        break;
    case Todo.Choice.SCISSORS:
        break;
    case Todo.Choice.PAPER:
        break;
    default:
        break;
}
```

그랬더니 <u>CS0119</u> 오류가 사라졌다.

하지만 바꾼 변수 choiceTransion은 ROCK이라는 0의 값 하나만

가리키고 있기 때문에 이 변수 하나로 나머지 SCISSORS와 PAPER와 절대로 매칭될 수 없었다.

---

## **이제는 단순히 <u>CS0119</u>를 없애는게 아니라 진짜비교하고 맞으면 출력하게 하는 코드를 만들고 싶었다.**

---

**2차 추론 : 그렇다면 열거형 변수 안에다가 총 3개의 값을 대입시키면 될 것 같다.**

---

# 구상

- 입력으로 0, 1, 2를 받아와서 그 값을 열거형 변수에다 대입시킨다.
- 열거형이 정수가 될 수는 없으므로 형변환이 필요하다 그렇지 않으면 <u>CS0119</u>오류가 다시 뜰 것 같다.
- 형변환된 변수로 switch문에서 int값에 대한 ROCK, SCISSORS, PAPER를 출력시킨다.

명시적 형변환(explicit casting)

---

## 2차 수정

**추가한 코드들**

```csharp
int choice = int.Parse(Console.ReadLine());
Choice choiceEnum = (Choice)choice;

switch(choiceEnum)
{
    case Choice.ROCK:
        Console.WriteLine("주먹을 냈습니다.");
        break;
    case Choice.SCISSORS:
        Console.WriteLine("가위를 냈습니다.");
        break;
    case Choice.PAPER:
        Console.WriteLine("보를 냈습니다.");
        break;
    default:
        Console.WriteLine("잘못된 입력을 받았습니다.");
        break;
}
```

---

# 수정 완료

Console.ReadLine으로 정수 입력을 받아서

enum의 자료형을 int로 형변환 시키고

switch의 인자로 넣었다.

해당 정수 값에 따라서 주먹, 가위, 보를 출력되었다.

(Choice)choice의 의미

---

**배운점 : enum을 다른 곳에서 사용할 때는 직접 불러오거나 혹은 변수를 만들고 초기화 혹은 입력받아 사용할 수 있었는데**

1. 직접 불러오는 것은 1:1 비교가 가능하다 즉, choice == (int)Todo.Choice.ROCK 처럼이다.

## 코드 예시

```csharp
if (choice == (int)Todo.Choice.ROCK)
{
   Console.WriteLine("주먹을 냈습니다.");
}
```

1. 변수를 만들고 초기화 혹은 입력받아 사용하면 다른 변수의 값이랑 비교가 가능하다.

## 코드 예시

```csharp
Choice choiceEnum = (Choice)choice;
switch(choiceEnum)
{
    case Choice.ROCK:
        Console.WriteLine("주먹을 냈습니다.");
        break;
    case Choice.SCISSORS:
        Console.WriteLine("가위를 냈습니다.");
        break;
    case Choice.PAPER:
        Console.WriteLine("보를 냈습니다.");
        break;
    default:
        Console.WriteLine("잘못된 입력을 받았습니다.");
        break;
}
```

---

## 전체 코드 비교

- 수정 전 코드
    
    ```csharp
    using System;
    using Todo;
    // 분기문
    // 코드를 원하는 부분만 실행하겠다.
    
    /*
     *  if( 조건문)
     *  {(body)
     *  
     *  }
     * 
     */
    
    // 무엇이 조건이냐 True / False
    
    // 보유돈, 강화할 때 필요한 돈
    
    int wallet = 500;
    int cost = 500;
    
    bool condition = wallet >= cost;
    if (condition)
    {
        Console.WriteLine("강화를 합니다.");
    }
    
    else
    {
        Console.WriteLine("돈이 부족합니다.");
    }
    
    int choice = int.Parse(Console.ReadLine()); // 1약속> 주먹 2가위 3보
    
    //const int ROCK = 1;
    //const int SCISSORS = 2;
    //const int PAPER = 3;
    
    Random rand = new Random();
    
    int otherChoice = rand.Next(1, 4);
    Console.WriteLine(otherChoice);
    
    //if (choice == (int)Todo.Choice.ROCK)
    //{
    
    //    Console.WriteLine("주먹을 냈습니다.");
    //}
    //else if (choice == (int)Todo.AttackStyle.SCISSORS)
    //{
    //    Console.WriteLine("가위를 냈습니다");
    //}
    //else if (choice == (int)Todo.Choice.PAPER)
    //{
    //    Console.WriteLine("보를 냈습니다.");
    //}
    //else
    //{
    //    Console.WriteLine("잘못된 입력을 받았습니다.");
    //}
    
    Choice choiceTransion = Todo.Choice.ROCK;
    
    switch (choiceTransion)
    {
        case Todo.Choice.ROCK:
            break;
        case Todo.Choice.SCISSORS:
            break;
        case Todo.Choice.PAPER:
            break;
        default:
            break;
    }
    ```
    

- 수정 후 코드
    
    ```csharp
    using System;
    using Todo;
    
    Console.WriteLine("가위바위보 게임을 시작합니다.");
    Console.WriteLine("1.주먹 2.가위 3.보");
    int choice = int.Parse(Console.ReadLine());
    
    choice = choice - 1; // 0,1,2로 변환
    
    Choice choiceEnum = (Choice)choice;
    switch(choiceEnum)
    {
        case Choice.ROCK:
            Console.WriteLine("주먹을 냈습니다.");
            break;
        case Choice.SCISSORS:
            Console.WriteLine("가위를 냈습니다.");
            break;
        case Choice.PAPER:
            Console.WriteLine("보를 냈습니다.");
            break;
        default:
            Console.WriteLine("잘못된 입력을 받았습니다.");
            break;
    }
    ```