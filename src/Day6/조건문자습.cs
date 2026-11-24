using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Todo
{
    internal class FileName
    {
        static void Main()
        {
            int age = int.Parse(Console.ReadLine());

            if (age >= 13 && age <= 19)
            {
                Console.WriteLine("정상");
            }
            else
            {
                Console.WriteLine("비정상");
            }
        }
    }
}
