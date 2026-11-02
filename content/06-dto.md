# 06. DTO / struct / record / class: 데이터를 전달하는 계약

## 1. 왜 메서드 인자 하나만 넘기지 않을까?

```csharp
TakeDamage(10);
```

단순하지만 누가 공격했는지, 어떤 피해인지, 치명타인지 등 정보가 늘면 `TakeDamage(10, "Player", true, 1.5f, ...)`처럼 매개변수가 끝없이 증가한다. **DTO(Data Transfer Object)**는 두 모듈이 주고받을 정보의 모양을 하나의 타입으로 묶는다.

DTO는 C# 문법 키워드가 아닌 **역할을 나타내는 이름**이다. `class`, `struct`, `record` 등 여러 타입으로 만들 수 있다.

## 2. 실습 DTO 파일

**실제 파일: `Assets/_Game/Contracts/DamageRequest.cs`**

```csharp
namespace Game.Collab.Contracts
{
    public readonly struct DamageRequest
    {
        public int Amount { get; }
        public string SourceId { get; }

        public DamageRequest(int amount, string sourceId)
        {
            Amount = amount;
            SourceId = sourceId ?? "unknown";
        }
    }
}
```

`DamageRequest`는 **타입**, `Amount`와 `SourceId`는 각 struct 값에 포함되는 **속성**, `amount`와 `sourceId`는 생성자의 **매개변수**다. `readonly struct`와 읽기 전용 속성 덕분에 생성 후 값을 임의로 변경할 수 없도록 의도했다.

**실제 파일: `Assets/_Game/Contracts/HealthSnapshot.cs`**

```csharp
public readonly struct HealthSnapshot
{
    public int Current { get; }
    public int Maximum { get; }
    public HealthSnapshot(int current, int maximum)
    {
        Current = current;
        Maximum = maximum;
    }
}
```

전체 파일에는 `namespace Game.Collab.Contracts` 선언도 있다. 각 코드 블록을 복사해 사용할 때는 실제 파일을 기준으로 한다.

## 3. DTO는 누구의 소유인가?

```csharp
var request = new DamageRequest(15, "Player"); // 지역 변수: struct 값
attack.Attack(request.Amount);
```

`request`는 이 메서드의 **지역 변수**이고, `DamageRequest`는 Contracts 어셈블리에 공개된 **타입**이다. 두 용어를 혼동하면 안 된다. 데이터 전달을 위해 DTO를 공유하더라도 다른 모듈의 내부 상태를 직접 공유하는 것은 아니다.

## 4. class와 struct의 큰 차이

```csharp
public sealed class MutableDamage
{
    public int Amount;
}

var a = new MutableDamage { Amount = 10 };
var b = a;
b.Amount = 20;
// a.Amount == 20: 둘 다 같은 class 인스턴스를 가리킴
```

```csharp
public struct ValueDamage
{
    public int Amount;
}

var a = new ValueDamage { Amount = 10 };
var b = a;
b.Amount = 20;
// a.Amount == 10: struct 값이 복사됨
```

작고 변경 불가능한 숫자 데이터에 `readonly struct`는 좋은 후보지만, 크기가 큰 값 타입이나 복잡한 소유권이 필요한 객체에는 `class`가 더 나을 수 있다. 컬렉션·참조 타입 필드를 포함한 DTO는 `readonly`라고 해서 참조 대상 내부까지 자동으로 불변이 되는 건 아니다.

## 5. record는 언제 사용할까?

```csharp
// 현재 Unity 프로젝트의 C# 언어 버전 지원 여부를 먼저 확인할 것.
public record DamageInfo(int Amount, string SourceId);
```

`record`는 값 기반 동등성과 편리한 데이터 표현에 적합하지만, Unity/C# 버전과 직렬화 지원을 확인해야 한다. 본 실습은 **광범위한 Unity 6 환경에서 이해하기 쉬운 `readonly struct`** 를 채택했다. Unity Inspector 직렬화가 필요하면 `[Serializable]` 필드 기반 클래스/구조체를 별도로 검토한다.

## 6. DTO 설계 규칙

- 수신자가 실제로 필요한 정보만 포함한다.
- 다른 팀의 구체 MonoBehaviour를 DTO에 무분별하게 넣지 않는다.
- `Amount`의 단위(HP), 허용 범위(음수 허용 안 함), 의미를 설명한다.
- `DamageRequest`는 **명령 데이터**, `HealthSnapshot`은 **상태 알림 데이터**다.
- 계약 수정 시 **양측 담당자에게 변경 영향을 알린다**.

## 연습

`DamageRequest`에 `DamageType` 열거형을 추가하고, `AttackService`에서 생성할 때 값을 전달해 보자. 인터페이스 메서드의 개수가 변하지 않고도 전달 데이터의 표현력이 늘어난다. 단, 기존 생성자 호출은 수정하거나 하위 호환 오버로드를 제공해야 한다.
