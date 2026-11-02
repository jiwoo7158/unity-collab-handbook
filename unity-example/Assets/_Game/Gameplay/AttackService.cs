using System;
using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    public sealed class AttackService
    {
        private readonly IDamageable target;  // 객체 참조: 외부에서 주입
        private readonly IDamageModifier modifier;
        private readonly Action<DamageRequest> onAttack; // 델리게이트 필드

        public AttackService(
            IDamageable target,
            IDamageModifier modifier,
            Action<DamageRequest> onAttack = null)
        {
            this.target = target ?? throw new ArgumentNullException(nameof(target));
            this.modifier = modifier ?? throw new ArgumentNullException(nameof(modifier));
            this.onAttack = onAttack;
        }

        public void Attack(int rawAmount)
        {
            int modified = modifier.Modify(rawAmount); // 지역 변수
            var request = new DamageRequest(modified, "Player");
            onAttack?.Invoke(request);
            target.TakeDamage(request);
        }
    }
}
