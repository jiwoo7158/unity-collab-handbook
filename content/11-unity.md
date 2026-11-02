# 11. Unity 연결 기술: MonoBehaviour, ScriptableObject, RequireComponent

## 1. 일반 C# 객체와 MonoBehaviour의 차이

```csharp
var model = new HealthModel(100); // 일반 C# 객체: new 가능
```

```csharp
var go = new GameObject("HUD");
var view = go.AddComponent<HealthOverlay>(); // Unity 컴포넌트 생성
```

`HealthModel`은 Unity `GameObject`가 필요 없는 순수 로직이다. `HealthOverlay`는 `MonoBehaviour`이므로 Unity가 GameObject를 통해 생명주기를 관리한다. `new HealthOverlay()`로 생성하지 않는다.

## 2. [SerializeField]는 에디터 데이터 연결

**실제 파일: `Assets/_Game/Integration/DemoBootstrap.cs` 일부**

```csharp
[SerializeField] private HealthOverlay overlay;
[SerializeField] private CombatSettings settings;
```

두 값은 **DemoBootstrap 컴포넌트 인스턴스의 private 필드**다. Inspector에서 참조를 할당할 수 있지만 다른 클래스가 직접 `bootstrap.overlay`라고 접근할 수는 없다. 이 필드들은 static 변수가 아니다.

## 3. [RequireComponent]는 컴포넌트 구성 보조

**실제 파일: `Assets/_Game/Gameplay/RequireComponentExample.cs`**

```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public sealed class RequireComponentExample : MonoBehaviour
{
    private Rigidbody body;

    private void Awake()
    {
        body = GetComponent<Rigidbody>();
    }
}
```

위 코드 블록에서는 namespace를 생략했다. 원본 파일에는 `Game.Collab.Gameplay`이 들어 있다. `RequireComponentExample`을 GameObject에 추가하면 필요한 `Rigidbody`가 없다면 추가되도록 한다. 다만 **이미 붙은 컴포넌트에 나중에 attribute를 추가한 경우를 소급해서 자동 복구하지 않는다.** `body` 필드를 자동 할당하는 기능도 아니다. 여전히 `GetComponent`가 필요하다.

## 4. ScriptableObject는 설정 데이터를 에셋으로 분리

**실제 파일: `Assets/_Game/Gameplay/CombatSettings.cs`**

```csharp
using UnityEngine;

namespace Game.Collab.Gameplay
{
    [CreateAssetMenu(menuName = "Collab Lab/Combat Settings")]
    public sealed class CombatSettings : ScriptableObject
    {
        [SerializeField, Min(1)] private int initialHp = 100;
        [SerializeField, Min(1)] private int attackDamage = 15;
        public int InitialHp => initialHp;
        public int AttackDamage => attackDamage;
    }
}
```

**생성 방법:** Unity Project 창 → `Create > Collab Lab > Combat Settings` → `CombatSettings.asset` 생성 → 씬의 `CombatBootstrap` 컴포넌트 `Settings` 슬롯에 할당. 설정 파일은 C# 소스가 아니라 에디터 에셋이다.

`initialHp`는 ScriptableObject **에셋 인스턴스의 직렬화된 필드**다. `static` 전역 변수가 아니다. 여러 컴포넌트가 **같은 에셋을 참조할 수 있지만**, 이는 같은 에셋 객체를 공유하는 것과 같다. 런타임 중 원본 설정을 수정하는 설계는 에디터/빌드 환경 차이에 주의하자.

## 5. 생명주기와 연결 시점

```text
씬 로드
  ↓
Awake: 일반 C# 로직 객체 생성
  ↓
OnEnable: UI 이벤트 구독 가능(소스가 연결된 경우)
  ↓
Start: 조립자가 UI.Bind(health) 호출
  ↓
OnGUI: 버튼 클릭 → AttackService.Attack → HealthChanged
  ↓
OnDisable / OnDestroy: UI 구독 해제
```

`Awake()`와 `Start()`의 실행 순서는 다른 GameObject끼리의 정확한 호출 순서를 임의로 가정하면 안 된다. 이 예제에서는 `DemoBootstrap.Awake()`에서 로직을 만들고 자신의 `Start()`에서 UI에 `Bind()`를 호출해 순서를 명시했다.

## 6. 씬 연결 vs 코드 연결 vs asmdef 연결

| 연결 | 실제 작업 |
| --- | --- |
| 컴파일 참조 | `Game.Collab.Integration.asmdef`에 `Game.Collab.UI` 추가 |
| Inspector 참조 | `DemoBootstrap.overlay`에 HealthOverlay 컴포넌트 할당 |
| 실행 중 인터페이스 참조 | `overlay.Bind(health)` 호출 |
| Event 구독 | `source.HealthChanged += OnHealthChanged` |

서로 다른 네 가지를 모두 거쳐야 하나의 UI 체력 갱신 흐름이 완성된다.

## 7. 팀 협업 시 에셋 소유권

UI 담당자는 `HealthOverlay.cs`와 UI 프리팹을, Gameplay 담당자는 `HealthModel.cs`를 소유한다. 씬 통합 담당자는 DemoBootstrap과 최종 씬 참조를 담당한다. 모두가 같은 씬을 동시에 수정하는 대신 프리팹별로 작업하고 통합 씬을 관리하는 편이 충돌을 줄인다.
