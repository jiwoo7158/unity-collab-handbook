# 10. Assembly Definition / 모듈화: 컴파일 단계에서 경계를 강제하기

## 1. 가장 먼저: 어셈블리란?

Unity는 기본적으로 많은 C# 게임 스크립트를 `Assembly-CSharp.dll` 같은 **하나의 컴파일 단위(어셈블리)** 에 묶는다. Assembly Definition(`.asmdef`)을 만들면 스크립트를 자체 어셈블리로 분리해 **어떤 어셈블리가 어떤 다른 어셈블리를 사용할 수 있는지** 직접 정한다.

- **.cs:** 실제 클래스·메서드가 들어 있는 코드 파일.
- **.dll:** 컴파일된 .NET 어셈블리 파일(보통 DLL 형식).
- **.asmdef:** 어셈블리의 이름, 참조 관계 등 컴파일 설정이 담긴 Unity 에셋.
- **.asmref:** 다른 폴더의 코드를 *기존* 어셈블리에 포함시키는 연결 에셋. `.asmdef`의 References와 다르다.

## 2. 폴더와 출력 어셈블리

```text
Assets/_Game/
├── Contracts/
│   ├── Game.Collab.Contracts.asmdef
│   ├── IDamageable.cs
│   └── DamageRequest.cs
├── Gameplay/
│   ├── Game.Collab.Gameplay.asmdef
│   ├── HealthModel.cs
│   └── AttackService.cs
├── UI/
│   ├── Game.Collab.UI.asmdef
│   └── HealthOverlay.cs
└── Integration/
    ├── Game.Collab.Integration.asmdef
    └── DemoBootstrap.cs
```

각 폴더의 `.asmdef`가 해당 폴더와 별도 어셈블리 설정이 없는 하위 폴더 스크립트를 모아 컴파일한다. 출력물 이름은 각각 `Game.Collab.Contracts.dll`, `Game.Collab.Gameplay.dll`, `Game.Collab.UI.dll` 등이다.

## 3. 실제 .asmdef JSON과 각 속성

**실제 파일: `Assets/_Game/Gameplay/Game.Collab.Gameplay.asmdef`**

```json
{
  "name": "Game.Collab.Gameplay",
  "rootNamespace": "Game.Collab.Gameplay",
  "references": ["Game.Collab.Contracts"],
  "autoReferenced": false
}
```

| 속성 | 실제 의미 | 범위 또는 주의 |
| --- | --- | --- |
| `name` | 새로 생성할 어셈블리의 이름 | 파일명과 일치시키면 관리가 편하지만 별도 필드 |
| `rootNamespace` | Unity가 새 스크립트 생성 때 사용할 기본 namespace 설정 | 기존 소스의 namespace를 자동 수정하지 않음 |
| `references` | **이 어셈블리에서 사용할 다른 사용자 정의 어셈블리** 목록 | 단방향. 상대가 나를 참조한다는 뜻 아님 |
| `autoReferenced` | 사전 정의된 어셈블리가 이 어셈블리를 자동 참조하는지 | `false`여도 해당 코드가 빌드에서 자동 제외되는 것은 아님 |

**주의:** `references`는 프로젝트의 다른 `.asmdef`를 지정한다. `UnityEngine`처럼 엔진에서 자동 제공하는 레퍼런스는 별도의 설정 개념이 있다. 다른 어셈블리의 타입을 보려면 **어셈블리 참조 + 공개 접근 권한 + 올바른 namespace**가 맞아야 한다.

## 4. 전체 의존성 방향

```text
                Game.Collab.Integration
                  /       |       \
                 v        v        v
       Game.Collab.Gameplay   Game.Collab.UI
                 \            /
                  v          v
                Game.Collab.Contracts
```

더 정확하게는 `Integration → Gameplay`, `Integration → UI`, `Integration → Contracts`, `Gameplay → Contracts`, `UI → Contracts`이다. `Gameplay → UI` 참조는 없다. 공격 로직은 화면 종류를 몰라도 되고 UI는 체력 모델의 구체 클래스에 의존하지 않는다.

## 5. 참조가 없을 때 발생하는 컴파일 오류

**예시: `Gameplay/BadExample.cs` — 만들지 말고 이해용으로만 볼 것**

```csharp
using Game.Collab.UI;

namespace Game.Collab.Gameplay
{
    public class BadExample
    {
        private HealthOverlay overlay; // 컴파일 오류 가능
    }
}
```

왜? `Game.Collab.Gameplay.asmdef`의 `references`에 `Game.Collab.UI`가 없기 때문이다. `using`만 추가해도 해결되지 않는다. **그래서 UI를 공격 로직에서 직접 건드리지 않는 설계를 컴파일 단계에서 유도할 수 있다.**

물론 `references`에 `Game.Collab.UI`를 추가하면 컴파일은 가능해질 수 있다. 하지만 설계상 의도한 경계를 무너뜨릴 수 있으므로 먼저 `Contracts` 이벤트/인터페이스로 해결 가능한지 검토한다.

## 6. Inspector에서 참조 추가 순서

1. Project에서 `Assets/_Game/Gameplay/Game.Collab.Gameplay.asmdef`를 선택한다.
2. Inspector에서 **Assembly Definition References**를 찾는다.
3. `+`를 눌러 새 슬롯을 추가한다.
4. `Game.Collab.Contracts` 어셈블리 에셋을 선택한다.
5. **Apply** 후 Console 컴파일 오류를 확인한다.

실제 JSON에서 `"references": ["Game.Collab.Contracts"]`로 적은 것과 같은 의미다. GUID 기반 참조 설정을 사용하면 JSON 표기가 달라질 수 있다.

## 7. 모듈화는 폴더를 만드는 것 이상이다

진짜 모듈에는 **책임·데이터 소유자·외부 공개 API·허용 의존성·통합 담당자**가 있어야 한다. 단순히 C# 파일을 `Combat/`, `UI/`로 나누는 것은 보기 좋게 정리할 뿐 컴파일 참조 제한이 되지 않는다. `.asmdef`와 `internal`을 함께 사용하면 실제 경계를 더 분명히 할 수 있다.

## 8. 주의: asmdef가 못 하는 것

- GameObject에 `MonoBehaviour` 컴포넌트를 자동 부착하지 않는다. (`[RequireComponent]`의 역할과 다름)
- Inspector에 필드가 자동 할당되지 않는다.
- 이벤트가 정확히 구독되는지 검사하지 않는다.
- C# 코드가 정확한 게임 규칙을 구현했는지 판정하지 않는다.
- 모든 DLL 간 결합을 자동 최적화하지 않는다. 참조를 무분별하게 추가하면 재컴파일 범위가 커질 수 있다.

## 9. 미니 실험

1. `Gameplay`의 asmdef에서 `Game.Collab.Contracts` 참조를 잠깐 제거한다.
2. Unity Console에 `IDamageable` 등 계약 타입을 찾을 수 없다는 컴파일 오류가 생기는지 확인한다.
3. 원래 참조를 복원한다.
4. Play Mode에서 다시 공격 버튼이 동작하는지 확인한다.

이 실험은 **참조는 코드 사용 권한이며 객체 생성이 아님**을 체감하게 해 준다.
