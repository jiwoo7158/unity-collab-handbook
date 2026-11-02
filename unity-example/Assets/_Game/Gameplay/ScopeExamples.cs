namespace Game.Collab.Gameplay
{
    public sealed class ScopeExamples
    {
        public const int DefaultMaxHp = 100;       // 컴파일 타임 상수, 타입 소속
        public static int CreatedCount { get; private set; } // 정적 속성, 객체 간 공유
        private int currentHp;                      // 인스턴스 필드, 객체별 독립

        public int CurrentHp => currentHp;         // 공개 읽기 전용 속성

        public ScopeExamples(int initialHp)         // initialHp: 매개변수
        {
            currentHp = initialHp;
            CreatedCount++;
        }

        public void Hurt(int amount)                // amount: 매개변수
        {
            int applied = amount < 0 ? 0 : amount; // applied: 지역 변수
            currentHp -= applied;
            if (currentHp < 0)
            {
                int correction = -currentHp;       // 블록 내부 지역 변수
                currentHp += correction;
            }
            // correction은 여기서 접근 불가.
        }
    }
}
