using System;
using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    // 일반 C# 인스턴스: GameObject에 붙이는 컴포넌트가 아님.
    public sealed class HealthModel : IDamageable, IHealthReadable
    {
        private readonly int maximum;  // 인스턴스 필드, 외부 직접 접근 불가
        private int current;           // 인스턴스 필드, 객체별 독립

        public HealthSnapshot Snapshot => new HealthSnapshot(current, maximum);
        public event Action<HealthSnapshot> HealthChanged;

        public HealthModel(int maximum)
        {
            if (maximum <= 0)
                throw new ArgumentOutOfRangeException(nameof(maximum));

            this.maximum = maximum;
            current = maximum;
        }

        public void TakeDamage(DamageRequest request)
        {
            if (request.Amount <= 0 || current == 0)
                return;

            current = Math.Max(0, current - request.Amount);
            HealthChanged?.Invoke(Snapshot);
        }
    }
}
