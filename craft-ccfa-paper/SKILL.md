---
name: craft-ccfa-paper
description: Plan research, write and revise papers, design experiments and editable figures, lay out manuscripts, and prepare reviews or rebuttals. Unifies CCF-A/ICLR and CVPR 2024–2026 evidence, the Yue Ma first/co-first profile, scientific review and anti-defensive editing. Use for 论文写作、论文修改、论文画图、审稿、整篇排版、mayue/马跃风格 and bundled conference corpus queries.
license: MIT
---

# CCF-A Paper — Unified Research, Writing, Figures and Review

Turn the user's research into the requested manuscript or visual artifact. This is the maintained workflow for `$craft-ccfa-paper`, `$write-top-ml-paper`, `$mayue-paper-skill` and `$yue-ma-paper-style`. All required reference collections and existing production scripts are bundled here; do not invoke a compatibility entry from this skill.

For paper writing, revision, captions and rebuttals, combine argument construction, relevant author examples, scientific review and anti-defensive editing in this single workflow. Scale the checks to the request; a sentence edit does not require a full-paper audit or a separate agent. Apply the user's global Mayue preference where the research fits; another style or an unrelated research topic can use the general profile.

## Choose the work and profile

Use the supplied draft, code, results and prior conversation before asking for missing material. For a small edit, read the matching section and complete the edit. A full-project inventory or submission audit is only needed when that scope is requested.

- **General profile:** use the venue/task-appropriate research, section, figure and layout guidance. It applies to empirical, theoretical, benchmark and system papers; the stored ML/CV sample is not evidence about every CCF-A field.
- **Mayue profile:** when requested by name, selected through either author entry or the user's global preference, or already established in the conversation, combine the same scientific workflow with [the Mayue overlay](references/mayue-overlay.md). Use 1–3 matching first/co-first paper cards for argument structure, module explanation and figure organization. Author style never overrides facts, a required venue format or the user's requested structure.

Resolve competing guidance in this order: user's task and supplied evidence → current official venue requirements → this unified route → applicable specialist reference → observed example or stylistic heuristic. Word-count ranges and example module counts are diagnostics, not quotas. Load only references needed by the active route.

| Requested work | Read | Produce |
|---|---|---|
| Idea, research direction, module or experiment design | [integrated writing](references/integrated-writing.md), relevant phases of [research workflow](references/end-to-end-paper-workflow.md) | Falsifiable hypothesis, mechanism, closest-work check and minimal experiment plan; proposed ideas remain hypotheses. |
| Write/revise a section or manuscript | [integrated writing](references/integrated-writing.md), matching [section playbook](modules/top-ml/references/section-playbook.md) | Actual requested prose or source edits, with material missing evidence identified. |
| Mayue-specific paragraph or module work | Above plus [Mayue overlay](references/mayue-overlay.md) and matching author reference | Original prose preserving technical meaning, parameter states and module/figure/ablation consistency. |
| 写图 / figure plan / caption | [integrated figures](references/integrated-figures.md) | Claims, panels, real asset requirements, placement and usable captions as requested. |
| Draw/edit figures, plots or PPT diagrams | Integrated figures, then [production](references/figure-production.md) or [PPT mechanics](references/ppt-diagrams.md) | Actual editable sources and inspected exports; a prompt alone does not complete drawing. |
| Page budget, first page, two columns, floats, pagination | [manuscript layout](references/manuscript-layout.md), [layout examples](modules/top-ml/references/layout-playbook.md) | Page/float plan and source-level changes; compile/render when source permits and inspect relevant pages. |
| Review, submission audit or rebuttal | Relevant [review gates](references/review-gates.md), [review rubric](modules/top-ml/references/review-rubric.md) | Prioritized findings or actual revised response, with evidence and exact locations. |
| Remove defensive writing / make prose direct | [anti-defensive editing](references/anti-defensive-writing.md), with review gates 2 and 6 | Actual revised prose preserving evidence, material scope, attribution and useful logical contrasts. |
| Conference talk | [PPT diagrams and talks](references/ppt-diagrams.md) | Argument-led, editable slides and inspected render when a deck is requested. |
| ICLR 2025 argument, section, module or figure examples | [ICLR playbook](references/iclr2025-playbook.md), selected [paper cards](modules/iclr2025/references/paper-cards.md) and [coverage](modules/iclr2025/references/coverage.md) | Contribution-specific prose/figures with sample scope; use the complete metadata index to locate additional papers. |
| CVPR 2024–2026 writing patterns, section logic, language or figure examples | Select the matching resource below; [coverage](modules/cvpr2024-2026/references/coverage.md) for corpus claims | Original prose or visual decisions supported by a relevant paper card; descriptive distributions when requested. |
| Corpus query, refresh or coverage | [merged evidence](references/merged-evidence.md), [corpus tools](references/corpus-tools.md) | Bounded records/statistics with snapshot date and reading depth; refresh only when requested or needed for current evidence. |

For CVPR-informed work, load only the resource matching the task: [argument and contributions](modules/cvpr2024-2026/references/argument-and-contributions.md), [section responsibilities](modules/cvpr2024-2026/references/section-playbook.md), [sentence/paragraph transitions](modules/cvpr2024-2026/references/language-and-transitions.md), [experimental reasoning](modules/cvpr2024-2026/references/experiments.md), or [figures and page allocation](modules/cvpr2024-2026/references/figure-design.md). Choose 1–3 relevant [paper cards](modules/cvpr2024-2026/references/paper-cards.md) by contribution type and failure mode, not presentation label alone. Explain the transferable operation and apply it to the user's artifact; do not copy distinctive sentences or force four paragraphs, three contributions, or a fixed palette. Oral/Highlight weighting guides discovery and descriptive statistics, not evidence strength. The [distillation design](modules/cvpr2024-2026/references/distillation-design.md) is for extending this module, not required reading for every edit.

