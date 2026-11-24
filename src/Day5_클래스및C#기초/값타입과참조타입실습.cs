using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Todo
{
    class Bag
    {
        public bool myBag;
    }

    struct PlayerInfo
    {
        public int score;
        public Bag myBag;
    }

    class Enemy
    {
        int score;
        int damage;
    }

    internal class 값타입과참조타입실습
    {
        static void Main(string[] args)
        {
            PlayerInfo playerInfo = new PlayerInfo();
            playerInfo.score = 10;
            playerInfo.myBag = new Bag { myBag = true };
            PlayerInfo copy = playerInfo;
            copy.score = 100;
            copy.myBag.myBag = false;

            Console.WriteLine($"플레이어인포 스코어 : {playerInfo.score}");
            Console.WriteLine($"플레이어인포 마이백 : {playerInfo.myBag.myBag}");
            Console.WriteLine($"카피 스코어 : {copy.score}");
            Console.WriteLine($"카피 마이백 : {copy.myBag.myBag}");
        }
    }

}
