namespace Game.Collab.Contracts
{
    public readonly struct HealthSnapshot
    {
        public int Current { get; }
        public int Maximum { get; }

        public HealthSnapshot(int current, int maximum)
        {
            Current = current;
            Maximum = maximum;
        }
    }
}
