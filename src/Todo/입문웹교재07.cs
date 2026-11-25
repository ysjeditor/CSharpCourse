using System;
using System.Diagnostics.CodeAnalysis;

public class Class1
{
    static void Main()
    {
        // foreach문을 통해 float 10, 20, 30을 대입
        // while문을 통해 50이 될때까지 반복
        // 배열 길이로 평균값을 나누고 그 값을 출력

        int[] scores = { 10, 20, 30 };
        int[] scores2 = new int[] { 1, 2, 3 };
        int result = 0;

        Console.WriteLine(scores[1]);
        Console.WriteLine(scores2[1]);

        //while (result < 29)
        //{
        //    for(int i = 0; i <scores.Length; ++i)
        //    {
        //        result += scores[i];
        //    }
        //    result = result / scores.Length;
        //    Console.WriteLine($"평균값 : {result}");
        //}

        foreach (int value in scores2)
        {
            {
                Console.WriteLine($"value : {value}");
            }
        }
    }
}
