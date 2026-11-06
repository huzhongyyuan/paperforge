#!/usr/bin/env python3
"""Snapshot CVPR main proceedings and independently reconcile official labels."""
import argparse
import concurrent.futures
import datetime as dt
import gzip
import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'modules/top-ml/scripts'))
from collect_corpus import parse_cvf, clean, norm_title as original_norm_title


def norm_title(title):
    # CVF transliterates these glyphs in its public title text.
    # This is display normalization, not fuzzy title matching.
    return original_norm_title(title.replace('°', 'deg').replace('α', 'a').replace('β', 'b').replace('π', 'p'))


def retrieve(item, out):
    year, kind, url = item
    path = out / 'sources' / f'{year}-{kind}.html.gz'
    if path.exists():
        data = gzip.decompress(path.read_bytes())
    else:
        req = urllib.request.Request(url, headers={'User-Agent': 'CVPR-writing-study/1.0 (academic metadata)'})
        with urllib.request.urlopen(req, timeout=90) as response:
            data = response.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(gzip.compress(data, mtime=0))
    return year, kind, data.decode('utf-8'), {
        'year': year, 'kind': kind, 'url': url, 'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(), 'snapshot': str(path.name),
    }


def accepted_rows(page):
    rows = []
    for block in re.findall(r'<tr\b[^>]*>(.*?)</tr>', page, re.S | re.I):
        m = re.search(r'<strong\b[^>]*>(.*?)</strong>', block, re.S | re.I)
        if m:
            rows.append({'title': clean(m.group(1)), 'highlight': bool(re.search(r'title="Highlight"', block))})
    return rows


def oral_rows(page):
    return [clean(t) for t in re.findall(r'<h3\s+class="event-title">\s*<a\s+href="[^"]+">(.*?)</a>\s*</h3>', page, re.S | re.I)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    for y in (2024, 2025, 2026):
        jobs += [(y, 'proceedings', f'https://openaccess.thecvf.com/CVPR{y}?day=all'),
                 (y, 'oral', f'https://cvpr.thecvf.com/virtual/{y}/events/{"Oral" if y == 2026 else "oral"}')]
        if y == 2026:
            jobs += [(y, 'papers', 'https://cvpr.thecvf.com/virtual/2026/papers.html'),
                     (y, 'highlights', 'https://cvpr.thecvf.com/virtual/2026/events/Highlights2026')]
        else:
            jobs += [(y, 'accepted', f'https://cvpr.thecvf.com/Conferences/{y}/AcceptedPapers')]
    pages, sources, errors = {}, [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(retrieve, j, out): j for j in jobs}
        for future in concurrent.futures.as_completed(futures):
            try:
                y,k,page,source = future.result()
                pages[y,k] = page
                sources.append(source)
            except Exception as exc:
                errors.append({'source': futures[future], 'error': str(exc)})
    if errors:
        (out/'source-errors.json').write_text(json.dumps(errors, indent=2))
        raise SystemExit('Source fetch failed; no complete inventory emitted: '+str(errors))
    records, stats, unmatched = [], {}, {}
    for y in (2024, 2025, 2026):
        source = f'https://openaccess.thecvf.com/CVPR{y}?day=all'
        recs = parse_cvf(pages[y,'proceedings'], 'CVPR', y, source)
        if y == 2026:
            ht = {norm_title(t) for t in oral_rows(pages[y,'highlights'])}
            titles = [clean(t) for t in re.findall(r'<a\s+href="/virtual/2026/poster/\d+">(.*?)</a>', pages[y,'papers'], re.S)]
            ar = [{'title':t, 'highlight':norm_title(t) in ht} for t in titles]
            accepted_source = 'https://cvpr.thecvf.com/virtual/2026/papers.html'
        else:
            ar = accepted_rows(pages[y,'accepted'])
            accepted_source = f'https://cvpr.thecvf.com/Conferences/{y}/AcceptedPapers'
        ot = oral_rows(pages[y,'oral'])
        assert recs and ar and ot, f'Empty parse for {y}'
        ai = {norm_title(r['title']):r for r in ar}
        oi = {norm_title(t):t for t in ot}
        pi = {norm_title(r['title']):r for r in recs}
        assert len(pi)==len(recs), f'Duplicate proceedings titles {y}'
        for r in recs:
            n=norm_title(r['title'])
            r['paper_id']=hashlib.sha256(f"CVPR|{y}|{r['title']}".encode()).hexdigest()[:24]
            r['oral']=n in oi
            r['highlight']=ai.get(n,{}).get('highlight',False)
            r['label_verified']=n in ai or n in oi
            r['presentation']='oral' if r['oral'] else 'highlight' if r['highlight'] else 'poster' if n in ai else 'unknown'
            r['weight']={'oral':3,'highlight':2,'poster':1,'unknown':1}[r['presentation']]
            r['label_sources']=[accepted_source] if n in ai else []
            if y==2026 and r['highlight']: r['label_sources'].append('https://cvpr.thecvf.com/virtual/2026/events/Highlights2026')
            if n in oi:r['label_sources'].append(f'https://cvpr.thecvf.com/virtual/{y}/events/{"Oral" if y==2026 else "oral"}')
        stats[y]={'proceedings':len(recs),'accepted_rows':len(ar),'oral_listed':len(ot),
                  'highlight_icons':sum(r['highlight'] for r in ar),
                  'labels':{p:sum(r['presentation']==p for r in recs) for p in ['oral','highlight','poster','unknown']}}
        unmatched[y]={'oral_not_in_proceedings':[v for k,v in oi.items() if k not in pi],
                      'accepted_not_in_proceedings':[v for k,v in ai.items() if k not in pi],
                      'proceedings_not_in_accepted':[r['title'] for r in recs if norm_title(r['title']) not in ai]}
        records += recs
    payload=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records).encode()
    (out/'papers.jsonl.gz').write_bytes(gzip.compress(payload,mtime=0))
    manifest={'retrieved_at':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'CVPR 2024–2026 main-conference CVF proceedings; workshops excluded',
              'records':len(records),'years':stats,'sources':sorted(sources,key=lambda x:(x['year'],x['kind'])),
              'title_normalization':'NFKD alphanumeric with °→deg, α→a, β→b, π→p display equivalents; no fuzzy matches',
              'weighting':{'oral':3,'highlight':2,'poster':1,'unknown':1},'corpus_sha256':hashlib.sha256(payload).hexdigest()}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (out/'unmatched.json').write_text(json.dumps(unmatched,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'records':len(records),'years':stats,'unmatched_counts':{y:{k:len(v) for k,v in items.items()} for y,items in unmatched.items()}},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
