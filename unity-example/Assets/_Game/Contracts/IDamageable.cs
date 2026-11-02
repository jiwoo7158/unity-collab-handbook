namespace Game.Collab.Contracts
{
    // 계약: 호출할 수 있는 행위를 정의. 실제 객체가 아님.
    public interface IDamageable
    {
        void TakeDamage(DamageRequest request);
    }
}
