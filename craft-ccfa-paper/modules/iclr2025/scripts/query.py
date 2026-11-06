#!/usr/bin/env python3
"""Search the complete official ICLR 2025 main-conference metadata snapshot."""
import argparse,gzip,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('query',nargs='?',default='')
p.add_argument('--topic',default='')
p.add_argument('--presentation',choices=['oral','spotlight','poster'])
p.add_argument('--limit',type=int,default=10)
p.add_argument('--abstract',action='store_true')
p.add_argument('--phrase',action='store_true',help='Match the entire query as a contiguous phrase, instead of separate AND terms.')
p.add_argument('--evidence',action='store_true',help='Show extraction status, detected headings and a bounded caption sample; not semantic close reading.')
p.add_argument('--captions',type=int,default=5,help='Maximum extracted captions per result with --evidence.')
a=p.parse_args()
corpus=Path(__file__).resolve().parents[1]/'corpus'
with gzip.open(corpus/'papers.jsonl.gz','rt') as f:rows=[json.loads(l) for l in f]
terms=[a.query.casefold()] if a.phrase else a.query.casefold().split()
hits=[r for r in rows if all(t in ' '.join(str(r.get(k) or '') for k in ['title','abstract','authors']).casefold() for t in terms) and a.topic.casefold() in str(r.get('topic') or '').casefold() and (not a.presentation or r['presentation']==a.presentation)]
selected=hits[:max(0,a.limit)]
def paper_id(r):
 return hashlib.sha256(f'{r["conference"]}|{r["year"]}|{r["title"]}'.encode()).hexdigest()[:24]
evidence={paper_id(r):{'status':'snapshot_unavailable','sections':[],'captions':[],'detected_caption_count':0} for r in selected}
if a.evidence:
 for filename,kind in [('paper-status.jsonl.gz','status'),('sections.jsonl.gz','sections'),('figures.jsonl.gz','captions')]:
  if not (corpus/filename).exists():continue
  with gzip.open(corpus/filename,'rt') as f:
   for line in f:
    item=json.loads(line);entry=evidence.get(item['paper_id'])
    if entry is None:continue
    if kind=='status':
     entry.update({k:item.get(k) for k in ['status','analyzer_version','pdf_sha256','error']})
    elif kind=='sections':
     entry['sections'].append({k:item.get(k) for k in ['section_order','heading','category','page_start','page_end']})
    else:
     entry['detected_caption_count']+=1
     if len(entry['captions'])<max(0,a.captions):
      entry['captions'].append({k:item.get(k) for k in ['kind','label','page','caption']})
 for entry in evidence.values():
  entry['sections'].sort(key=lambda x:x['section_order'])
  entry['meaning']='Automatic extraction only; headings/captions may be missing or misassigned. Check the linked PDF for scientific claims.'
print(json.dumps({'snapshot':'2026-09-18','scope':'main conference events, reconciled with proceedings','total':len(rows),'matches':len(hits),'search_mode':'phrase' if a.phrase else 'AND substrings'},ensure_ascii=False))
for r in selected:
 out={k:r.get(k) for k in ['title','authors','topic','presentation','paper_url','openreview_url','pdf_url','in_proceedings']}
 if a.abstract:out['abstract']=r['abstract']
 if a.evidence:out['extraction']=evidence[paper_id(r)]
 print(json.dumps(out,ensure_ascii=False))
