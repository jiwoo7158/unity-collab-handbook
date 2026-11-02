# 05. Event / Observer / Pub-Sub: 상태 변화 알리기

## 1. '명령'과 '알림'은 다르다

- `target.TakeDamage(request)`는 **상대에게 하라고 요청하는 명령**이다. 누구를 호출할지 알고 있어야 한다.
- `HealthChanged?.Invoke(snapshot)`은 **이미 일어난 사실을 알리는 이벤트**다. 누가 듣는지는 알 필요가 없다.

체력 모델이 UI를 직접 변경한다면 UI 팀원이 체력 클래스에 영향을 준다. 대신 체력 모델은 '체력이 바뀌었다'만 알리고 UI는 그 사실을 구독하도록 한다.

## 2. `event` 문법의 구성

**실제 파일: `Assets/_Game/Contracts/IHealthReadable.cs`**

```csharp
using System;

namespace Game.Collab.Contracts
{
    public interface IHealthReadable
    {
        HealthSnapshot Snapshot { get; }
        event Action<HealthSnapshot> HealthChanged;
    }
}
```

**실제 파일: `Assets/_Game/Gameplay/HealthModel.cs` 일부**

```csharp
public sealed class HealthModel : IDamageable, IHealthReadable
{
    public event Action<HealthSnapshot> HealthChanged;

    public void TakeDamage(DamageRequest request)
    {
        if (request.Amount <= 0 || current == 0) return;
        current = Math.Max(0, current - request.Amount);
        HealthChanged?.Invoke(Snapshot);
    }
}
```

- `event`는 **해당 인스턴스 멤버**다. `static`이 없으므로 HealthModel 객체마다 구독 목록이 다르다.
- `Action<HealthSnapshot>`는 구독할 함수의 형태를 정의한다.
- `+=`는 구독을 추가한다. `-=`는 특정 구독을 제거한다.
- 선언한 클래스 밖에서는 일반적인 field-like event를 직접 `Invoke`하거나 `=`로 전체 교체할 수 없다.

## 3. UI가 구독한다

**실제 파일: `Assets/_Game/UI/HealthOverlay.cs` 일부**

```csharp
private IHealthReadable source;     // UI 객체의 인스턴스 필드
private HealthSnapshot visible;    // UI 객체의 현재 표시 상태

public void Bind(IHealthReadable newSource)
{
    Unsubscribe();          // 이전 대상 구독 해제
    source = newSource;     // 새 객체 참조 저장
    if (source == null) return;
    visible = source.Snapshot; // 첫 화면은 이벤트를 기다리지 않고 직접 읽음
    Subscribe();
}

private void Subscribe()
{
    if (source == null || !isActiveAndEnabled) return;
    source.HealthChanged -= OnHealthChanged;
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
```

여기서 `source`와 `visible`은 **각 HealthOverlay 인스턴스의 필드**다. 체력 변경 통지는 `HealthModel` 쪽에서 호출되지만 실제 UI 메서드는 구독자로 등록되어 있어 실행된다. 서로의 클래스 이름을 직접 알 필요가 없다.

## 4. Unity 생명주기에 따라 구독 해제하기

```csharp
private void OnEnable()  => Subscribe();
private void OnDisable() => Unsubscribe();
private void OnDestroy() => Unsubscribe();
```

유니티 컴포넌트가 비활성화되거나 파괴되었는데 여전히 이벤트를 구독하고 있으면 원하지 않는 호출이나 참조 유지 문제가 생길 수 있다. 같은 콜백을 중복 `+=` 하는 버그도 주의한다. 실제 `HealthOverlay.cs`는 중복을 막기 위해 구독 전에 같은 핸들러를 제거한다.

**선택:** 구독자가 비활성화 중에도 이벤트를 수신해야 한다면 생명주기 설계가 달라질 수 있다. `OnEnable/OnDisable`은 무조건적인 법칙이 아니라 이 예제의 정책이다.

## 5. Observer와 Pub/Sub의 차이

**Observer 패턴**에서는 특정 발행자 객체의 변경을 관찰한다. 이 예제의 `health.HealthChanged += ...`가 해당한다.

**Pub/Sub**는 주제(topic) 또는 채널을 통해 여러 발행자와 구독자를 더 느슨하게 연결한다. 예를 들어 퀘스트, 업적, 로그 시스템이 `EnemyKilled` 메시지를 각자 구독할 수 있다. 다만 중앙 이벤트 버스를 전역 정적 객체로 남발하면 데이터 흐름 추적이 어려워진다.

```csharp
// 개념용 축약 예시: 앱 전체에서 접근 가능한 static 이벤트.
public static class GlobalSignals
{
    public static event Action<string> EnemyKilled;

    public static void PublishEnemyKilled(string id)
        => EnemyKilled?.Invoke(id);
}
```

위의 `EnemyKilled`는 **static 이벤트**라 인스턴스별 이벤트와 달리 타입에 소속된다. 게임 재시작/테스트 시 등록된 구독자를 초기화하는 정책이 없으면 문제가 될 수 있다. 본 실습에서는 의도적으로 글로벌 이벤트 버스를 쓰지 않는다.

## 6. 이벤트 데이터는 값으로 전달한다

`HealthChanged`가 `EnemyHealth` 전체 객체를 전달하면 UI가 내부 구조에 의존할 수 있다. 이 프로젝트는 대신 `HealthSnapshot` DTO를 전달한다. UI는 필요한 숫자만 읽는다.

## 검증 방법

1. 예제 씬 Play → 공격 버튼 클릭 → UI가 `100/100 → 85/100` 변경되는지 확인한다.
2. `HealthModel.TakeDamage`의 `HealthChanged?.Invoke(...)`를 잠시 주석 처리한다.
3. 체력 숫자는 내부에서 바뀌지만 화면 갱신은 안 되는 것을 확인한다.
4. 코드를 되돌린다. **내부 상태 계산과 외부 알림이 다른 책임**임을 확인할 수 있다.