## One shared scientific workflow

1. Establish the task, relevant venue constraints, central claim and available evidence. Missing venue information makes venue-dependent choices provisional; it need not block a paragraph draft.
2. Link each major claim to an evidence item or proposed test. For full projects, retain claim IDs, protocol and raw-result locations. For small edits, a compact internal map is enough.
3. Separate observed failure, cited limitation, design reasoning and untested hypothesis. Verify cited propositions in the primary source before using them as facts.
4. Explain the method in actual dependency order. For each module identify **purpose, failure/cause, input, operation, output/injection point, training/inference state and verification** where applicable. Keep inherited components identifiable. Do not turn parallel branches into sequential stages for storytelling.
5. Make prose, equations, labels, captions and ablations express the same computation and claim. Calibrate interpretations to the actual protocol. Never invent results, comparisons, citations, author roles or novelty checks.
6. For prose and captions, check the relevant [review gates](references/review-gates.md), then apply [anti-defensive editing](references/anti-defensive-writing.md). Remove redundant apologies and hedges; retain conditions needed to interpret the exact claim. Compare meanings before and after: stronger wording must not add facts, causal strength, priority, generalization or superiority. Preserve contrasts that explain why the next design is needed.
7. Complete the requested artifact, then run proportionate semantic and format checks. For a complete manuscript, plan space and floats, compile and inspect every page; for a local edit, inspect its affected scope.

Draft international-venue prose in English unless the user chooses another language; explain edits in the user's language. Write original text. Source-paper patterns describe published collaborations, not private idea histories or personal authorship of every passage.

## Production tools

Paths below are relative to this skill's root; use absolute resolved paths when executing from a paper project. Tools write to the user's chosen workspace, not into the installed skill.

- `scripts/init_project.py <workspace>` initializes a new paper workspace without overwriting existing files. Existing projects can retain their structure.
- `scripts/audit_project.py <workspace>` checks the bundled project records in working mode; add `--final` for submission-candidate gates that reject unresolved major fields. Use it for projects using that manifest layout; its failure is not a scientific verdict on unrelated project structures.
- `scripts/render_diagram_svg.py validate SPEC.json` and `render SPEC.json --output OUT.svg` build editable vectors from a semantic JSON graph. Start with [diagram_spec.example.json](assets/diagram_spec.example.json), replacing its example method and layout.
- `scripts/render_diagram_pptx.mjs SPEC.json --output OUT.pptx` builds native PowerPoint shapes. Use the dependency locator to find Node.js and `pptxgenjs` in Codex desktop; do not assume Node is on PATH.
- `modules/share-tools/scripts/check_section.py SECTION FILE` provides optional, nonblocking section-style diagnostics. `modules/share-tools/scripts/check_terms.py FACTS --text method=METHOD --figure LABELS` checks canonical names; missing modules become failures only for explicitly selected complete scopes with `--require-in`. Use [shared facts and checks](modules/share-tools/references/guide.md) when prose and figures need this handoff; reuse existing authoritative records.
- `modules/share-tools/scripts/figkit.py` provides image stacks, encoders, network blocks, state icons and HTML/SVG/PDF/PNG export. Use the same [guide](modules/share-tools/references/guide.md) for this optional code-based framework route; numerical plots still require real data.
- `modules/mayue/scripts/generate_templates.py OUTPUT_DIRECTORY` rebuilds the four original [Mayue scaffolds](modules/mayue/assets/01-framework.svg). Adapt topology as well as labels. Attributed source excerpts are study references, not figures to relabel as the user's work.
- Historical query/analysis tools remain in `modules/top-ml/scripts/`; the CVPR 2024–2026 offline query and read-only exporter are in `modules/cvpr2024-2026/scripts/`. [Corpus tools](references/corpus-tools.md) gives working-directory-aware commands. Ordinary writing uses bundled evidence without starting new downloads.

Numerical plots require real data and retained code. Architecture/workflow diagrams use structured vector or native shapes. Qualitative evidence uses actual outputs and matched crops/times. Generated raster art is suitable only for clearly conceptual, non-evidentiary illustration. Do not claim native editability or export compatibility without checking the delivered format.

Preserve original images and final export quality. Compress model-input/process previews toward 200,000 bytes per image, crop small text when needed, and inspect only the relevant small set of previews.

## Completion and coverage

Return the requested draft/edit/file first, followed by material changes, actual checks and consequential missing evidence. A figure delivery includes editable source, caption and inspected preview, plus high-quality export when available; plots also include source data and code. Full-manuscript work includes the compiled PDF, page/float findings and unresolved venue dependencies. A section edit does not require a deck, full audit or new project scaffold.

Read [merged evidence](references/merged-evidence.md) before reporting source coverage. The conference metadata, sampled full-text features and author close readings have different units and dates; do not add their counts or claim exhaustive CCF-A full-text study. No writing pattern proves acceptance, scientific correctness or novelty. Structural validators verify artifacts, not research quality.
