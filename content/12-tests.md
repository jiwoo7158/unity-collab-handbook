# 12. Unit Test와 Integration Test: 계약이 지켜졌는지 확인하기

## 1. 무엇을 검증할까?

| 종류 | 테스트 관점 | 이 실습의 대상 |
| --- | --- | --- |
| Unit Test | 한 클래스/작은 로직의 계산·계약 | `HealthModel`, `LegacyEnemyAdapter` |
| Integration Test | 여러 클래스나 모듈이 함께 동작 | `DemoBootstrap + AttackService + HealthOverlay` |
| Play Test | 실제 게임 씬·오브젝트 설정 | `CollaborationDemo.unity`에서 버튼 클릭 |

**컴파일 성공은 테스트 성공이 아니다.** 이벤트가 발생하지 않아도 클래스는 컴파일될 수 있다. 씬의 Inspector 참조가 비어 있어도 대부분 컴파일은 성공한다.

## 2. EditMode 테스트 파일

**실제 파일: `Assets/_Game/Tests/EditMode/HealthModelTests.cs`**

```csharp
using NUnit.Framework;
using Game.Collab.Contracts;
using Game.Collab.Gameplay;

[Test]
public void TakeDamage_ReducesHpAndNotifies()
{
    var health = new HealthModel(100); // 테스트용 로컬 변수(객체 참조)
    int notifications = 0;           // 지역 변수
    HealthSnapshot last = default;   // 지역 변수

    health.HealthChanged += snapshot =>
    {
        notifications++;
        last = snapshot;
    };

    health.TakeDamage(new DamageRequest(15, "Test"));

    Assert.That(health.Snapshot.Current, Is.EqualTo(85));
    Assert.That(last.Current, Is.EqualTo(85));
    Assert.That(notifications, Is.EqualTo(1));
}
```

위 코드는 해당 클래스의 메서드 **일부**다. 완전한 테스트 파일에서는 `class HealthModelTests` 안에 `[Test]` 메서드가 정의되어 있다. 실제 소스 전체를 참고하자. 테스트는 입력 15 → 상태 85와 알림 1회를 함께 검사한다.

## 3. 테스트 asmdef는 따로 필요하다

**실제 파일: `Assets/_Game/Tests/EditMode/Game.Collab.Tests.EditMode.asmdef`**

```json
{
  "name": "Game.Collab.Tests.EditMode",
  "rootNamespace": "Game.Collab.Tests.EditMode",
  "references": [
    "Game.Collab.Contracts",
    "Game.Collab.Gameplay"
  ],
  "autoReferenced": false,
  "includePlatforms": ["Editor"],
  "optionalUnityReferences": ["TestAssemblies"]
}
```

유니티 버전별 테스트 어셈블리 설정이 달라질 수 있다. **Test Runner에서 `Create Test Assembly Folder`로 생성된 asmdef 구성과 비교**하고 NUnit 참조 인식이 안 되면 Editor에서 자동 생성된 test assembly 설정에 맞춰 조정한다. 일반 빌드에 테스트 코드를 섞지 않는 것이 중요하다.

## 4. PlayMode 통합 테스트

**실제 파일: `Assets/_Game/Tests/PlayMode/DemoFlowTests.cs`**

```csharp
[UnityTest]
public IEnumerator Damage_UpdatesOverlayAcrossModules()
{
    var viewGo = new GameObject("test-overlay");
    var bootGo = new GameObject("test-bootstrap");
    try
    {
        var overlay = viewGo.AddComponent<HealthOverlay>();
        var bootstrap = bootGo.AddComponent<DemoBootstrap>();
        bootstrap.SetOverlay(overlay);
        yield return null; // Start 호출을 위해 프레임 이동

        bootstrap.TestAttack(15);
        Assert.That(bootstrap.CurrentHp, Is.EqualTo(85));
        Assert.That(overlay.DisplayText, Does.Contain("85/100"));
    }
    finally
    {
        Object.Destroy(viewGo);
        Object.Destroy(bootGo);
    }
}
```

`yield return null`을 사용하므로 `IEnumerator`와 `[UnityTest]`가 필요하다. 순수 계산 테스트보다 무거우므로 중요한 연결 경로에 집중해서 작성하는 것이 좋다.

## 5. Unity Editor에서 실행

1. Package Manager에서 **Test Framework**가 설치되었는지 확인한다.
2. `Window > General > Test Runner` (버전에 따라 메뉴 위치가 다를 수 있음)를 연다.
3. EditMode에서 `HealthModelTests` 4개의 테스트가 탐지되는지 확인한다.
4. **Run All**을 실행한다.
5. PlayMode에서 `DemoFlowTests`가 탐지되는지 확인 후 실행한다.
6. 실패하면 Console의 오류 메시지와 테스트 어셈블리 참조 설정을 확인한다.

테스트는 로컬 환경에서 실행 가능한 형태로 제공했지만, **이 배포물 생성 과정에서 Unity Editor의 실제 실행 테스트를 수행한 것은 아니다.** 패키지/Unity 버전에 따른 조정 가능성이 있음을 이해하자.

## 6. 팀원별 완료 조건 예시

- **Gameplay 담당:** 체력 최소 0, 음수 피해 무시, 변경 때만 이벤트 발행.
- **UI 담당:** 첫 구독 시 현재 상태 표시, 이벤트 구독/해제, 소스 재연결.
- **통합 담당:** 실제 공격이 체력 변경으로 전달, UI가 변화, 씬 참조 연결.
- **PR 리뷰어:** 기능 코드와 테스트 코드가 같은 계약을 사용하고 있는지 확인.
