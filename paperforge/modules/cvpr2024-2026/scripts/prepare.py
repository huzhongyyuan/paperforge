#!/usr/bin/env python3
"""Seed an isolated analysis DB and reuse successful exact-URL legacy features."""
import argparse
import collections
import datetime as dt
import gzip
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'modules/top-ml/scripts'))
from analyze_full_corpus import init_db, seed_db, ANALYZER_VERSION


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', type=Path, required=True)
    ap.add_argument('--db', type=Path, required=True)
    ap.add_argument('--legacy-db', type=Path, required=True)
    args = ap.parse_args()
    records = [json.loads(s) for s in gzip.open(args.corpus, 'rt')]
    conn = sqlite3.connect(args.db) if args.db.exists() else init_db(args.db)
    conn.row_factory = sqlite3.Row
    if conn.execute("SELECT COUNT(*) FROM papers WHERE status='processing'").fetchone()[0]:
        raise SystemExit('Active/stale processing rows found; inspect owner before preparing again.')
    seed_db(conn, records)
    conn.execute('CREATE TABLE IF NOT EXISTS provenance(paper_id TEXT PRIMARY KEY, kind TEXT, source TEXT, source_paper_id TEXT, source_updated_at INTEGER, note TEXT)')
    old = sqlite3.connect(f'file:{args.legacy_db}?mode=ro', uri=True)
    old.row_factory = sqlite3.Row
    lookup = {(r['year'], r['title'], r['pdf_url']): r for r in old.execute("SELECT * FROM papers WHERE conference='CVPR'")}
    counters = collections.Counter()
    for rec in records:
        pid = rec['paper_id']
        if conn.execute('SELECT 1 FROM provenance WHERE paper_id=?',(pid,)).fetchone():
            counters['already_prepared'] += 1
            continue
        prev = lookup.get((rec['year'], rec['title'], rec['pdf_url']))
        if prev and prev['status'] == 'done' and prev['analyzer_version'] == ANALYZER_VERSION:
            fields = ['status','attempts','analyzer_version','pdf_bytes','pdf_sha256','pages','word_count','section_count','figure_count','table_count','image_object_count','error','updated_at']
            conn.execute('UPDATE papers SET '+','.join(f'{f}=?' for f in fields)+' WHERE paper_id=?', [prev[f] for f in fields]+[pid])
            for table in ['sections','visuals']:
                rows = old.execute(f'SELECT * FROM {table} WHERE paper_id=?',(prev['paper_id'],)).fetchall()
                if rows:
                    conn.executemany(f'INSERT INTO {table} VALUES('+','.join('?' for _ in rows[0])+')', [[pid]+list(row)[1:] for row in rows])
            kind, note = 'reused_success', 'Exact year, title, PDF URL and analyzer version match; no PDF refetch.'
        elif prev and prev['status'] == 'error' and '429' not in (prev['error'] or ''):
            kind, note = 'legacy_non429_error', prev['error']
            conn.execute("UPDATE papers SET status='held_legacy_error', error=? WHERE paper_id=?",(note,pid))
        else:
            kind, note = 'new_pending', 'No reusable successful analysis; fresh extraction eligible.'
        counters[kind] += 1
        conn.execute('INSERT INTO provenance VALUES(?,?,?,?,?,?)',(pid,kind,str(args.legacy_db) if prev else None,prev['paper_id'] if prev else None,prev['updated_at'] if prev else None,note))
    conn.commit()
    report = {'as_of':dt.datetime.now(dt.timezone.utc).isoformat(), 'source_read_only':str(args.legacy_db), 'rows':len(records),'actions':dict(counters), 'states':[list(row) for row in conn.execute('SELECT year,status,count(*) FROM papers GROUP BY year,status')]}
    (args.db.parent/'prepare-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    old.close(); conn.close()


if __name__ == '__main__': main()
