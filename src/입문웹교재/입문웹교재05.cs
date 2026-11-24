using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Todo
{
    internal class 웹입문서05
    {
        enum Choice { Rock, Scissors, Paper };

        static void Main()
        {
            Console.WriteLine("0, 1, 2 중에 고르시오");
            int choice = int.Parse(Console.ReadLine() ?? "");

            Choice choiceInput = (Choice)choice;

            switch (choiceInput)
            {
                case Choice.Rock:
                    Console.WriteLine($"낸 것은 {(Choice)choice}입니다.");
                    break;
                case Choice.Scissors:
                    Console.WriteLine($"낸 것은 {(Choice)choice}입니다.");
                    break;
                case Choice.Paper:
                    Console.WriteLine($"낸 것은 {(Choice)choice}입니다.");
                    break;
                default:
                    Console.WriteLine("올바른 값을 입력하지 않았습니다");
                    break;
            }
        }
    }
}
