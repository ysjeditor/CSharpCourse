using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Todo
{
    internal class 입문웹교재08
    {
        static void Main()
        {
            int input = int.Parse(Console.ReadLine());
            Console.WriteLine(Output(input));

            static bool Output(int input)
            {
                return input >= 60;
            }
        }
    }
}
