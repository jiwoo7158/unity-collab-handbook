using UnityEngine;
using Game.Collab.Contracts;

namespace Game.Collab.UI
{
    public sealed class HealthOverlay : MonoBehaviour
    {
        private IHealthReadable source;  // 인터페이스 타입 인스턴스 필드
        private HealthSnapshot visible;

        public string DisplayText => $"Enemy HP: {visible.Current}/{visible.Maximum}";

        public void Bind(IHealthReadable newSource)
        {
            Unsubscribe();
            source = newSource;
            if (source == null) return;

            visible = source.Snapshot;
            Subscribe();
        }

        private void OnEnable()
        {
            Subscribe();
        }

        private void OnDisable()
        {
            Unsubscribe();
        }

        private void OnDestroy()
        {
            Unsubscribe();
        }

        private void Subscribe()
        {
            if (source == null || !isActiveAndEnabled) return;
            source.HealthChanged -= OnHealthChanged; // 중복 방지
            source.HealthChanged += OnHealthChanged;
        }

        private void Unsubscribe()
        {
            if (source != null)
                source.HealthChanged -= OnHealthChanged;
        }

        private void OnHealthChanged(HealthSnapshot snapshot)
        {
            visible = snapshot;
        }

        private void OnGUI()
        {
            GUI.Box(new Rect(16, 16, 315, 66), DisplayText);
        }
    }
}
