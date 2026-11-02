# 04. Delegate: '호출할 함수'를 값처럼 전달하기

## 1. Delegate는 무엇인가?

일반 변수 `int damage = 10`은 숫자를 저장한다. **델리게이트 변수는 특정 시그니처(매개변수·반환형)에 맞는 메서드 호출 대상을 담는다.** 호출하는 쪽이 메서드가 정의된 구체 클래스까지 꼭 알아야 할 필요가 줄어든다.

**델리게이트는 로컬/인스턴스/static 범위를 결정하지 않는다.** 델리게이트도 선언 위치에 따라 지역 변수, 객체 필드 또는 정적 필드가 된다.

## 2. 선언과 호출 문법

```csharp
using System;

public static class DelegateSyntaxDemo
{
    // 맞는 메서드 형태: (int)를 받아 void 반환
    public delegate void DamageLogged(int amount);

    private static void PrintDamage(int amount)
    {
        Console.WriteLine(amount);
    }

    public static void Run()
    {
        DamageLogged callback = PrintDamage; // 지역 변수에 함수 참조 저장
        callback(10);                         // 저장된 함수 호출
    }
}
```

`PrintDamage`는 **정적 메서드**, `callback`은 **Run 안의 지역 변수**다. 매개변수 `amount`는 각 메서드 호출 때 전달받는 값이다.

## 3. C#에 미리 정의된 델리게이트

```csharp
Action             a = () => Console.WriteLine("start");
Action<int>        b = value => Console.WriteLine(value);
Func<int, int>     c = value => value * 2;
Predicate<int>     d = value => value > 0;

// Action: 반환 void
// Func: 마지막 타입 인자가 반환형
// Predicate<T>: T를 받아 bool 반환
```

실무에서는 새로운 delegate 타입을 매번 만들기보다 `Action<>`, `Func<>`로 충분한 경우가 많다.

## 4. 실제 프로젝트: 공격 로그를 주입한다

**실제 파일: `Assets/_Game/Gameplay/AttackService.cs`**

```csharp
private readonly Action<DamageRequest> onAttack;

public AttackService(
    IDamageable target,
    IDamageModifier modifier,
    Action<DamageRequest> onAttack = null)
{
    this.target = target;
    this.modifier = modifier;
    this.onAttack = onAttack;
}

public void Attack(int rawAmount)
{
    int modified = modifier.Modify(rawAmount); // 지역 변수
    var request = new DamageRequest(modified, "Player");
    onAttack?.Invoke(request); // 등록되지 않았으면 호출하지 않음
    target.TakeDamage(request);
}
```

**실제 파일: `Assets/_Game/Integration/DemoBootstrap.cs`**

```csharp
private void Awake()
{
    health = new HealthModel(100);
    attacks = new AttackService(health, new FlatDamageModifier(0), LogAttack);
}

private void LogAttack(DamageRequest request)
{
    Debug.Log(request.Amount);
}
```

여기서 `LogAttack`은 `DemoBootstrap` **인스턴스 메서드**다. `Action<DamageRequest>`는 그 메서드를 호출할 수 있도록 참조를 저장한다. `AttackService`는 `DemoBootstrap` 타입을 참조하지 않아도 로그를 남길 수 있다.

## 5. Delegate와 Interface 선택 기준

| 문제 | 선호하는 접근 |
| --- | --- |
| 한 번 호출할 함수 하나만 전달 | `Action<T>` / `Func<T>` |
| 여러 메서드·속성의 긴 계약 | `interface` |
| 상태 변화가 일어났다는 것을 여러 구독자에게 알림 | `event` |
| 외부가 등록된 콜백을 마음대로 전체 교체하면 안 됨 | `event` |

## 6. 멀티캐스트와 부작용

```csharp
Action<int> callbacks = x => Console.WriteLine($"A:{x}");
callbacks += x => Console.WriteLine($"B:{x}");
callbacks?.Invoke(3); // A:3 그리고 B:3
```

멀티캐스트 델리게이트는 여러 함수를 연결할 수 있다. 하지만 외부에 `public Action` 필드를 노출하면 외부 코드가 `=`로 기존 목록을 덮어쓰거나 직접 호출할 수 있다. **일반적인 상태 알림에는 `event`를 우선** 사용한다.

## 연습

`AttackService`를 생성할 때 `onAttack`으로 `request => Debug.Log(request.Amount)`를 전달해 본다. 람다는 **메서드 인자로 전달한 델리게이트 값**이고, 로그 메시지는 AttackService 내부 필드와 무관하다.
