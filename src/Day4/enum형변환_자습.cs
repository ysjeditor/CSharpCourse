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