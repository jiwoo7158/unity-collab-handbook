# Unity 팀 코드 협업 기술 핸드북

**인터페이스 · 델리게이트 · 이벤트 · DTO · DI · Adapter/Facade · Assembly Definition · 테스트 · GitHub 협업**을 같은 Unity 전투 예제로 학습하는 정적 문서 사이트입니다.

## 바로 보기

- **오프라인:** `docs/index.html` 파일을 브라우저로 엽니다. HTML/CSS/JS가 모두 저장소 안에 있어 별도 빌드가 필요 없습니다.
- **GitHub Pages:** GitHub 저장소에 업로드 후 `Settings > Pages > Build and deployment > Deploy from a branch > main /docs > Save`를 선택합니다. 저장소의 공개 주소 형식은 보통 `https://<사용자>.github.io/<저장소>/`입니다.
- **유니티 실습:** [`unity-example/README.md`](unity-example/README.md)를 읽고 `unity-example/Assets/_Game/`를 새 Unity 6 프로젝트에 복사합니다.

## 저장소 구조

```text
content/                 원본 Markdown (17장)
docs/                    GitHub Pages에 그대로 게시할 완성 HTML
  assets/                로컬 CSS/JS
scripts/build_site.py    Markdown → 정적 HTML 사이트 생성기
unity-example/           Unity 6 프로젝트에 복사할 학습 코드
.github/                 이슈/PR 템플릿
```

## 문서 수정

Python 3과 `markdown-it-py`, `Pygments` 라이브러리가 필요합니다.

```bash
python -m pip install -r requirements-docs.txt
python scripts/build_site.py
```

`.md`를 수정한 뒤 빌드 스크립트를 실행하고, `content/`와 `docs/` 둘 다 커밋합니다. `python scripts/validate_repo.py`로 장별 링크와 `.asmdef` 참조 그래프도 확인할 수 있습니다. 정적 사이트는 외부 CDN과 Node.js 빌드에 의존하지 않습니다. GitHub Actions의 `docs-check.yml`은 문서 생성 및 참조 관계를 자동 검증하며 Unity 에디터 라이선스를 요구하지 않습니다.

## GitHub 초기 업로드 예시

```bash
git init
git add .
git commit -m "docs: publish Unity collaboration handbook"
git branch -M main
git remote add origin https://github.com/YOUR_ID/YOUR_REPO.git
git push -u origin main
```

`YOUR_ID`와 `YOUR_REPO`는 본인의 GitHub 사용자명/저장소명으로 바꿉니다. 기존 원격 저장소가 있다면 `git init`/`remote add`를 무작정 다시 실행하지 않습니다.

> **한계:** Unity 에디터 자체는 이 환경에서 실행 검증하지 못했으므로, 샘플은 실제 Unity 6 프로젝트에서 컴파일 및 테스트 결과를 확인해야 합니다. `unity-example`은 독립 실행 가능한 완전한 Unity 프로젝트가 아니라 새 프로젝트에 복사할 `Assets` 실습 묶음입니다. Unity가 처음 가져오면서 만든 `.meta` 파일은 이후 팀 저장소에 원본 에셋과 함께 커밋해야 GUID 참조가 유지됩니다.
