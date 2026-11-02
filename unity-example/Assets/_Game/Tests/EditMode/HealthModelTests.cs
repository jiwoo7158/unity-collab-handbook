using NUnit.Framework;
using Game.Collab.Contracts;
using Game.Collab.Gameplay;

namespace Game.Collab.Tests.EditMode
{
    public class HealthModelTests
    {
        [Test]
        public void TakeDamage_ReducesHpAndNotifies()
        {
            var health = new HealthModel(100);
            int notifications = 0; // 테스트 메서드 지역 변수
            HealthSnapshot last = default;
            health.HealthChanged += snapshot =>
            {
                notifications++;
                last = snapshot;
            };

            health.TakeDamage(new DamageRequest(15, "Test"));

            Assert.That(health.Snapshot.Current, Is.EqualTo(85));
            Assert.That(last.Current, Is.EqualTo(85));
            Assert.That(notifications, Is.EqualTo(1));
        }

        [Test]
        public void TakeDamage_DoesNotGoBelowZero()
        {
            var health = new HealthModel(30);
            health.TakeDamage(new DamageRequest(50, "Test"));
            Assert.That(health.Snapshot.Current, Is.EqualTo(0));
        }

        [Test]
        public void Adapter_ConnectsLegacyCode()
        {
            var legacy = new LegacyHitPoints(50);
            IDamageable adapter = new LegacyEnemyAdapter(legacy);
            adapter.TakeDamage(new DamageRequest(15, "Test"));
            Assert.That(legacy.Hp, Is.EqualTo(35));
        }

        [Test]
        public void Facade_OffersSimplePublicAPI()
        {
            var facade = new CombatFacade(80);
            facade.PlayerAttack(10);
            Assert.That(facade.Health.Snapshot.Current, Is.EqualTo(70));
        }
    }
}
