namespace Game.Collab.Contracts
{
    // 모듈 간 전달하는 값: 로컬 변수도, 전역 변수도 아닌 데이터 타입.
    public readonly struct DamageRequest
    {
        public int Amount { get; }
        public string SourceId { get; }

        public DamageRequest(int amount, string sourceId)
        {
            Amount = amount;
            SourceId = sourceId ?? "unknown";
        }
    }
}
