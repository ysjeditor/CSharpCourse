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


const int ROCK = 1;
const int SCISSORS = 2;
const int PAPER = 3;

Random rand = new Random();

int otherChoice = rand.Next(1, 4);
Console.WriteLine(otherChoice);

if (choice == (int)Todo.Choice.ROCK)
{
   Console.WriteLine("주먹을 냈습니다.");
}
else if (choice == (int)Todo.AttackStyle.SCISSORS)
{
   Console.WriteLine("가위를 냈습니다");
}
else if (choice == (int)Todo.Choice.PAPER)
{
   Console.WriteLine("보를 냈습니다.");
}
else
{
   Console.WriteLine("잘못된 입력을 받았습니다.");
}

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