# 08. Adapter와 Facade: 기존 코드와 복잡한 기능 감싸기

## 1. Adapter: 호출 규약이 다를 때

B팀이 이미 `LoseHp(int)` 메서드를 만들어 두었다. 새 전투 시스템은 `IDamageable.TakeDamage(DamageRequest)`만 호출한다. 기존 코드를 전부 뜯어고치지 않고 **중간 변환기(Adapter)**를 만든다.

**실제 파일: `Assets/_Game/Gameplay/LegacyHitPoints.cs`**

```csharp
public sealed class LegacyHitPoints
{
    public int Hp { get; private set; }
    public LegacyHitPoints(int hp) { Hp = Math.Max(0, hp); }
    public void LoseHp(int value) { Hp = Math.Max(0, Hp - Math.Max(0, value)); }
}
```

**실제 파일: `Assets/_Game/Gameplay/LegacyEnemyAdapter.cs`**

```csharp
using Game.Collab.Contracts;

public sealed class LegacyEnemyAdapter : IDamageable
{
    private readonly LegacyHitPoints legacy;

    public LegacyEnemyAdapter(LegacyHitPoints legacy)
    {
        this.legacy = legacy;
    }

    public void TakeDamage(DamageRequest request)
    {
        legacy.LoseHp(request.Amount);
    }
}
```

위 코드 블록은 핵심을 보여주기 위해 네임스페이스/가드 일부를 생략했다. **실제 실행용은 샘플 파일 전체를 기준으로 한다.**

```csharp
var oldCode = new LegacyHitPoints(100); // 별도 객체
IDamageable target = new LegacyEnemyAdapter(oldCode); // Adapter 객체
var attack = new AttackService(target, new FlatDamageModifier(0));
attack.Attack(15);
// oldCode.Hp == 85
```

**의존성 방향:** AttackService → IDamageable ← LegacyEnemyAdapter → LegacyHitPoints. AttackService는 `LoseHp`가 있는지도 모른다.

## 2. Facade: 내부가 복잡하지만 외부는 단순하게

반대로 여러 클래스를 묶어 외부에 **단순한 사용 창구(Facade)**를 제공하고 싶을 수 있다.

**실제 파일: `Assets/_Game/Gameplay/CombatFacade.cs`**

```csharp
public sealed class CombatFacade
{
    private readonly HealthModel health;
    private readonly AttackService attack;

    public IHealthReadable Health => health;

    public CombatFacade(int maximumHp)
    {
        health = new HealthModel(maximumHp);
        attack = new AttackService(health, new FlatDamageModifier(0));
    }

    public void PlayerAttack(int damage) => attack.Attack(damage);
}
```

외부 코드는 복잡한 연결 대신 다음만 사용한다.

```csharp
var combat = new CombatFacade(100);
combat.PlayerAttack(15);
// combat.Health.Snapshot.Current == 85
```

Facade는 시스템 내부의 여러 클래스를 **조직하고 진입점을 단순화**한다. 그러나 모든 기능을 한 거대한 `GameManager` Facade에 몰아넣으면 오히려 경계를 무너뜨릴 수 있다.

## 3. 둘을 구분하는 질문

| 문제 | 적절한 패턴 |
| --- | --- |
| 이미 만든 클래스의 API가 계약과 다르다 | Adapter |
| 외부에서 내부 클래스 5개를 직접 조립해야 한다 | Facade |
| 실제 구현체를 바꿔 끼우고 싶다 | Interface + DI |
| 변경된 상태를 여러 곳에 알리고 싶다 | Event / Observer |

## 4. 팀 통합 상황에서 단계적으로 적용

1. 기존 `LegacyHitPoints`는 그대로 둔다.
2. 외부 계약 `IDamageable`을 합의한다.
3. `LegacyEnemyAdapter`를 만든다.
4. `AttackService`는 인터페이스만 호출하게 한다.
5. 통합 테스트로 결과가 100 → 85인지 확인한다.
6. 장기적으로 기존 코드를 교체할 때 Adapter만 제거한다.

**중요:** Adapter는 '무조건 좋은 설계'가 아니라 기존 시스템 간 불일치를 관리하는 선택지다. 코드를 서로 합의해서 수정할 수 있다면 직접 계약을 구현하는 편이 더 단순할 수도 있다.
