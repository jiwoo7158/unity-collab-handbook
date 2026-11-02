# 14. 종합 실습: 3명이 만든 기능을 실제로 연결하기

> **이번 장의 결과:** Play 버튼을 누르고 공격 버튼을 클릭하면 체력이 100 → 85로 변하고 UI가 갱신된다. Unity 테스트에서 같은 흐름을 자동 검증한다.

## 0단계. Unity 프로젝트 준비

1. Unity Hub에서 Unity 6 계열의 **3D Core** 프로젝트를 새로 만든다.
2. 이 저장소의 `unity-example/Assets/_Game/` 전체를 새 Unity 프로젝트의 `Assets/_Game/` 폴더로 복사한다.
3. Unity가 스크립트 컴파일을 마칠 때까지 확인하고 Console에 오류가 없는지 검사한다.
4. Package Manager에서 **Test Framework** 패키지를 설치한다(없을 때만).

이 저장소에 Unity Editor 설치 파일이나 `Library/` 폴더는 들어 있지 않다. 제공하는 것은 **새 프로젝트에 복사할 실습 소스**이다. `Packages/manifest.json` 같은 환경 파일을 강제로 덮어쓰지 않으려는 의도다.

## 1단계. 실제 파일 위치 확인

```text
unity-example/Assets/_Game/
├── Contracts/
│   ├── Game.Collab.Contracts.asmdef
│   ├── IDamageable.cs
│   ├── IDamageModifier.cs
│   ├── IHealthReadable.cs
│   ├── DamageRequest.cs
│   └── HealthSnapshot.cs
├── Gameplay/
│   ├── Game.Collab.Gameplay.asmdef
│   ├── HealthModel.cs
│   ├── AttackService.cs
│   ├── FlatDamageModifier.cs
│   ├── LegacyHitPoints.cs
│   ├── LegacyEnemyAdapter.cs
│   ├── CombatFacade.cs
│   ├── ScopeExamples.cs
│   └── CombatSettings.cs
├── UI/
│   ├── Game.Collab.UI.asmdef
│   └── HealthOverlay.cs
├── Integration/
│   ├── Game.Collab.Integration.asmdef
│   └── DemoBootstrap.cs
├── Editor/
│   ├── Game.Collab.Editor.asmdef
│   └── CreateDemoScene.cs
└── Tests/
    ├── EditMode/
    │   ├── Game.Collab.Tests.EditMode.asmdef
    │   └── HealthModelTests.cs
    └── PlayMode/
        ├── Game.Collab.Tests.PlayMode.asmdef
        └── DemoFlowTests.cs
```

## 2단계. 세 명이 나누는 방식

| 담당 | 작업 파일 | 본인 책임 | 알아야 할 외부 API |
| --- | --- | --- | --- |
| A (공격) | `AttackService.cs`, `FlatDamageModifier.cs` | 공격 요청·피해 보정 | `IDamageable`, `IDamageModifier`, `DamageRequest` |
| B (체력) | `HealthModel.cs` | HP 소유·감소·이벤트 발행 | `IHealthReadable`, `DamageRequest` |
| C (UI) | `HealthOverlay.cs` | 표시·구독·구독 해제 | `IHealthReadable`, `HealthSnapshot` |
| 통합자 | `DemoBootstrap.cs`, `CreateDemoScene.cs` | 실제 객체 생성·UI 연결·테스트 | A/B/C의 공개 API |

**중요:** 세 팀원이 공유 계약의 내용을 각자 중복 정의하는 것이 아니라, `Contracts` 어셈블리를 먼저 합의해 병합한다.

## 3단계. 계약을 먼저 읽는다

```csharp
// IDamageable.cs
public interface IDamageable
{
    void TakeDamage(DamageRequest request);
}

// IHealthReadable.cs
public interface IHealthReadable
{
    HealthSnapshot Snapshot { get; }
    event Action<HealthSnapshot> HealthChanged;
}
```

두 블록은 핵심 부분만 추린 것이며 원본에는 `namespace`와 `using`이 있다.

- A는 체력 계산 구현을 알 필요 없이 `TakeDamage(request)`만 호출한다.
- B는 UI가 무엇인지 몰라도 상태 변경 이벤트를 발행한다.
- C는 A와 B의 구현 클래스 이름을 몰라도 이벤트를 구독한다.

## 4단계. Assembly Definition 검토

