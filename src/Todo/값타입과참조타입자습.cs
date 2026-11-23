using System;

class Bag
{
    public string Item;
}

struct PlayerInfo
{
    public int Level;
    public Bag MyBag;
}

class Program
{
    static void Main()
    {
        PlayerInfo original = new PlayerInfo();
        original.Level = 10;
        original.MyBag = new Bag { Item = "빨간 물약" };

        PlayerInfo copy = original;

        copy.Level = 99;          
        copy.MyBag.Item = "빈 병";     

        Console.WriteLine($"원본 레벨: {original.Level}");  
        Console.WriteLine($"복사본 레벨: {copy.Level}");   

        Console.WriteLine($"원본 가방: {original.MyBag.Item}"); 
        Console.WriteLine($"복사본 가방: {copy.MyBag.Item}");    
    }
}
