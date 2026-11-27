using System.Numerics;
namespace Todo;
using Todo;

/// <summary>겹친 쌍의 수와, 거리 검사를 몇 번 했는지.</summary>
public readonly record struct CollisionResult(int Overlaps, long Checks);

public static class Collision
{
    /// <summary>모든 쌍을 검사해 겹친 원의 쌍을 센다.</summary>
    /// <remarks>시간 O(n²): 거리 검사 정확히 n(n−1)/2회.
    /// 추가 메모리 O(1), 할당 없음.</remarks>
    public static CollisionResult BruteForce(Vector2[] pos, float radius)
    {
        float hit = 2 * radius;
        int overlaps = 0;
        long checks = 0;
        for (int i = 0; i < pos.Length; i++)
            for (int j = i + 1; j < pos.Length; j++)
            {
                checks++;
                if (Vector2.DistanceSquared(pos[i], pos[j]) < hit * hit)
                    overlaps++;
            }
        return new CollisionResult(overlaps, checks);
    }
    // Grid(pos, radius): 격자에 나눠 담고 이웃 9칸만 검사 (생략)
}

