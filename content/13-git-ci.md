# 13. Git·GitHub PR·CI: '각자 완성'을 '함께 작동'으로 만들기

## 1. Git 충돌과 통합 실패는 다르다

A가 `AttackService.cs`를 수정하고 B가 `HealthModel.cs`를 수정하면 Git 텍스트 충돌은 없을 수 있다. 그러나 A가 `LoseHp`를 호출하고 B가 `TakeDamage`만 제공하면 **코드는 서로 연결되지 않는다.** 그래서 Git 전략과 계약 검토·통합 테스트를 함께 사용해야 한다.

## 2. 일 시작 전에 만드는 기능 계약 카드

**이슈 예시: `F-012 Player Attack`**

```text
책임: 플레이어 공격 시 대상에게 피해 요청
소유 모듈: Game.Collab.Gameplay
공개 API: AttackService.Attack(int rawAmount)
요구 계약: IDamageable, IDamageModifier, DamageRequest
데이터 소유자: 체력 값은 HealthModel, 공격력은 공격 구성
통합 지점: DemoBootstrap / 별도 테스트 씬
완료 조건: 15 피해 → 100 HP가 85가 되고 UI 변경
```

핵심은 **누가 상대 파일을 수정해야 하는가**가 아니라 **모듈 간 연결 계약이 무엇인가**를 합의하는 것이다.

## 3. 브랜치 작업 예시

```bash
# 최신 main에서 기능 브랜치 시작
git switch main
git pull --ff-only
git switch -c feat/player-attack

# 작업 후 작은 단위로 커밋
git add unity-example/Assets/_Game/Gameplay
git commit -m "feat: add contract-driven attack service"
git push -u origin feat/player-attack
```

GitHub에서 PR을 생성한다. 가능한 한 **계약 → 기본 구현 → 이벤트/UI → 통합 씬** 순서로 작은 PR을 만든다. 모든 팀원이 일주일 넘게 자기 브랜치에서 따로 작업하다 마지막에 한 번에 병합하지 않는다.

## 4. PR 템플릿에서 중요한 질문

```markdown
## 변경 대상과 소유자
- 담당 기능/모듈:
- 영향받는 외부 계약(interface/DTO/event):

## 사용 방법
- 다른 팀원은 어떤 메서드를 호출해야 하나?
- Inspector에서 어떤 객체를 연결해야 하나?

## 검증
- EditMode 테스트:
- PlayMode/수동 씬 테스트:
- 미해결 연결 작업:
```

실제 저장소에 `.github/PULL_REQUEST_TEMPLATE.md`가 포함되어 있으니 직접 수정해서 사용할 수 있다.

## 5. CI(Continuous Integration)는 무얼 하는가?

CI는 변경 사항을 공유 브랜치에 합칠 때 **자동 검사 작업을 실행하는 체계**다. 일반적으로 PR 생성/업데이트 시 코드 검사와 테스트를 수행하고 실패하면 병합을 막도록 구성한다.

다만 Unity 테스트를 GitHub Actions에서 실행하려면 Unity 설치 환경, **Unity 라이선스 인증**, Test Framework 등 추가 구성이 필요하다. 그래서 이 자료에서는 **GitHub Pages 배포 자체는 빌드 없이 진행**하고, Unity CI는 사용자가 환경을 맞춘 뒤 활성화하는 선택 실습으로 다룬다.

**선택적 Unity CI 예시 (직접 설정 후 사용)**

```yaml
name: unity-tests
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
          UNITY_EMAIL: ${{ secrets.UNITY_EMAIL }}
          UNITY_PASSWORD: ${{ secrets.UNITY_PASSWORD }}
        with:
          projectPath: .
          githubToken: ${{ secrets.GITHUB_TOKEN }}
```

**주의:** 위 YAML은 **완전한 즉시 실행용이 아닌 구성 원리 예시**다. 이 저장소의 `unity-example/`는 완성 Unity 프로젝트가 아니라 `Assets` 복사 실습 묶음이므로 `projectPath: .`로 바로 실행할 수 없다. Unity 프로젝트 전체를 별도로 저장소에 두고 그 경로를 지정해야 하며, 인증 방식도 Unity 라이선스 종류에 따라 달라진다. 비밀키를 저장소 코드에 직접 기록하지 않는다.

## 6. 처음 팀에서 적용할 최소 규칙

1. 공용 인터페이스와 DTO 변경은 구현 담당자와 함께 리뷰한다.
2. PR 본문에 **다른 팀원이 호출할 API**와 **씬/프리팹 연결 방법**을 적는다.
3. PR 단위로 수정 범위를 작게 유지한다.
4. `main` 보호 규칙으로 리뷰와 필수 검사를 설정한다.
5. CI가 아직 없다면 병합 전에 적어도 해당 Unity 씬에서 수동 통합 테스트를 수행한다.

## 7. merge, rebase와 실제 위험

공유 브랜치에 다른 팀원이 추가 커밋했다면 무분별한 force push를 피한다. conflict가 난 코드를 문법만 맞춰 합치지 말고 변경된 **API 의도**까지 확인한다. 충돌 파일이 씬·프리팹 YAML이라면 Unity Editor에서 실제 참조가 살아 있는지도 검증해야 한다.