```json
// JSON 문법에서는 주석을 사용할 수 없다. 아래는 설명용 의사 코드다.
Game.Collab.Gameplay  references → [Game.Collab.Contracts]
Game.Collab.UI        references → [Game.Collab.Contracts]
Game.Collab.Integration references →
    [Game.Collab.Contracts, Game.Collab.Gameplay, Game.Collab.UI]
```

**실제 JSON 문법은 10장에서 확인한다.** 각 참조는 코드 타입 접근을 허용하지만 런타임 객체를 자동 생성하지는 않는다.

## 5단계. 에디터 메뉴로 씬 만들기

Unity 상단 메뉴에서 `Tools > Collaboration Lab > Create Demo Scene`을 클릭한다. 그러면 `Assets/_Game/Demo/CollaborationDemo.unity`가 생성된다.

```text
CollaborationDemo.unity
├── HealthOverlay      (HealthOverlay 컴포넌트)
└── CombatBootstrap    (DemoBootstrap 컴포넌트)
```

이 도구는 **Editor 전용** `CreateDemoScene.cs`에 정의되어 있다. UI를 화면에 그리는 데는 학습 편의를 위해 `OnGUI()`를 사용하므로 별도의 Canvas/Slider 설정이 필요 없다. 실제 게임 UI에서는 uGUI나 UI Toolkit을 도입할 수 있다.

## 6단계. Play에서 실행

1. 생성된 `CollaborationDemo.unity` 씬을 연다.
2. Play 모드로 진입한다.
3. 게임 화면에 `Enemy HP: 100/100`이 보이는지 확인한다.
4. `Attack enemy (-15 HP)` 버튼을 클릭한다.
5. `Enemy HP: 85/100`과 Console의 `Attack: Player, damage=15` 로그를 확인한다.

**데이터 흐름**

```text
DemoBootstrap.OnGUI(): 버튼 클릭
    ↓
AttackService.Attack(15)
    ↓
FlatDamageModifier.Modify(15) → 15
    ↓
DamageRequest(15, "Player") 생성
    ↓
HealthModel.TakeDamage(request)
    ↓
HealthModel.current = 85 (private 인스턴스 필드)
    ↓
HealthChanged(HealthSnapshot(85,100))
    ↓
HealthOverlay.OnHealthChanged(snapshot)
    ↓
HealthOverlay.OnGUI() 화면 변경
```

## 7단계. 테스트에서 검증

- **EditMode:** `HealthModelTests` 실행 → 피해 감소, 이벤트 알림, Adapter, Facade를 확인한다.
- **PlayMode:** `DemoFlowTests` 실행 → Unity 컴포넌트 연결 후 UI 문자열까지 변경되는지 확인한다.

오류가 난다면 [15장](15-troubleshooting.html)의 `.asmdef`/Test Framework/씬 연결 해결 순서대로 확인한다.

## 8단계. 고의로 실패시켜 보기

**실험 A — 계약 참조 제거:** `Game.Collab.Gameplay.asmdef`의 `references`에서 `Game.Collab.Contracts`를 잠시 삭제한다. 컴파일 오류를 확인한 다음 복구한다.

**실험 B — 이벤트 발행 누락:** `HealthModel`의 `HealthChanged?.Invoke(Snapshot);`를 주석 처리한다. 내부 체력은 변하지만 UI 변경이 멈춘다. 다시 복구한다.

**실험 C — 주입 구현 변경:** `DemoBootstrap.Awake`의 `new FlatDamageModifier(0)`을 `new FlatDamageModifier(5)`로 바꾼다. 피해량이 15에서 20으로 바뀌는지 확인한다. 공격 시스템 소스 자체를 고치지 않고도 정책을 교체했다.

**실험 D — 서로 다른 객체:** `new HealthModel(100)`을 두 번 호출하여 다른 객체를 만들면 UI가 구독한 모델과 공격 대상 모델이 달라질 수 있다. **같은 클래스여도 같은 인스턴스가 아님**을 실험으로 확인한다.

## 9단계. 팀 PR 순서로 연습

```text
PR-1 Contracts: 인터페이스/DTO 추가
PR-2 Gameplay: HealthModel/AttackService + EditMode 테스트
PR-3 UI: HealthOverlay + 이벤트 연결
PR-4 Integration: DemoBootstrap + 씬 생성기 + PlayMode 테스트
```

이 순서를 따라가면 '다 만들었는데 연결이 안 된다'가 아니라 **중간 단계부터 연결 지점의 호환성을 검증**할 수 있다.
