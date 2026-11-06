---
name: paperforge
description: Write and revise research papers, design experiments and editable figures, lay out manuscripts, and prepare scientific reviews or rebuttals. Also revise technical explanations and delivery reports for direct, evidence-preserving expression. Use for paper writing, figures, layout, review, clear writing, and bundled ML/CV corpus queries.
license: MIT
---

# PaperForge

Complete the user's requested research or writing artifact through one workflow. Select resources by function and technical problem; paper cases supply examples, not a separate author profile. All required collections and production scripts are bundled here.

Use the supplied draft, code, results and prior conversation before asking for missing material. Read only what the task needs. A sentence edit needs its context and a meaning check; a full-paper audit or new workspace is appropriate only when the requested scope calls for it.

## Route by function

| Requested work | Read | Produce |
|---|---|---|
| Research idea, module or experiment design | [Integrated writing](references/integrated-writing.md), relevant phases of [research workflow](references/end-to-end-paper-workflow.md) | Falsifiable hypothesis, mechanism, closest-work check and minimal experiment plan; ideas remain hypotheses until tested. |
| Draft or revise a section/manuscript | Integrated writing and the matching [section playbook](modules/top-ml/references/section-playbook.md) | Actual prose or source edits, with material evidence gaps identified. |
| Figure plan or caption | [Integrated figures](references/integrated-figures.md) | Claims, panels, real-asset requirements, placement and usable captions. |
| Draw/edit figures, plots or diagrams | Integrated figures, then [production](references/figure-production.md), [component tools](modules/share-tools/references/guide.md) or [PPT mechanics](references/ppt-diagrams.md) | Actual editable sources and inspected exports; a prompt alone does not complete drawing. |
| Page budget, two columns, floats or pagination | [Manuscript layout](references/manuscript-layout.md), [layout examples](modules/top-ml/references/layout-playbook.md) | Source-level layout changes; compile/render when source permits and inspect affected pages. |
| Scientific review, submission audit or rebuttal | Relevant [review gates](references/review-gates.md), [review rubric](modules/top-ml/references/review-rubric.md) | Prioritized findings or a revised response with evidence and exact locations. |
| Direct technical explanation, ordinary answer or delivery report | [Direct writing](references/direct-writing.md) | Revised text retaining facts, uncertainty, failures and actual completion status; no paper audit required. |
| Direct paper prose, caption, contribution or rebuttal | Scientific checks above, then [paper expression](references/anti-defensive-writing.md) | Revised prose whose scope, causal strength and attribution match the evidence. |
| Relevant method, paragraph or visual examples | [Case selection](references/case-library.md), then 1–3 matching paper cards | Transferable reasoning or visual operations applied to the user's original work. |
| Conference talk | [PPT diagrams and talks](references/ppt-diagrams.md) | Argument-led, editable slides and inspected render when a deck is requested. |
| ICLR 2025 examples | [ICLR playbook](references/iclr2025-playbook.md), selected [paper cards](modules/iclr2025/references/paper-cards.md) and [coverage](modules/iclr2025/references/coverage.md) | Contribution-specific prose/figures with stated sample scope. |
| CVPR 2024–2026 examples | Matching resources below; [coverage](modules/cvpr2024-2026/references/coverage.md) for corpus claims | Original prose or visual decisions supported by relevant cases. |
| Corpus query or coverage | [Merged evidence](references/merged-evidence.md), [corpus tools](references/corpus-tools.md) | Bounded records/statistics with snapshot date and reading depth; refresh when requested or needed for current evidence. |

Resolve competing guidance in this order: user's task and supplied evidence → current official venue requirements → this route → relevant specialist guidance → observed examples. Word-count ranges and example module counts are diagnostics, not quotas. The ML/CV sample is not evidence about every research field. General expression tasks use the direct-writing route; paper tasks combine argument, scientific review and expression in the same workflow.

For CVPR-informed work, load only the resource matching the task: [argument and contributions](modules/cvpr2024-2026/references/argument-and-contributions.md), [section responsibilities](modules/cvpr2024-2026/references/section-playbook.md), [sentence/paragraph transitions](modules/cvpr2024-2026/references/language-and-transitions.md), [experimental reasoning](modules/cvpr2024-2026/references/experiments.md), or [figures and page allocation](modules/cvpr2024-2026/references/figure-design.md). Choose 1–3 relevant [paper cards](modules/cvpr2024-2026/references/paper-cards.md) by contribution type and failure mode, not presentation label alone. Explain the transferable operation and apply it to the user's artifact; do not copy distinctive sentences or force four paragraphs, three contributions, or a fixed palette. Oral/Highlight weighting guides discovery and descriptive statistics, not evidence strength. The [distillation design](modules/cvpr2024-2026/references/distillation-design.md) is for extending this module, not required reading for every edit.

## One shared scientific workflow

Apply this workflow to research and paper tasks. Ordinary answers, technical explanations and delivery reports use the direct-writing route above with its fact and meaning checks.

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
- `modules/case-library/scripts/generate_templates.py OUTPUT_DIRECTORY` rebuilds the four original [case-based scaffolds](modules/case-library/assets/01-framework.svg). Adapt topology as well as labels. Attributed source excerpts are study references, not figures to relabel as the user's work.
- Historical query/analysis tools remain in `modules/top-ml/scripts/`; the CVPR 2024–2026 offline query and read-only exporter are in `modules/cvpr2024-2026/scripts/`. [Corpus tools](references/corpus-tools.md) gives working-directory-aware commands. Ordinary writing uses bundled evidence without starting new downloads.

Numerical plots require real data and retained code. Architecture/workflow diagrams use structured vector or native shapes. Qualitative evidence uses actual outputs and matched crops/times. Generated raster art is suitable only for clearly conceptual, non-evidentiary illustration. Do not claim native editability or export compatibility without checking the delivered format.

Preserve original images and final export quality. Compress model-input/process previews toward 200,000 bytes per image, crop small text when needed, and inspect only the relevant small set of previews.

## Completion and coverage

Return the requested draft/edit/file first, followed by material changes, actual checks and consequential missing evidence. A figure delivery includes editable source, caption and inspected preview, plus high-quality export when available; plots also include source data and code. Full-manuscript work includes the compiled PDF, page/float findings and unresolved venue dependencies. A section edit does not require a deck, full audit or new project scaffold.

Read [merged evidence](references/merged-evidence.md) before reporting source coverage. The conference metadata, sampled full-text features and case close readings have different units and dates; do not add their counts or claim exhaustive CCF-A full-text study. No writing pattern proves acceptance, scientific correctness or novelty. Structural validators verify artifacts, not research quality.
