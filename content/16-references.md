# 16. 용어집과 공식 참고 자료

## 핵심 용어집

| 용어 | 뜻 |
| --- | --- |
| Contract | 모듈 경계에서 합의한 공개 API·데이터·이벤트 규약 |
| Coupling(결합도) | 한 코드가 다른 코드의 구체 구조에 얼마나 의존하는가 |
| Cohesion(응집도) | 같은 모듈 안의 책임들이 얼마나 밀접하게 관련되는가 |
| Assembly | 컴파일된 C# 타입과 메타데이터를 담는 단위 |
| Namespace | 클래스 등의 이름을 그룹화하는 논리적 이름 공간 |
| Object Reference | 실행 중 특정 객체 인스턴스를 가리키는 값 |
| Assembly Reference | 컴파일 때 다른 어셈블리의 타입을 사용할 수 있도록 정한 의존 관계 |
| Interface | 클래스가 구현하기로 약속한 멤버의 타입 계약 |
| Delegate | 일정한 시그니처의 함수를 참조·전달하는 타입 |
| Event | 구독자가 추가/제거되는 알림 창구 |
| DTO | 모듈·계층 사이에서 전달할 정보를 담는 타입 |
| DI | 의존 객체를 사용하는 클래스 외부에서 제공하는 기법 |
| Adapter | 기존 API를 새로운 계약에 맞춰 변환하는 객체 |
| Facade | 복잡한 하위 시스템에 제공하는 단순한 외부 진입점 |
| Composition Root | 실제 구현 객체를 생성하고 연결하는 조립 장소 |
| Unit Test | 작은 로직 단위의 동작 검사 |
| Integration Test | 복수 모듈의 협력 동작 검사 |
| CI | 코드 변경마다 자동화한 빌드/검사를 수행하는 프로세스 |

## 공식 문서

학습서의 기술 설명은 아래 공식 문서의 일반적인 원칙을 바탕으로 구성했다. 유니티 버전 및 패키지 업데이트에 따라 에디터 메뉴와 설정은 달라질 수 있으므로 사용 중인 버전의 설명서를 함께 확인한다.

- [Unity — 어셈블리와 Assembly Definition 소개](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/script-compilation/assembly-definition-files/assembly-definitions-intro)
- [Unity — Assembly 참조의 기본 원칙](https://docs.unity.com/en-us/engine/6000.0/manual/programming-environment/script-compilation/assembly-definition-files/assembly-definitions-referencing)
- [Unity — EditMode / PlayMode 테스트의 차이](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/test-framework-introduction/getting-started/edit-mode-vs-play-mode-tests)
- [Unity — Test Assembly 만들기](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/test-framework-introduction/getting-started/workflow-create-test-assembly)
- [Unity — Assembly Definition 한국어 속성 설명](https://docs.unity.com/ko-kr/engine/6000.0/manual/scripting/compilation-and-code-reload/script-compilation/assembly-definition-files/class-assembly-definition-importer)
- [GitHub — Pages 게시 소스 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GameCI — Unity Test Runner GitHub Actions](https://game.ci/docs/github/test-runner/)
- [Microsoft — C# 언어 설명서](https://learn.microsoft.com/dotnet/csharp/)

## 이 자료의 검증 범위와 한계

- 문서 사이트는 **정적 HTML 파일**로 생성되며 별도 서버 코드는 없다.
- 제공한 Unity 실습의 C# 소스와 `.asmdef`는 일관된 폴더 구조로 준비했다.
- 이 자료를 만드는 환경에는 Unity Editor가 설치되지 않아 실제 Unity 컴파일·PlayMode 실행은 확인하지 못했다. 사용 중인 Unity 버전의 Test Framework 패키지에 따라 test `.asmdef` 조정이 필요할 수 있다.
- GitHub Pages 게시와 CI 수행은 **사용자 GitHub 저장소의 설정·권한·라이선스**가 필요하며, 자료 안에 비밀 토큰을 포함하지 않는다.

## 학습 이후 다음 단계

이 문서의 14장까지 완료했다면 다음 기능을 실제 팀 프로젝트에 적용해 보자. 예를 들어 공격과 체력을 별도 담당자에게 분담하고, Contracts만 먼저 합의해 병합한 다음, 각자 Fake로 개발해 **통합 테스트가 있는 작은 PR**로 결합한다. 가장 중요한 평가는 '디자인 패턴을 몇 개 썼는가'가 아니라 **팀원이 상대 구현을 몰라도 기능을 개발·연결·검증할 수 있는가**다.
