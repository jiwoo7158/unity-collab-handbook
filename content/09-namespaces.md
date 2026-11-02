# 09. Namespace와 접근 제한자: 이름과 공개 범위

## 1. namespace는 이름을 정리한다

```csharp
namespace Game.Collab.Gameplay
{
    public class HealthModel { }
}

namespace Game.Collab.UI
{
    public class HealthModel { } // 같은 짧은 이름도 다른 완전한 이름
}
```

두 타입의 완전한 이름은 각각 `Game.Collab.Gameplay.HealthModel`과 `Game.Collab.UI.HealthModel`이다. 파일/폴더 이름과 namespace는 자동으로 같아지는 것이 아니다.

```csharp
using Game.Collab.Gameplay;
// 같은 이름이 없으면 HealthModel처럼 짧게 쓸 수 있다.
```

`using`은 네임스페이스 이름을 편하게 쓰도록 하며 **클래스 자동 생성, 패키지 설치, 어셈블리 참조 추가를 수행하지 않는다.**

## 2. 접근 제한자는 '어디까지 보이는가?'

| 키워드 | 일반적인 접근 범위 | 예시 용도 |
| --- | --- | --- |
| `public` | 어셈블리 참조가 있으면 외부 코드에서도 접근 가능 | 공개 API, 계약 |
| `internal` | 동일 어셈블리 내부에서 접근 가능(예외: friend assembly) | 모듈 내부 구현 |
| `private` | 선언된 타입 내부에서만 접근 가능 | 체력 필드 |
| `protected` | 선언 타입과 파생 클래스 | 상속 확장 지점 |
| `protected internal` | 동일 어셈블리 또는 파생 클래스 | 의도적 확장 API |
| `private protected` | 동일 어셈블리 안의 파생 클래스 | 제한된 상속 확장 |

**주의:** `public`이어도 `.asmdef` 참조가 없다면 다른 어셈블리에서 사용할 수 없다. `internal`은 namespace가 같아도 **어셈블리가 다르면 기본적으로 접근 불가**다.

## 3. 속성의 읽기/쓰기 권한

```csharp
public sealed class Health
{
    private int hp = 100;                  // 외부 직접 접근 불가
    public int CurrentHp => hp;            // 외부 읽기만 가능
    public int MaxHp { get; private set; } = 100; // 외부 getter 가능, setter 내부만
    public void TakeDamage(int amount) { hp -= amount; }
}
```

다른 클래스는 `health.CurrentHp`를 읽을 수 있지만, `health.CurrentHp = 999`는 컴파일되지 않는다. 데이터 변경 경로를 메서드 하나로 모으면 검증과 이벤트 발행을 중앙화할 수 있다.

## 4. 클래스·인스턴스·정적 여부 구분

```csharp
public static class MathTools
{
    public static int Double(int n) => n * 2;
}

public sealed class Counter
{
    public int Value { get; private set; }  // 인스턴스 상태
    public void Increment() => Value++;
}

int n = MathTools.Double(3); // 정적 메서드: 객체 없이 호출
var a = new Counter();      // 인스턴스 객체 생성
var b = new Counter();      // 별도 인스턴스 생성
a.Increment();              // a.Value == 1, b.Value == 0
```

`static`은 '프로젝트 전체에서 아무거나 접근 가능한' 뜻이 아니다. 메서드가 정적인지, 접근 제한자가 무엇인지, 해당 타입을 컴파일상 볼 수 있는지 모두 고려해야 한다.

## 5. 같은 폴더면 접근 가능한가?

폴더는 코드에 대한 직접 접근 권한을 결정하지 않는다. Unity에서는 `.asmdef`가 있는 폴더와 그 하위 폴더(별도 asmdef/asmref가 없는 경우)의 스크립트가 해당 어셈블리에 포함된다. **같은 폴더 구조라도 어셈블리가 다르면 `internal` 접근은 달라진다.**

## 확인 문제

`Game.Collab.Gameplay` namespace를 사용하는 `HealthModel`의 `private` 필드를, 같은 namespace의 다른 클래스가 읽을 수 있을까? **없다.** namespace가 같아도 `private`은 선언 타입 내부로 제한된다.
