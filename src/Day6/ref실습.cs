namespace Todo
{
    public class PlayerInfo
    {
        public int hp;
        public int mp;
    }

    internal class ref실습
    {
        static void PrintHp(PlayerInfo hp)
        {
            hp.hp = -20;
            hp = new PlayerInfo();
            hp.hp = -1000;
        }

        static void PrintHpRef(ref PlayerInfo hp)
        {
            hp.hp = -20;
            hp = new PlayerInfo();
            hp.hp = -1000;
        }

        static void PrintMp(PlayerInfo mp)
        {
            mp.mp = -20;
            mp = new PlayerInfo();
            mp.mp = -1000;
        }

        static void PrintMpRef(ref PlayerInfo mp)
        {
            mp.mp = -20;
            mp = new PlayerInfo();
            mp.mp = -1000;
        }

        static void Main(string[] args)
        {
            PlayerInfo playerInfo = new PlayerInfo { hp = 1000 };
            playerInfo.mp = 500;
            PrintHp(playerInfo);
            Console.WriteLine($"ref 없이 HP : {playerInfo.hp}");

            PrintHpRef(ref playerInfo);
            Console.WriteLine($"ref 적용 후 HP ref : {playerInfo.hp}");

            PrintMp(playerInfo);
            Console.WriteLine($"ref 없이 MP : {playerInfo.mp}");

            PrintMpRef(ref playerInfo);
            Console.WriteLine($"ref 적용 후mP ref : {playerInfo.mp}");
        }
    }
}
