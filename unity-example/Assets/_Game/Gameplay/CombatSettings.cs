using UnityEngine;

namespace Game.Collab.Gameplay
{
    // 설정 데이터를 에셋으로 저장. 런타임 객체 생성/로직과 다름.
    [CreateAssetMenu(menuName = "Collab Lab/Combat Settings")]
    public sealed class CombatSettings : ScriptableObject
    {
        [SerializeField, Min(1)] private int initialHp = 100;
        [SerializeField, Min(1)] private int attackDamage = 15;

        public int InitialHp => initialHp;
        public int AttackDamage => attackDamage;
    }
}
