// Program.cs — 최상위 문(top-level statements)

int[] scores = { 100, 90, 0, 4 };
int[] numbers = new int[5];

int hp = 100;               // 문(statement)은 ;로 끝난다
int damage = 30;
if (damage > 0)
{                           // { } 블록: 여러 문을 하나로
    hp -= damage;
    Console.WriteLine($"HP: {hp}");   // HP: 70
}
/* 여러 줄 주석은 이렇게 감싼다 */