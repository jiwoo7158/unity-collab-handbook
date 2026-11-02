# 02. 변수·필드·속성·static·범위 완전 정리

> 이 장은 기술별로 반복 등장하는 '이 상태를 누가 소유하는가?'를 이해하는 핵심이다.

## 1. 같은 `int`라도 무엇에 선언했는지가 다르다

**실제 파일: `Assets/_Game/Gameplay/ScopeExamples.cs`**

```csharp
namespace Game.Collab.Gameplay
{
    public sealed class ScopeExamples
    {
        public const int DefaultMaxHp = 100;  // [A] 상수. 타입 소속
        public static int CreatedCount { get; private set; } // [B] 정적 속성
        private int currentHp;                 // [C] 인스턴스 필드

        public int CurrentHp => currentHp;    // [D] 인스턴스 속성

        public ScopeExamples(int initialHp)   // [E] 생성자 매개변수
        {
            currentHp = initialHp;
            CreatedCount++;
        }

        public void Hurt(int amount)           // [F] 메서드 매개변수
        {
            int applied = amount < 0 ? 0 : amount; // [G] 지역 변수
            currentHp -= applied;
            if (currentHp < 0)
            {
                int correction = -currentHp; // [H] 블록 내부 지역 변수
                currentHp += correction;
            }
            // correction 사용 불가: 선언된 블록을 벗어났음.
        }
    }
}
```

| 표식 | 분류 | 소유 범위·생존 기간 | 코드 밖 접근 |
| --- | --- | --- | --- |
| A | `const` 필드 | 타입에 속하는 컴파일 시점 상수 | `ScopeExamples.DefaultMaxHp` |
| B | `static` 속성 | 타입 수준에서 공유; 도메인 재로드 등 생명주기 주의 | 읽기 가능, 외부에서 `set` 불가 |
| C | `private` 인스턴스 필드 | **각 객체별**로 별도 저장 | 클래스 외부 직접 접근 불가 |
| D | `public` 인스턴스 속성 | 각 객체 상태의 공개 읽기 API | `example.CurrentHp` |
| E/F | 매개변수 | 호출 때 전달, 해당 함수 몸체에서 사용 | 밖에서 이름으로 접근 불가 |
| G | 지역 변수 | 선언 위치의 블록부터 그 범위 끝 | 다른 메서드에서 접근 불가 |
| H | 블록 지역 변수 | `if { ... }` 내부 | `if` 밖에서 접근 불가 |

**주의:** 접근 제한자(`public`/`private`)는 '누가 접근 가능한가'이고, `static`은 '객체마다 하나인가 타입 전체 하나인가'다. 서로 다른 축이다.

## 2. `static`과 인스턴스 값 비교

```csharp
var a = new ScopeExamples(100);
var b = new ScopeExamples(30);
a.Hurt(10);

// a.CurrentHp == 90
// b.CurrentHp == 30  (a를 바꿔도 b는 변하지 않음)
// ScopeExamples.CreatedCount는 객체 생성 시 2 증가
```

`CreatedCount`는 `a.CreatedCount`가 아닌 **`ScopeExamples.CreatedCount`** 형태로 접근한다. `static` 상태는 서로 공유되므로 테스트 간 값 오염·게임 리스타트 시 상태 잔존 가능성을 고려해야 한다. Unity의 Enter Play Mode Options에서 Domain Reload를 끄면 정적 상태와 이벤트의 초기화가 더욱 중요해진다.

## 3. C#에는 진짜 '글로벌 변수'가 있나?

**C#에는 네임스페이스에 직접 놓는 전역 변수 선언이 없다.** 보통 '전역 변수'라고 부르는 것은 `public static` 필드/속성 또는 싱글턴 객체인 경우가 많다.

```csharp
public static class ScoreBoard
{
    public static int Score { get; private set; }
    public static void Add(int amount) => Score += amount;
}

// 타입 이름으로 어디서나 접근 '가능할 수' 있지만,
// 실제로는 타입의 접근 제한자와 어셈블리 참조가 모두 맞아야 한다.
ScoreBoard.Add(10);
```

`ScoreBoard.Score`는 전역 범위에 떠다니는 변수가 아니라 **ScoreBoard 타입에 소속된 정적 속성**이다. Unity 멀티씬/테스트에서는 정적 공유 상태를 함부로 도입하지 않는 것이 좋다.

## 4. 객체 참조를 복사한 것과 객체를 복사한 것

```csharp
var a = new ScopeExamples(100);
var b = a;             // 같은 객체를 가리키는 참조 복사
b.Hurt(20);
// a.CurrentHp == 80, b.CurrentHp == 80

var c = new ScopeExamples(100); // 새 객체 생성
c.Hurt(20);
// c와 a는 서로 다른 인스턴스
```

클래스 변수는 기본적으로 객체 참조를 담고, `struct`는 값 자체를 담는다. 이는 DTO에서 왜 변경 불가능한 데이터 구조를 쓰는지 이해하는 데 연결된다.

## 5. `SerializeField`는 접근 제한자를 변경하지 않는다

```csharp
[SerializeField] private int maxHp = 100;
```

Inspector에 노출하도록 직렬화하는 것이지 `private`을 `public`으로 만드는 것이 아니다. 다른 스크립트에서 `other.maxHp`로 접근할 수 없다. 메서드나 공개 읽기 속성을 통해 제공한다.

## 실습 문제

`ScopeExamples`의 `currentHp`를 `static`으로 바꾸면 두 객체가 왜 서로 영향을 줄까? 또 `Hurt` 함수 안의 `int applied`를 다른 클래스에서 바로 읽으려 하면 왜 안 될까? 답은 **공유 단위와 선언 범위가 다르기 때문**이다.
