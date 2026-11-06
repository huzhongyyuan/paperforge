# Conference corpus tools

All commands here assume the working directory is the unified `paperforge` root. When working inside a paper repository, resolve these paths against the installed skill rather than changing or overwriting the paper's files. Read [coverage](merged-evidence.md) before reporting counts. Existing scripts inside `modules/top-ml/` retain their original sibling-import layout.

## Query the stored metadata

```bash
python3 modules/top-ml/scripts/query_corpus.py \
  --corpus modules/top-ml/references/corpus/papers.jsonl.gz \
  --conference CVPR --presentation oral --query 'diffusion|generation' --limit 12
```

Use records for discovery. Read the primary paper before citing its technical claim. Do not load the complete compressed metadata into model context.

## CVPR 2024–2026: offline evidence and scoped readings

Use this newer module for the CVF main-proceedings snapshot, verified presentation labels, section/caption statistics and reading scopes. It overlaps the historical library; do not add the counts. See its [coverage and feature semantics](../modules/cvpr2024-2026/references/coverage.md).

```bash
python3 modules/cvpr2024-2026/scripts/query.py search --year 2026 --presentation highlight --query EffectErase
python3 modules/cvpr2024-2026/scripts/query.py cards --query FreeU
python3 modules/cvpr2024-2026/scripts/query.py stats --year 2025 --presentation oral --metric section.introduction.word_count
python3 modules/cvpr2024-2026/scripts/query.py features --query 'Video Depth Anything' --limit 1
```

`search` is literal title matching, not regex or semantic search. `cards` reports only the recorded reading scopes. `stats` supports year/presentation groups; omitting `--metric` lists available keys. `features` includes extraction status, provenance, quality flags and per-paper features. All four modes use the standard library and perform no network requests. `done` means the extraction ran, not that all extracted text or semantics passed review.

`statistics.json` includes unweighted and Oral 3 / Highlight 2 / Poster 1 summaries; unknown presentation labels are excluded from weighted summaries. Missing feature categories are not measured zeros. `extraction-gaps.json` preserves inaccessible, held and failed records. Do not automatically download them during ordinary writing.

To re-export an already authorized local analysis database, without fetching PDFs:

```bash
python3 modules/cvpr2024-2026/scripts/export.py \
  --db /absolute/path/to/analysis.sqlite \
  --output /absolute/path/to/export-directory
```

The exporter opens SQLite read-only and checks IDs, years, titles, labels and PDF URLs against the bundled metadata. It does not initialize or change the database. The separate `stream.py` is for an authorized unfinished extraction pass, not routine querying: it processes only pending rows, locks the database, caps concurrency at four, and retries only HTTP 429 at most twice. It refuses unresolved in-flight rows. Never run the legacy analyzer's database initializer against this live snapshot: initialization can reset ownership/status information. Preserve prior failures unless the user authorizes a justified retry; a status file alone is not authority to restart an unknown run.

## Refresh only the evidence needed

For a requested updated metadata snapshot:

```bash
python3 modules/top-ml/scripts/collect_corpus.py --output-dir /tmp/top-ml-corpus --refresh
```

Inspect the generated manifest before reporting current coverage. For newly public venue-years use `modules/top-ml/references/corpus/source-config.example.json`, replace placeholders with verified official URLs, and pass `--source-config /path/to/sources.json`. Do not invent endpoints or interpret an empty response as zero accepted papers.

For a requested or necessary proportional full-text sample, with `pypdf` and `curl` available:

```bash
python3 modules/top-ml/scripts/analyze_corpus.py \
  --corpus /tmp/top-ml-corpus/papers.jsonl \
  --output-dir /tmp/top-ml-analysis \
  --priority-per-stratum 12 --poster-per-venue 8 --jobs 4
```

## Resumable exhaustive pass

Use when the user's scope requests an exhaustive pass, not merely an ordinary writing task or skill merge. Install the dependencies from `modules/top-ml/scripts/requirements-full-corpus.txt` into an appropriate isolated environment. The analyzer streams PDFs through temporary files and stores extracted features in SQLite; omit `--keep-pdfs` unless retaining the large PDF archive is explicitly requested.

```bash
python3 modules/top-ml/scripts/analyze_full_corpus.py \
  --corpus modules/top-ml/references/corpus/papers.jsonl.gz \
  --database /tmp/top-ml-full/full.sqlite \
  --temp-dir /tmp/top-ml-full/tmp \
  --progress-json /tmp/top-ml-full/progress.json \
  --jobs 3
python3 modules/top-ml/scripts/report_full_corpus.py \
  --database /tmp/top-ml-full/full.sqlite \
  --output-dir /tmp/top-ml-full/report
```

The same analyzer command resumes the database. Blocked publishers use per-host circuit breakers. Retry blocked sources only when the cause has changed; use `--retry-errors` for transient failures. Report `done`, `blocked`, `error`, `not_found`, `no_pdf`, `pending`, and unavailable venue-years separately. Keep reports `in_progress` while analyzable records remain.

Exported `full-corpus-report.md`, `summary.json`, `sections.jsonl.gz` and `figures.jsonl.gz` preserve aggregate and record-level features. A partially completed report does not turn the original 55-paper sample into an exhaustive observation. For independent databases from an earlier task, inspect their reports and status rather than inferring completion from these installed scripts.
