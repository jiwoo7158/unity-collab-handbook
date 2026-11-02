using System;
using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    // 다른 효과 계산기로 바꿀 수 있는 DI용 구현체.
    public sealed class FlatDamageModifier : IDamageModifier
    {
        private readonly int bonus;

        public FlatDamageModifier(int bonus)
        {
            this.bonus = bonus;
        }

        public int Modify(int rawAmount)
        {
            return Math.Max(0, rawAmount + bonus);
        }
    }
}
