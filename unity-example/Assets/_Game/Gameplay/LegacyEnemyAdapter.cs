using System;
using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    public sealed class LegacyEnemyAdapter : IDamageable
    {
        private readonly LegacyHitPoints legacy;

        public LegacyEnemyAdapter(LegacyHitPoints legacy)
        {
            this.legacy = legacy ?? throw new ArgumentNullException(nameof(legacy));
        }

        public void TakeDamage(DamageRequest request)
        {
            legacy.LoseHp(request.Amount);
        }
    }
}
