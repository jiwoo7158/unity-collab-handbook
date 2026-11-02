using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    // 바깥에는 단순한 API를 제공하는 Facade.
    public sealed class CombatFacade
    {
        private readonly HealthModel health;
        private readonly AttackService attack;

        public IHealthReadable Health => health;

        public CombatFacade(int maximumHp)
        {
            health = new HealthModel(maximumHp);
            attack = new AttackService(health, new FlatDamageModifier(0));
        }

        public void PlayerAttack(int damage)
        {
            attack.Attack(damage);
        }
    }
}
