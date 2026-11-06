#!/usr/bin/env python3
"""Analyze only pending records; keep successes, retry HTTP 429 at most twice."""
import argparse
import concurrent.futures as cf
import fcntl
import gzip
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'modules/top-ml/scripts'))
from analyze_full_corpus import analyze_pdf, write_success, write_failure


def download(url, path, max_mb=80):
    limit = max_mb * 1024 * 1024
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'AcademicWritingStudy/1.0'})
            started = time.monotonic()
            with urllib.request.urlopen(req, timeout=45) as res, path.open('wb') as dst:
                size = 0
                while chunk := res.read(1024 * 1024):
                    size += len(chunk)
                    if size > limit: raise ValueError(f'PDF exceeds {max_mb} MiB limit')
                    if time.monotonic() - started > 180: raise TimeoutError('download total time exceeded 180 seconds')
                    dst.write(chunk)
            with path.open('rb') as f:
                if f.read(4) != b'%PDF': raise ValueError('Response is not PDF')
            return
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 2: raise
            delay = exc.headers.get('Retry-After', '')
            delay = int(delay) if delay.isdigit() else (10, 30)[attempt]
            if delay > 60: raise
            time.sleep(max(1, delay))


def process(rec, temp_root, keep_root, keep_ids, max_mb):
    try:
        with tempfile.TemporaryDirectory(prefix=rec['paper_id']+'-', dir=temp_root) as td:
            pdf = Path(td) / 'paper.pdf'
            download(rec['pdf_url'], pdf, max_mb)
            analysis = analyze_pdf(pdf, rec)
            if keep_root and rec['paper_id'] in keep_ids:
                shutil.copy2(pdf, Path(keep_root) / (rec['paper_id']+'.pdf'))
            return analysis
    except Exception as exc:
        # HTTPError can contain an open response, which ProcessPool cannot pickle.
        return {'worker_error': {'type': type(exc).__name__,
                                 'message': str(exc)[:1000],
                                 'http_status': exc.code if isinstance(exc, urllib.error.HTTPError) else None}}


def snapshot(conn, dest, run):
    out = {'run': run, 'as_of_unix': time.time(), 'states': [list(r) for r in conn.execute('SELECT year,status,count(*) FROM papers GROUP BY year,status')]}
    dest.write_text(json.dumps(out, indent=2)+'\n')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--corpus', type=Path, required=True)
    ap.add_argument('--db', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=3, choices=range(1,5))
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--max-pdf-mb', type=int, default=80)
    ap.add_argument('--keep-ids', type=Path)
    ap.add_argument('--keep-dir', type=Path)
    args = ap.parse_args()
    lock = (args.db.parent/'stream.lock').open('a+')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    run = {'pid': os.getpid(), 'started_unix':time.time(), 'argv':sys.argv, 'retry':'Only HTTP 429, at most two retries; old errors excluded'}
    lock.seek(0); lock.truncate(); lock.write(json.dumps(run)); lock.flush()
    conn = sqlite3.connect(args.db)
    if conn.execute("SELECT count(*) FROM papers WHERE status='processing'").fetchone()[0]:
        raise SystemExit('Unresolved processing rows: inspect previous owner; no automatic reset.')
    pending = {r[0] for r in conn.execute("SELECT paper_id FROM papers WHERE status='pending'")}
    records = [json.loads(s) for s in gzip.open(args.corpus,'rt')]
    keep_ids = set(args.keep_ids.read_text().split()) if args.keep_ids else set()
    records = sorted((r for r in records if r['paper_id'] in pending), key=lambda r:(r['paper_id'] not in keep_ids, {'oral':0,'highlight':1,'poster':2}.get(r['presentation'],3),r['year'],r['paper_id']))
    if args.limit: records = records[:args.limit]
    temp = args.db.parent/'temporary-pdfs'; temp.mkdir(exist_ok=True)
    if args.keep_dir: args.keep_dir.mkdir(parents=True,exist_ok=True)
    progress = args.db.parent/'stream-progress.json'
    log = (args.db.parent/'stream-events.jsonl').open('a')
    print(json.dumps({'queued':len(records),'jobs':args.jobs,'retained_pdf_ids':len(keep_ids)}),flush=True)
    n, consecutive_failures, stopped = 0, 0, False
    iterator = iter(records)
    with cf.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = {}
        def submit():
            try: rec = next(iterator)
            except StopIteration: return
            conn.execute("UPDATE papers SET status='processing',updated_at=? WHERE paper_id=?",(int(time.time()),rec['paper_id'])); conn.commit()
            futures[pool.submit(process,rec,temp,args.keep_dir,keep_ids,args.max_pdf_mb)] = rec
        for _ in range(args.jobs): submit()
        while futures:
            done,_ = cf.wait(futures, timeout=30, return_when=cf.FIRST_COMPLETED)
            if not done:
                snapshot(conn,progress,run)
                continue
            for future in done:
                rec = futures.pop(future)
                event = {'paper_id':rec['paper_id'],'year':rec['year'],'time':time.time()}
                try:
                    result = future.result()
                    if 'worker_error' in result:
                        event['worker_error'] = result['worker_error']
                        raise RuntimeError(json.dumps(result['worker_error']))
                    write_success(conn,rec['paper_id'],result)
                    event.update(status='done',pdf_bytes=result['paper']['pdf_bytes'])
                    consecutive_failures = 0
                except Exception as exc:
                    status = write_failure(conn,rec['paper_id'],exc)
                    event.update(status=status,error=str(exc)[:1000])
                    consecutive_failures += 1
                log.write(json.dumps(event)+'\n'); log.flush()
                n += 1
                snapshot(conn,progress,run)
                if n % 25 == 0 or event['status'] != 'done':
                    print(json.dumps({'completed':n,'queued':len(records),**event}),flush=True)
                # Avoid turning a general outage into thousands of failed requests.
                if consecutive_failures >= 3 and not stopped:
                    stopped = True
                    print('Stopped new submissions after three consecutive failures; pending work preserved.',flush=True)
                if not stopped: submit()
    print(json.dumps(snapshot(conn,progress,run)),flush=True)
    log.close(); conn.close()


if __name__ == '__main__': main()
