#!/usr/bin/env python3
"""Fetch a deliberately selected reading set; extract page-indexed study text."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import pymupdf as fitz
from stream import download


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selection',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    textdir=args.output.parent/'study-text'; textdir.mkdir(exist_ok=True)
    log=args.output.parent/'study-acquisition.jsonl'
    existing={r['paper_id']:r for r in (json.loads(s) for s in log.read_text().splitlines())} if log.exists() else {}
    for rec in json.loads(args.selection.read_text()):
        pid=rec['paper_id']; path=args.output/(pid+'.pdf')
        if pid in existing and existing[pid]['status']=='error':
            print('Previous error retained: '+pid,flush=True); continue
        try:
            if not path.exists():
                with tempfile.TemporaryDirectory(dir=args.output) as td:
                    temp=Path(td)/'paper.pdf'; download(rec['pdf_url'],temp)
                    temp.replace(path)
            doc=fitz.open(path)
            layout=subprocess.run(['pdftotext',str(path),'-'],check=True,capture_output=True,text=True).stdout.split('\f')
            out='\n'.join(f'\n===== PDF PAGE {i+1} =====\n'+p for i,p in enumerate(layout) if p.strip())
            (textdir/(pid+'.txt')).write_text(out)
            item={'paper_id':pid,'status':'acquired_not_yet_read','pages':len(doc),'bytes':path.stat().st_size,'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pdf_url':rec['pdf_url']}
            doc.close()
        except Exception as exc:
            item={'paper_id':pid,'status':'error','error':str(exc)}
        with log.open('a') as f: f.write(json.dumps(item)+'\n')
        print(json.dumps(item),flush=True)


if __name__=='__main__': main()
