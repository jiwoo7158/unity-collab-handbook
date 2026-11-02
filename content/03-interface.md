# 03. Interface: 팀 사이의 '기능 계약'

## 1. Interface가 해결하는 문제

A팀이 공격 시스템을 만들고 B팀이 적 체력을 만든다. A가 `EnemyHealth`의 내부 필드를 직접 바꾸면 B가 구조를 바꾸는 순간 A도 수정해야 한다. **인터페이스는 A에게 '어떤 메서드를 호출할 수 있는가'만 알려주고 B가 내부 구현을 자유롭게 바꾸도록 한다.**

인터페이스는 런타임에 새 GameObject나 실제 인스턴스를 자동 생성하지 않는다. 인터페이스 자체에 호출할 로직이 있는 것도 아니다(이 교재는 기본 계약 선언을 사용한다).

## 2. 실제 파일과 문법

**파일: `Assets/_Game/Contracts/IDamageable.cs`**

```csharp
namespace Game.Collab.Contracts
{
    public interface IDamageable
    {
        void TakeDamage(DamageRequest request);
    }
}
```

- `public`: 어셈블리 외부에도 타입 공개(단, 참조가 필요).
- `interface`: 객체가 구현해야 할 멤버의 계약.
- `void`: 반환값이 없다.
- `DamageRequest request`: 매개변수이며 **호출 시 전달되는 값**이다. 전역 변수나 필드가 아니다.

**파일: `Assets/_Game/Gameplay/HealthModel.cs` 일부**

```csharp
public sealed class HealthModel : IDamageable
{
    private int current; // 이 객체의 인스턴스 필드

    public void TakeDamage(DamageRequest request)
    {
        current -= request.Amount;
    }
}
```

위 코드는 **문법만 보여주는 축약 예시**다. 완전한 실행 코드는 실습 묶음의 `HealthModel.cs`를 사용하며, 음수·0 처리와 이벤트가 들어 있다.

## 3. 사용하는 쪽은 인터페이스 타입으로 선언한다

**파일: `Assets/_Game/Gameplay/AttackService.cs` 일부**

```csharp
private readonly IDamageable target; // AttackService '객체'가 가진 필드

public AttackService(IDamageable target, IDamageModifier modifier)
{
    this.target = target; // 생성자 매개변수로 받은 객체 참조 저장
}

public void Attack(int amount)
{
    target.TakeDamage(new DamageRequest(amount, "Player"));
}
```

`target`의 **정적 타입**은 `IDamageable`이고, **실제 런타임 객체**는 `HealthModel`, `LegacyEnemyAdapter` 등 계약을 구현한 어떤 클래스일 수 있다. 이것이 다형성이다.

## 4. 독립 개발 시 Fake로 대체

아래는 문법 실습용으로 추가해 볼 파일이다.

**직접 생성: `Assets/_Game/Gameplay/FakeDamageable.cs`**

```csharp
using Game.Collab.Contracts;

namespace Game.Collab.Gameplay
{
    public sealed class FakeDamageable : IDamageable
    {
        public int LastDamage { get; private set; } // 객체별 상태

        public void TakeDamage(DamageRequest request)
        {
            LastDamage = request.Amount;
        }
    }
}
```

```csharp
var fake = new FakeDamageable();
var attack = new AttackService(fake, new FlatDamageModifier(0));
attack.Attack(15);
// fake.LastDamage == 15
```

적 시스템 개발이 끝나지 않아도 공격 시스템의 요청 전달을 검증할 수 있다.

## 5. 누가 무엇에 접근하는가?

| 대상 | 소유자 | 다른 팀이 접근 가능한 부분 |
| --- | --- | --- |
| `IDamageable` | Contracts 어셈블리 | `TakeDamage` 계약(Contracts 참조 필요) |
| `HealthModel.current` | HealthModel 인스턴스 | `private`이라 외부 직접 접근 불가 |
| `HealthModel.TakeDamage` | HealthModel 인스턴스 | `public`이므로 참조 가능한 코드에서 호출 가능 |
| `AttackService.target` | AttackService 인스턴스 | `private readonly`라 외부 직접 접근 불가 |

## 6. 사용할 때와 사용하지 않을 때

**권장:** 여러 구현체를 공통으로 처리하거나, 기능 담당 팀 사이에 경계를 만들거나, 테스트에서 Fake를 주입할 때.

**과한 경우:** 내부에서만 쓰는 단순 계산기 하나를 위해 구현체도 한 종류뿐인데 앞으로 교체할 요구가 없는 상황. 모든 클래스마다 `IClassName`을 만드는 것은 목표가 아니다.

## 주의할 점

- 인터페이스의 변경은 **구현체 전체에 영향**을 준다. PR에서 계약 변경을 먼저 검토한다.
- 한 거대한 인터페이스에 피해·UI·저장·사망을 모두 넣지 않는다. 역할별로 작게 분리한다.
- 인터페이스 선언만으로 Unity Inspector 연결이 자동으로 이루어지지 않는다. 실제 객체 연결은 DI/통합 계층에서 한다.
