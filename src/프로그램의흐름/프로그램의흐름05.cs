                Console.WriteLine("시작");
                int health = 100;
                health = health - 25;
                Console.WriteLine(health);
                Console.WriteLine("끝");

                            Console.WriteLine($"전달받은 인자 개수: {args.Length}개");

            for (int i = 0; i < args.Length; i++)
            {
                Console.WriteLine($"args[{i}] = {args[i]}");
            }