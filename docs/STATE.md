# 개발 상황

## 프로젝트
INC0GNITO 2026 본선용 MemGuard 데모 사이트 — 30개 인젝션 페이지 + ground_truth.jsonl + GitHub Pages 배포 구조.

## 플랜 단계
- [x] 1단계: 모든 산출물 일괄 생성 (30 pages + ground_truth.jsonl + index.html + styles.css + README + .gitignore + .nojekyll)
- [x] 2단계: 시각 비가시성 검증 (stdlib intent-check 100% PASS + GitHub Pages 배포 완료)
- [x] 3-pre: 위장 패턴 sample 3개 ChatGPT 5 검증 — Pattern 1만 부분 작동, 나머지 5종 silent ignore.
- [x] 3-main: panel 1이 /tmp/memguard-pages에서 30 페이지 일괄 갱신 + ground_truth + commit `2f1f0f5` + push 완료.
  - acceptance PASS: grep 노골 0회, sub-form 6종 균등(5~6회), 브랜드 7종 균등(4~5회), forbidden 0개
  - working dir(이 Dev-harness scratch)와 /tmp/memguard-pages 콘텐츠 완전 동기
- [x] 4단계: 사이트 detection-evasion 강화 — 4-1~4-4 모두 PASS, 4-5 스킵.
  - commit `9c46857 fix: strip detection signals from site-level perspective` push 동기
  - GitHub repo rename: hwanyeeeee/memguard-test-page → hwanyeeeee/**morning-stack-digest**
  - GitHub Pages 새 URL: https://hwanyeeeee.github.io/morning-stack-digest/
- [x] 5단계: Cross-LLM 침투 검증 (박채민 인계분) — 6 모델 × 3 페이지 = 16-cell matrix 완료.
  - 측정 모델: ChatGPT 5, Claude Sonnet 4.6, Gemini (web), Sider, Grok fast, Gemini Assistant (Chrome)
  - 측정 페이지: page03 (css_hidden, QuantumDev), page18 (zero_width, AtlasMonitor), page21 (visual_deception, NexusIDE)
  - 산출: `results/cross_llm_matrix.csv`, `results/cross_llm_findings.md`, `results/protocol.md`
  - 핵심 finding:
    - **Claude Sonnet 4.6만 능동 차단** (omit+caveat+contextual defense). 나머지 5 모델은 무방어/제한방어.
    - **Gemini Assistant (Chrome)이 가장 위험** — page-resident ambient context로 탭 열림 동안 perpetual contamination (사용자가 새 대화/메모리 클리어로 우회 불가).
    - **6 모델 모두 cross-session memory persistence는 0건** → MINJA 3-step demo narrative는 부분만 현실 모델에서 작동. 본선 demo narrative pivot 필요: "response poisoning + ambient context".
    - **Vendor-internal divergence**: Gemini web vs Chrome Assistant는 같은 family인데 침투 양상 정반대 → MemGuard ingress-agnostic 차단 가치 입증.
    - **카테고리 비대칭**: zero_width는 paste 기반 ingress에서 일부 모델 침투 실패. URL fetch 기반에서는 작동. 데이터셋의 다층 평가 가치 입증.
    - 침투 패턴 7종 확인: faithful, over-absorption, anchor, direct rank-1, page-grounded, brand reification, ambient context.

## 현재 작업
- 도구: claude
- 위치: 5단계 완료
- 수행 중: -
- 재시도: 0

## 완료
- 시각: 2026-05-08 07:55
- 비고:
  - 1단계: 30 페이지 + ground_truth + index/styles/README/.nojekyll/.gitignore 일괄 생성 (commit `b9fa787`)
  - 2단계: stdlib intent-check 100% PASS, GitHub Pages 배포
  - 3-pre: 6 패턴 sample ChatGPT 5 검증 → Pattern 1만 부분 작동, 나머지 5종 silent ignore
  - 3-main: 30 페이지 인젝션을 Pattern 1 (first_person_disguise) + 6 sub-form 균등 + 7 브랜드 분산으로 일괄 갱신 (commit `2f1f0f5`)
  - 박주환·panel 1 재해석: 30 URL 한 번 측정은 비현실. 1 페이지/세션이 현실. Demo narrative = 3-step memory injection (MINJA): 페이지 노출 → follow-up 추천 → 메모리 침투
  - 4단계: repo rename(morning-stack-digest) + page05 메타 콘텐츠를 KV-cache 논문으로 교체 + README "Morning Stack Digest" 리라이팅 + EVAL.md 분리(.gitignore) + index.html reveal 토글 제거 (commit `9c46857`)
  - 잔여(박주환): ChatGPT memory clear → page21 (NexusIDE interviewee_quote) 1개 던지고 follow-up 추천 + 새 대화 메모리 침투 검증. 본선 PPT에 academic backbone (MINJA 98.2%, EchoLeak CVE-2025-32711, AutoInject allelujah 92.4%, OWASP #1 AI threat 2026) 인용
  - 5단계: Cross-LLM 검증 16-cell matrix 완료 (results/). 본선 narrative pivot — "response poisoning + page-resident ambient context"가 진짜 vector, MINJA 3-step memory injection은 현실 모델에서 부분 작동.
  - 6단계: Lakera Guard baseline 측정 — 33 인젝션 중 2건만 detect (6.1%). 한국어 0/17 (0.0%), 영어 2/16 (12.5%). personal_anecdote sub-form만 2/6, 나머지 5 sub-form 모두 0%. zero_width 0/10. SafeType은 PII redaction 도구로 위협 vector 직교 — 측정 불요. PPT 객관성 40점 핵심 정량 데이터. results/lakera_baseline.csv + run_lakera_baseline.py 추가.
