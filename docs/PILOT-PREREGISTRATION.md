# Economics of Attention — first pilot preregistration

Status: draft for approval before recruitment
Instrument freeze candidate: commit c6bc4da plus the pilot instrumentation commit

## Question

At a fixed 180-second reading budget, does the progressive-compression artifact preserve more consequential causal understanding than the conventional PDF control?

## Arms

- Progressive: `game/progressive-stimulus-v1.html`
- Control: `game/standard-paper.pdf`
- Assignment: randomized in the local clean-session interface; participants can see the surface type, so this is not participant-blinded.

## Primary hypothesis and outcome

- H0: U_P = U_C
- H1: U_P > U_C
- Primary outcome: U = correct answers / 5 on the frozen `game/question-set-v1.json`.
- The five dimensions are thesis, mechanism, economics, boundary, and transfer.

## Secondary outcome

`T_Q`, quiz/retrieval time after the source is removed. Reading efficiency is `U / T_R`; quiz time is not included in `T_R`.

## Eligibility and primary analysis set

Primary analysis: first-exposure runs only, defined by the pre-run exposure snapshot having `prior_run_count = 0`, `seen_question_set_v1 = false`, and no previously seen arm. Repeat exposures remain in the ledger, are linked by the local participant identifier, and are analyzed descriptively or in sensitivity analysis, never silently pooled as naive observations.

Invalid delivery runs (`status = stimulus_load_failure` or `stimulus_ready = false`) are excluded from outcome analysis and counted in a delivery-failure report.

## Frozen materials

Every valid receipt records the SHA-256 hashes of the progressive stimulus, control PDF, question set, and protocol. The exact question prompts and answer options are frozen in `question-set-v1.json`.

## Attribution and funnel events

The public pilot may record only privacy-bounded events: click/session start, stimulus-ready, and result. Events contain no name, email, IP address, free text, or raw answer selections. The browser supplies a locally persisted pseudonymous participant ID and a run ID. UTM values are bounded and truncated. Result events include arm, score, `T_R`, `T_Q`, prior-exposure status, and artifact hashes.

Event counts are descriptive. They do not establish that a hook caused a result difference. Hook/content variants must be assigned and recorded before comparison; missing events remain missing, not zero.

## Reporting boundary

These observations describe the declared instrument and pilot participants only. They do not establish effects in humans generally, markets, institutions, language, or production AI.
