using UnityEngine;
using Game.Collab.Contracts;
using Game.Collab.Gameplay;
using Game.Collab.UI;

namespace Game.Collab.Integration
{
    // 여러 어셈블리의 실제 객체를 연결하는 Composition Root.
    public sealed class DemoBootstrap : MonoBehaviour
    {
        [SerializeField] private HealthOverlay overlay;
        [SerializeField] private CombatSettings settings; // 선택: null이면 기본값 사용

        private HealthModel health;
        private AttackService attacks;

        public int CurrentHp => health == null ? -1 : health.Snapshot.Current;

        public void SetOverlay(HealthOverlay value)
        {
            overlay = value;
            if (overlay != null && health != null)
                overlay.Bind(health);
        }

        private void Awake()
        {
            int maxHp = settings == null ? 100 : settings.InitialHp;
            health = new HealthModel(maxHp);
            attacks = new AttackService(health, new FlatDamageModifier(0), LogAttack);
        }

        private void Start()
        {
            if (overlay == null)
                Debug.LogWarning("HealthOverlay reference is missing", this);
            else
                overlay.Bind(health);
        }

        public void TestAttack(int damage)
        {
            attacks.Attack(damage);
        }

        private void LogAttack(DamageRequest request)
        {
            Debug.Log($"Attack: {request.SourceId}, damage={request.Amount}", this);
        }

        private void OnGUI()
        {
            int damage = settings == null ? 15 : settings.AttackDamage;
            if (GUI.Button(new Rect(16, 96, 315, 40), $"Attack enemy (-{damage} HP)"))
                TestAttack(damage);
        }
    }
}
