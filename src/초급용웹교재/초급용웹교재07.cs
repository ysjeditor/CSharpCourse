 int a = 1;
 int b = 5;

 Console.WriteLine(a);
 Console.WriteLine(b);

 Swap(ref a, ref b);
 Console.WriteLine(a);
 Console.WriteLine(b);

 Add(4, 10);

 var value = Add2(3, 5);

 Console.WriteLine(value);
 
  static void Swap(ref int a, ref int b)
 {
     int temp = a;
     a = b;
     b = temp;
     Console.WriteLine(a);
     Console.WriteLine(b);
 }

 static void Add(int a1, int a2)
 {
     Console.WriteLine(a1 + a2);
 }

 static int Add2(int a1, int a2)
 {
     return a1 + a2;
 }