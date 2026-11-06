#!/usr/bin/env python3
"""Export a consistent read-only SQLite snapshot; no downloads or retries."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import sqlite3

WEIGHTS = {'oral': 3, 'highlight': 2, 'poster': 1}
MODULE = Path(__file__).resolve().parents[1]


def distribution(pairs):
    pairs = sorted((float(v), float(w)) for v, w in pairs
                   if v is not None and w > 0 and math.isfinite(float(v)))
    if not pairs:
        return {'n_papers': 0, 'weight_sum': 0}
    total = sum(w for _, w in pairs)
    def q(f):
        cumulative = 0
        for v, w in pairs:
            cumulative += w
            if cumulative >= total * f: return v
        return pairs[-1][0]
    return {'n_papers': len(pairs), 'weight_sum': total,
            'mean': sum(v*w for v, w in pairs)/total,
            'p25': q(.25), 'median': q(.5), 'p75': q(.75),
            'min': pairs[0][0], 'max': pairs[-1][0]}


def write_jsonl(path, rows):
    with path.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0) as gz:
        for row in rows:
            gz.write((json.dumps(row, ensure_ascii=False, separators=(',', ':'))+'\n').encode())
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_snapshot(db):
    conn = sqlite3.connect(db.resolve().as_uri()+'?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA query_only=ON')
    conn.execute('BEGIN')
    rows = {table: [dict(r) for r in conn.execute('SELECT * FROM '+table)]
            for table in ('papers', 'sections', 'visuals', 'provenance')}
    conn.rollback(); conn.close()
    return rows


def make_features(rows):
    sections = defaultdict(lambda: defaultdict(Counter))
    visuals = defaultdict(lambda: defaultdict(list))
    compact_sections, compact_visuals = [], []
    for s in rows['sections']:
        rec = {k:v for k,v in s.items() if k != 'role_counts_json'}
        rec['regex_role_counts'] = json.loads(s['role_counts_json'] or '{}')
        compact_sections.append(rec)
        agg = sections[s['paper_id']][s['category']]
        agg['detected_blocks'] += 1
        for k in ('word_count','sentence_count','paragraph_count','citation_mentions',
                  'figure_mentions','table_mentions','equation_mentions',
                  'first_person_mentions','hedge_mentions','strong_claim_mentions',
                  'contribution_cues','limitation_cues'):
            agg[k] += s[k] or 0
    for v in rows['visuals']:
        signals = json.loads(v['caption_signals_json'] or '{}')
        geometry = json.loads(v['visual_json'] or '{}')
        rec = {k:v[k] for k in ('paper_id','visual_order','kind','label','page','figure_type','image_object_count')}
        rec.update(caption_signals=signals, inferred_visual_proxy=geometry)
        compact_visuals.append(rec)
        visuals[v['paper_id']][v['kind']].append(rec)
    features = []
    provenance = {p['paper_id']:p for p in rows['provenance']}
    for p in sorted(rows['papers'], key=lambda r:(r['year'],r['paper_id'])):
        f = dict(p)
        f['presentation_weight'] = WEIGHTS.get(p['presentation'],0)
        f['provenance'] = provenance.get(p['paper_id'],{})
        f['quality_flags'] = (['low_extracted_word_count_under_1000']
                              if p['status']=='done' and (p['word_count'] or 0)<1000 else [])
        f['metrics'] = {k:p[k] for k in ('pages','word_count','section_count','figure_count','table_count','image_object_count')}
        for cat, val in sections[p['paper_id']].items():
            for k,v in val.items(): f['metrics'][f'section.{cat}.{k}'] = v
            if val['sentence_count']:
                f['metrics'][f'section.{cat}.words_per_detected_sentence'] = val['word_count']/val['sentence_count']
            if val['word_count']:
                for k in ('citation_mentions','first_person_mentions','hedge_mentions','strong_claim_mentions'):
                    f['metrics'][f'section.{cat}.{k}_per_1000_words'] = 1000*val[k]/val['word_count']
        for kind, group in visuals[p['paper_id']].items():
            f['metrics'][f'visual.{kind}.detected_count'] = len(group)
            types = Counter(v['figure_type'] for v in group)
            for typ, count in types.items(): f['metrics'][f'visual.{kind}.type.{typ}.count'] = count
            for key in ('word_count','sentence_count','subfigure_count','has_takeaway','has_comparison','has_protocol','defines_panels'):
                vals = [v['caption_signals'][key] for v in group if isinstance(v['caption_signals'].get(key),(int,float))]
                if vals: f['metrics'][f'visual.{kind}.caption.{key}.paper_mean'] = sum(vals)/len(vals)
            for key in ('white_fraction','colorfulness','contrast','edge_density','width_page_fraction','height_page_fraction'):
                vals = [v['inferred_visual_proxy'][key] for v in group if isinstance(v['inferred_visual_proxy'].get(key),(int,float))]
                if vals: f['metrics'][f'visual.{kind}.proxy.{key}.paper_mean'] = sum(vals)/len(vals)
        features.append(f)
    return features, compact_sections, compact_visuals


def summarize_group(rows, metric_names):
    done = [p for p in rows if p['status']=='done']
    out = {'total':len(rows), 'states':dict(Counter(p['status'] for p in rows)),
           'presentations':dict(Counter(p['presentation'] for p in rows)),
           'extracted':len(done), 'weighted_extracted_papers':sum(p['presentation_weight']>0 for p in done),
           'extracted_weight_sum':sum(p['presentation_weight'] for p in done), 'metrics':{}}
    for key in metric_names:
        vals = [p for p in done if p['metrics'].get(key) is not None]
        if not vals: continue
        weight_sum = sum(p['presentation_weight'] for p in vals)
        den = out['extracted_weight_sum']
        out['metrics'][key] = {
            'unweighted':distribution([(p['metrics'][key],1) for p in vals]),
            'weighted_3_2_1':distribution([(p['metrics'][key],p['presentation_weight']) for p in vals]),
            'detected_paper_fraction':len(vals)/len(done) if done else None,
            'weighted_detected_fraction':weight_sum/den if den else None}
    return out


def export(db, corpus, outdir):
    rows = load_snapshot(db)
    official = [json.loads(s) for s in gzip.open(corpus,'rt')]
    ids = {p['paper_id'] for p in official}
    if len(ids)!=len(official) or ids!={p['paper_id'] for p in rows['papers']}:
        raise ValueError('Corpus / DB IDs do not match exactly')
    meta = {p['paper_id']:p for p in official}
    for p in rows['papers']:
        m=meta[p['paper_id']]
        if any(p[k]!=m[k] for k in ('year','title','presentation','pdf_url')):
            raise ValueError('Metadata mismatch: '+p['paper_id'])
    features, sections, visuals = make_features(rows)
    done_ids = {p['paper_id'] for p in features if p['status']=='done'}
    if any(s['paper_id'] not in done_ids for s in sections+visuals):
        raise ValueError('Feature rows outside successful papers')
    names=sorted({k for p in features if p['status']=='done' for k in p['metrics']})
    groups={'all':features}
    for year in sorted({p['year'] for p in features}):
        groups[f'year:{year}']=[p for p in features if p['year']==year]
    for label in sorted({p['presentation'] for p in features}):
        groups[f'presentation:{label}']=[p for p in features if p['presentation']==label]
        for year in (2024,2025,2026):
            groups[f'year:{year}/presentation:{label}']=[p for p in features if p['year']==year and p['presentation']==label]
    outdir.mkdir(parents=True,exist_ok=True)
    hashes={}
    for filename,data in (('features-paper.jsonl.gz',features),('features-section.jsonl.gz',sections),('features-visual.jsonl.gz',visuals)):
        hashes[filename]=write_jsonl(outdir/filename,data)
    unfinished=sum(p['status'] in ('pending','processing') for p in features)
    report={
        'schema_version':1, 'as_of':datetime.now(timezone.utc).isoformat(),
        'extraction_state':'in_progress' if unfinished else 'finished_with_gaps' if len(done_ids)<len(features) else 'finished',
        'corpus_sha256':hashlib.sha256(gzip.decompress(corpus.read_bytes())).hexdigest(),
        'corpus_gzip_sha256':hashlib.sha256(corpus.read_bytes()).hexdigest(),
        'hash_scope':'corpus_sha256 hashes uncompressed JSONL, as in manifest.json; corpus_gzip_sha256 and artifact_sha256 hash file bytes.',
        'weights':WEIGHTS, 'unknown_label_policy':'Included unweighted; excluded weighted. Overrides metadata manifest fallback unknown=1.',
        'aggregation':'Paper-weighted pooled years, not year-equal. Section values sum detected category blocks within a paper. Visual values average detections within a paper, then aggregate papers. Quantiles use inverse empirical CDF.',
        'feature_scope':'Heuristic PDF extraction including references and possible appendices; not semantic reading or validated main-text counts. Done means extractor completed, not text-quality approval. Caption flags, rhetorical regex and visual proxies are unvalidated heuristics, not aesthetic scores. Metrics are conditional on detection: an absent category is missing, not a measured zero.',
        'quality_diagnostics':{
            'policy':'Flag successful records with fewer than 1000 extracted words for inspection; threshold is a screening heuristic, not a validated acceptance rule. All done records remain in raw distributions; flags are not silently removed.',
            'flagged_papers':sum(bool(p['quality_flags']) for p in features),
            'paper_ids':[p['paper_id'] for p in features if p['quality_flags']]},
        'feature_rows':{'papers':len(features),'sections':len(sections),'visuals':len(visuals)},
        'provenance_counts':dict(Counter(p['provenance'].get('kind','unknown') for p in features)),
        'analyzer_versions':dict(Counter(p['analyzer_version'] for p in features if p['status']=='done')),
        'artifact_sha256':hashes,
        'groups':{k:summarize_group(v,names) for k,v in groups.items()}}
    (outdir/'statistics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    misses=[{k:p[k] for k in ('paper_id','year','title','presentation','status','error','pdf_url')} for p in features if p['status']!='done']
    (outdir/'extraction-gaps.json').write_text(json.dumps(misses,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'state':report['extraction_state'],'states':report['groups']['all']['states'],'rows':report['feature_rows'],'output':str(outdir)},ensure_ascii=False))
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db',type=Path,required=True)
    ap.add_argument('--corpus',type=Path,default=MODULE/'references/corpus/papers.jsonl.gz')
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); export(a.db,a.corpus,a.output)
