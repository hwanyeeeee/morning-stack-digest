# MemGuard Test Pages

30개의 프롬프트 인젝션 데모 페이지 데이터셋. INC0GNITO 2026 본선(한국정보보호학회 주관)에서 MemGuard Chrome Extension의 객관적 성능 측정에 사용됩니다.

**MemGuard**는 악의적 웹 페이지가 ChatGPT·Claude 등 AI 어시스턴트의 장기 메모리를 오염시키는 공격(MINJA 유형, 피해자 인지율 0%)을 탐지·차단하는 Chrome Extension입니다.

---

## 디렉토리 구조

```
memguard-test-page/
├── index.html               # 30개 카드 그리드 (카테고리 라벨 기본 숨김)
├── styles.css               # 공통 스타일 (외부 의존 0)
├── pages/
│   ├── page01.html ~ page30.html
├── ground_truth.jsonl       # 30-line NDJSON, 인젝션 메타데이터
├── README.md
├── .nojekyll
└── .gitignore
```

---

## 데이터셋 구성

| 카테고리 | 범위 | 기법 |
|---|---|---|
| `css_hidden` | page01–10 | `display:none`, `visibility:hidden`, `font-size:0`, `height:0+overflow:hidden`, `clip-path:inset(100%)` |
| `zero_width` | page11–20 | ZWSP (U+200B), ZWNJ (U+200C), ZWJ (U+200D), BOM (U+FEFF) |
| `visual_deception` | page21–30 | `color:white`, `position:absolute;left:-9999px`, `color:#ffffff`, `opacity:0`, `transform:scale(0)` |

언어 분배: 한국어 15개 / 영어 15개  
인젝션 패턴: `memory_persist`, `recommendation_bias`, `system_masquerade`, `override`, `multi_step_chain` (각 6–7회)

---

## 사용법 — 평가 스크립트

### 기본 검증 (acceptance test)

```python
import json, os

pages = [json.loads(l) for l in open('ground_truth.jsonl')]
assert len(pages) == 30
assert all(os.path.isfile(p['filename']) for p in pages)
assert {p['language'] for p in pages} == {'ko', 'en'}
assert {p['category'] for p in pages} == {'css_hidden', 'zero_width', 'visual_deception'}
print("OK:", len(pages), "pages validated")
```

### BeautifulSoup 셀렉터 검증 (CSS hidden / visual deception)

```python
from bs4 import BeautifulSoup
import json

for line in open('ground_truth.jsonl'):
    page = json.loads(line)
    if page['category'] == 'zero_width':
        continue
    soup = BeautifulSoup(open(page['filename']).read(), 'html.parser')
    for inj in page['injections']:
        el = soup.select_one(inj['selector'])
        assert el is not None, f"selector not found: {inj['selector']} in {page['filename']}"
        assert inj['content'] in el.get_text(), f"content mismatch in {page['filename']}"
print("All CSS/visual selectors verified")
```

### GitHub Pages URL 기준 평가 (원격)

```python
import requests, json

BASE = "https://[USERNAME].github.io/memguard-test-page"

for line in open('ground_truth.jsonl'):
    page = json.loads(line)
    url = f"{BASE}/{page['filename']}"
    r = requests.get(url, timeout=10)
    assert r.status_code == 200, f"HTTP {r.status_code}: {url}"
print("All 30 pages reachable")
```

---

## 시연 영상

MemGuard 시연은 아래 URL 형식으로 접근합니다 (`[USERNAME]`을 본인 GitHub 사용자명으로 교체):

```
https://[USERNAME].github.io/memguard-test-page/pages/page01.html
```

카테고리 라벨을 표시하려면:

```
https://[USERNAME].github.io/memguard-test-page/?reveal=true
```

---

## GitHub Pages 활성화

1. 이 레포지토리를 GitHub에 push합니다.
2. GitHub 레포 → **Settings** → **Pages**
3. Source: `Deploy from a branch` → Branch: `main` / `(root)` → **Save**
4. 약 5분 후 `https://[USERNAME].github.io/memguard-test-page/` 접속 확인

---

## 라이선스

MIT
