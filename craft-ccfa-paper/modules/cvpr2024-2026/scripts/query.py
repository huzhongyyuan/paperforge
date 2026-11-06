#!/usr/bin/env python3
"""Offline discovery, reading scopes and descriptive CVPR features; no network."""
import argparse
import gzip
import json
from pathlib import Path

MODULE=Path(__file__).resolve().parents[1]
REF=MODULE/'references'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=('search','cards','stats','features'))
    ap.add_argument('--year',type=int,choices=(2024,2025,2026))
    ap.add_argument('--presentation',choices=('oral','highlight','poster','unknown'))
    ap.add_argument('--query',default='',help='Case-insensitive literal title substring')
    ap.add_argument('--id',dest='paper_id')
    ap.add_argument('--metric',help='Exact metric key; with stats only')
    ap.add_argument('--limit',type=int,default=10)
    a=ap.parse_args()
    if a.limit<1 or a.limit>100: ap.error('--limit must be between 1 and 100')
    if a.mode=='stats':
        if a.query or a.paper_id: ap.error('Stats groups are year/presentation only')
        p=REF/'corpus/statistics.json'
        if not p.exists(): ap.error('No exported statistics; do not infer extraction completion')
        d=json.loads(p.read_text())
        key='/'.join(([f'year:{a.year}'] if a.year else [])+([f'presentation:{a.presentation}'] if a.presentation else [])) or 'all'
        group=d['groups'][key]
        out={k:d[k] for k in ('as_of','extraction_state','weights','unknown_label_policy','aggregation','feature_scope','quality_diagnostics')}
        out['group']=key; out['counts']={k:v for k,v in group.items() if k!='metrics'}
        if a.metric:
            if a.metric not in group['metrics']: ap.error('Metric not detected in this group; use stats to list keys')
            out['metric']={a.metric:group['metrics'][a.metric]}
        else: out['available_metrics']=sorted(group['metrics'])
    else:
        if a.metric: ap.error('--metric is only for stats')
        if a.mode=='cards':
            records=json.loads((REF/'reading-ledger.json').read_text())
        else:
            name='features-paper.jsonl.gz' if a.mode=='features' else 'papers.jsonl.gz'
            path=REF/'corpus'/name
            if not path.exists(): ap.error('No exported '+name)
            with gzip.open(path,'rt') as f: records=[json.loads(s) for s in f]
        records=[r for r in records if (not a.year or r['year']==a.year)
                 and (not a.presentation or r['presentation']==a.presentation)
                 and (not a.paper_id or r['paper_id']==a.paper_id)
                 and a.query.casefold() in r['title'].casefold()]
        records.sort(key=lambda r:({'oral':0,'highlight':1,'poster':2}.get(r['presentation'],3),-r['year'],r['title']))
        if a.mode=='search':
            keys=('paper_id','year','title','presentation','paper_url','pdf_url','label_verified')
            records=[{k:r.get(k) for k in keys} for r in records]
        out={'mode':a.mode,'matches':len(records),'returned':min(len(records),a.limit),'records':records[:a.limit],
             'interpretation':'Metadata is discovery only; cards record actual bounded reading. Features are heuristic extraction, not semantic reading.'}
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
