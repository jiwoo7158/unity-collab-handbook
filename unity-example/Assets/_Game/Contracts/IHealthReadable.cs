using System;

namespace Game.Collab.Contracts
{
    public interface IHealthReadable
    {
        HealthSnapshot Snapshot { get; }
        event Action<HealthSnapshot> HealthChanged;
    }
}
