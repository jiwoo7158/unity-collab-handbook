# 01. 먼저 이해할 것: 코드, 객체, DLL, 참조

## 1. 파일과 타입은 다르다

**`Player.cs`는 파일**이고, 그 안의 `Player`는 **타입(class)** 이다. 클래스는 객체를 만들기 위한 정의다. 파일 이름과 클래스 이름은 별개 개념이지만 Unity의 `MonoBehaviour`는 파일명과 클래스명을 맞추는 것이 실무상 중요하다.

**파일: `Assets/_Game/Gameplay/ScopeExamples.cs` 일부**

```csharp
namespace Game.Collab.Gameplay
{
    public sealed class ScopeExamples
    {
        private int currentHp; // 객체마다 따로 존재하는 필드
        public ScopeExamples(int initialHp) { currentHp = initialHp; }
        public int CurrentHp => currentHp;
    }
}
```

**다른 파일: 일반 C# 스크립트 또는 테스트 내부**

```csharp
var alice = new Game.Collab.Gameplay.ScopeExamples(100);
var bob = new Game.Collab.Gameplay.ScopeExamples(50);
// alice와 bob은 별개의 객체(인스턴스)다.
// alice.CurrentHp == 100, bob.CurrentHp == 50
```

`alice`, `bob`은 **지역 변수에 저장한 객체 참조**이고, `currentHp`는 **각 객체 내부의 인스턴스 필드**다. 같은 클래스에서 만들었다고 필드 값이 자동으로 공유되지 않는다.

## 2. 컴파일은 무엇을 만드는가?

대부분의 Unity C# 소스는 **어셈블리(컴파일 단위)**로 묶여 컴파일된다. 어셈블리 결과물은 보통 `.dll`로 표현된다. 이것은 Windows에서만 쓰는 네이티브 DLL이라는 뜻이 아니라, .NET 관리 코드와 메타데이터를 담은 어셈블리 파일이라는 뜻이다. Unity가 최종 플랫폼용으로 빌드하는 단계에서는 추가 변환이 일어날 수 있다.

```text
PlayerAttack.cs + HealthModel.cs + ...
                 │  C# 컴파일
                 ▼
       Assembly-CSharp.dll  (기본 구성의 예)
```

어셈블리를 분리하면 다음처럼 된다.

```text
IDamageable.cs  ───> Game.Collab.Contracts.dll
HealthModel.cs  ───> Game.Collab.Gameplay.dll
HealthOverlay.cs ──> Game.Collab.UI.dll
```

## 3. 의존(Dependency)은 '사용한다'는 의미

A 클래스가 B 타입을 필드, 매개변수, 반환형, `new` 등의 위치에서 사용하면 A는 B에 **타입 의존성**이 있다.

```csharp
public sealed class PlayerAttack
{
    private EnemyHealth enemy; // EnemyHealth 타입을 알아야 컴파일 가능
}
```

반대로 아래 코드는 `EnemyHealth`라는 구체적 타입에 대한 의존성이 없다. 다만 `IDamageable` 계약에는 의존한다.

```csharp
public sealed class PlayerAttack
{
    private IDamageable target; // 계약에는 의존함
}
```

**의존성은 완전히 제거하는 것이 아니라 안정적인 방향으로 관리하는 것**이다.

## 4. 두 개의 참조를 혼동하지 말자

| 참조 | 의미 | 설정 위치 |
| --- | --- | --- |
| **어셈블리 참조** | 다른 DLL의 `public` 타입을 컴파일 중 볼 수 있음 | `.asmdef` → References |
| **객체 참조** | 실행 중 특정 인스턴스를 가리킴 | 필드, 생성자, Inspector, `GetComponent` 등 |

```csharp
// 이 코드가 컴파일되는 조건: 이 파일의 어셈블리가 IDamageable 어셈블리를 참조
private IDamageable target;

// 이 코드가 실제로 동작하는 조건: target에 실제 객체가 연결돼 있어야 함
target.TakeDamage(new DamageRequest(10, "Player"));
```

어셈블리 참조가 있어도 `target == null`이면 런타임에 실패할 수 있다. 반대로 객체가 씬에 있어도 컴파일상 사용이 허용되지 않으면 타입을 직접 적는 코드가 컴파일되지 않는다.

## 5. Namespace와 Assembly도 다르다

```csharp
namespace Game.Collab.Gameplay { /* 여러 클래스 */ }
```

`namespace`는 타입 이름을 조직하고 충돌을 줄이기 위한 **이름 공간**이다. 접근을 막는 보안 경계나 컴파일 단위가 아니다. 서로 다른 어셈블리가 같은 namespace를 사용해도 되고, 하나의 어셈블리 안에 여러 namespace가 있어도 된다.

## 체크포인트

- `new HealthModel(100)`은 객체 생성인가, DLL 생성인가? → 객체 생성.
- `.asmdef` 참조를 추가하면 체력 UI가 자동 연결되는가? → 아니다.
- `using Game.Collab.Contracts;`는 어셈블리 참조를 대신하는가? → 아니다.
