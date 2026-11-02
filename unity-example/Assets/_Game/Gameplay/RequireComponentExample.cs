using UnityEngine;

namespace Game.Collab.Gameplay
{
    // 선택 학습 예시: 씬 데모에는 필수로 사용되지 않음.
    [RequireComponent(typeof(Rigidbody))]
    public sealed class RequireComponentExample : MonoBehaviour
    {
        private Rigidbody body;

        private void Awake()
        {
            body = GetComponent<Rigidbody>();
        }
    }
}
