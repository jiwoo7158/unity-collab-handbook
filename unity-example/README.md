# Unity 실습 코드 (복사 방식)

이 폴더는 **완성된 Unity 프로젝트가 아니라, 새 프로젝트에 복사해서 사용하는 `Assets` 실습 묶음**입니다. 프로젝트 버전과 패키지를 임의로 고정하지 않기 위한 구성입니다.

1. Unity Hub에서 Unity 6의 **3D Core** 프로젝트를 새로 만듭니다.
2. 이 폴더의 `Assets/_Game` 전체를 새 프로젝트의 `Assets/_Game`으로 복사합니다.
3. Unity Editor가 컴파일을 마치고 Console에 오류가 없는지 확인합니다.
4. 상단 메뉴 `Tools > Collaboration Lab > Create Demo Scene`을 누릅니다.
5. 생성된 `Assets/_Game/Demo/CollaborationDemo.unity` 씬을 열고 Play를 누릅니다.
6. 게임 화면 왼쪽 위의 **Attack enemy (-15 HP)** 버튼을 클릭해 HP 100 → 85를 확인합니다.
7. `Window > General > Test Runner`에서 EditMode / PlayMode 테스트를 실행합니다. Test Framework 패키지가 없으면 Package Manager에서 설치합니다.

`Game.Collab.Editor`는 Editor 전용 어셈블리이므로 일반 플레이어 빌드에 포함되지 않습니다. `CombatSettings` 에셋은 선택 사항이며 `Assets > Create > Collab Lab > Combat Settings` 메뉴로 만들 수 있습니다. Inspector에서 `CombatBootstrap`의 Settings 필드에 넣으면 기본 체력과 공격력을 바꿀 수 있습니다.

실행 전 주의: 이 묶음의 소스는 학습 목적 예시이며 실제 Unity Editor에서 자동 컴파일·실행 검증한 것은 아닙니다. Unity 버전 및 Test Framework 패키지 구성에 따라 테스트 어셈블리 설정을 에디터에서 조정해야 할 수 있습니다.

> **팀 저장소에 적용:** Unity에서 임포트 후 자동 생성된 `.meta` 파일을 각 에셋과 함께 Git/UVCS에 커밋하세요. 기존 `.meta` 파일을 임의로 삭제·재생성하면 참조가 끊어질 수 있습니다.
