using System;

namespace Game.Collab.Gameplay
{
    // 일부러 예전 API를 재현: IDamageable을 구현하지 않음.
    public sealed class LegacyHitPoints
    {
        public int Hp { get; private set; }

        public LegacyHitPoints(int hp)
        {
            Hp = Math.Max(0, hp);
        }

        public void LoseHp(int value)
        {
            Hp = Math.Max(0, Hp - Math.Max(0, value));
        }
    }
}
