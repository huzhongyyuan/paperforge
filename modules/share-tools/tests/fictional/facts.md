# Facts: TideMotion

Fictional method, for testing only.

## Method

- Name: TideMotion
- One-line mechanism: splits motion features by frequency band and routes each band to a separate expert.

## Task

- Definition: video motion transfer from one reference video.
- Dilemma or structural gap: fine motion needs high-frequency detail, while long-range motion needs low-frequency structure.

## Existing paradigms

| Paradigm | Representative work | Mechanism-level flaw |
|---|---|---|
| Training-free guidance | [CITE: training-free motion transfer] | Bounded by the pretrained motion prior |
| Per-video tuning | [CITE: tuning-based motion transfer] | Updates all features uniformly |

## Modules

| Name | Aliases | State | Role | Reproducible quantity |
|---|---|---|---|---|
| Frequency-routed Motion Prior | Motion Prior | trainable | Assigns each band to an expert | [TODO] |
| Band-wise Test-time Adaptation | BTA | trainable | Tunes the relevant experts per video | [TODO] |
| Spectral Alignment Loss | | new | Aligns motion in each band | [TODO] |

## Inputs and outputs

- Inputs: reference video, text prompt
- Outputs: generated video
- Real images available: [TODO]
- Training vs inference differences: [TODO]
- Loss paths: [TODO]

## Experiments

- Datasets or benchmark: [TODO]
- Baselines: [TODO]
- Metrics and results: [TODO]
- Hardware and time: [TODO]
- Code availability: [TODO]

## Claims to confirm

- None yet.

## Figure notes
