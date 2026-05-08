#!/usr/bin/env python3
"""
Lakera Guard baseline: 30 페이지 인젝션 텍스트를 Lakera Guard v2 API에 던져
detection rate 측정. 결과를 results/lakera_baseline.csv 로 저장.

Usage:
    export LAKERA_API_KEY='<your_key>'
    python3 results/run_lakera_baseline.py

Output columns:
    page_id, category, brand, sub_form, type, content_preview,
    flagged, prompt_attack_score, latency_ms
"""
import os, sys, json, csv, time, urllib.request, urllib.error

API_KEY = os.environ.get('LAKERA_API_KEY', '').strip()
if not API_KEY:
    print('ERROR: LAKERA_API_KEY not set. export LAKERA_API_KEY=<key> first.', file=sys.stderr)
    sys.exit(1)

ENDPOINT = 'https://api.lakera.ai/v2/guard'
GT_PATH = 'ground_truth.jsonl'
OUT_PATH = 'results/lakera_baseline.csv'

def call_lakera(text: str) -> tuple[bool, float, int]:
    """Returns (flagged, prompt_attack_score, latency_ms)."""
    body = json.dumps({'messages': [{'role': 'user', 'content': text}]}).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
        },
        method='POST',
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')[:200]
        print(f'  HTTP {e.code}: {body}', file=sys.stderr)
        return (False, -1.0, int((time.time() - t0) * 1000))
    latency = int((time.time() - t0) * 1000)
    flagged = bool(data.get('flagged', False))
    pa_score = -1.0
    for cat, info in (data.get('categories') or {}).items():
        if cat in ('prompt_attack', 'prompt_injection') and isinstance(info, dict):
            pa_score = float(info.get('detected', info.get('score', 0)) or 0)
            break
    if pa_score < 0:
        results = data.get('results') or []
        if results and isinstance(results[0], dict):
            cats = results[0].get('categories') or {}
            scores = results[0].get('category_scores') or {}
            for k in ('prompt_attack', 'prompt_injection'):
                if k in scores:
                    pa_score = float(scores[k])
                    break
    return (flagged, pa_score, latency)

def main():
    pages = [json.loads(l) for l in open(GT_PATH, encoding='utf-8')]
    rows = []
    print(f'measuring {sum(len(p["injections"]) for p in pages)} injections across {len(pages)} pages...')
    for p in pages:
        for inj in p['injections']:
            content = inj['content']
            pat_tokens = inj['pattern'].split('+')
            sub_form = next((t for t in pat_tokens if t in {
                'ps','author_postscript','interviewee_quote',
                'comment_quote','personal_anecdote','byline'}), '')
            brand = next((t.replace('brand_', '') for t in pat_tokens if t.startswith('brand_')), '')
            flagged, score, latency = call_lakera(content)
            rows.append({
                'page_id': p['id'],
                'category': p['category'],
                'brand': brand,
                'sub_form': sub_form,
                'type': inj['type'],
                'content_preview': content[:80].replace('\n', ' '),
                'flagged': flagged,
                'prompt_attack_score': score,
                'latency_ms': latency,
            })
            print(f'  {p["id"]:6s} {inj["type"]:25s} flagged={flagged} score={score:.3f} ({latency}ms)')
            time.sleep(0.3)  # gentle rate limit

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    flagged_n = sum(1 for r in rows if r['flagged'])
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r['category'], [0, 0])
        by_cat[r['category']][0] += 1
        by_cat[r['category']][1] += int(bool(r['flagged']))

    print(f'\n=== Lakera Guard baseline ===')
    print(f'total injections: {n}')
    print(f'flagged: {flagged_n} ({flagged_n*100/n:.1f}%)')
    print(f'by category:')
    for c, (tot, fl) in sorted(by_cat.items()):
        print(f'  {c:20s} {fl}/{tot} ({fl*100/tot:.1f}%)')
    print(f'\nfull csv: {OUT_PATH}')

if __name__ == '__main__':
    main()
