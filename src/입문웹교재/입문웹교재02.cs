using System;

string name = "민수";
int level = 1;
double speed = 2.5;
bool isReady = true;
char grade = 'A';
level = level + 1;
Console.WriteLine($"{name}: 레벨 {level}, 속도 {speed}");
Console.WriteLine($"준비: {isReady}, 등급: {grade}");

int health = 100;
int damage = 25;
int currentHealth = health - damage;
Console.WriteLine(currentHealth);