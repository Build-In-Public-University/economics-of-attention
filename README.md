# The Economics of Attention

Research repository for the working paper:

> The Economics of Attention: From Shannon Entropy to Hayekian Prices to Transformers
>
> Why information abundance makes discrimination—not information—the scarce resource.

This is a paper-specific projection connected to the shared research hub:

- Hub repository: `Build-In-Public-University/dynamic-verification-knowledge`
- Local hub checkout: `/Users/leoguinan/Projects/dynamic-verification-knowledge`
- Related paper: `transaction-costs-of-understanding`

The hub owns shared vocabulary, evidence conventions, and cross-paper research infrastructure. This repository owns the attention model, argument map, claim ledger, related-work targets, and future computational/empirical extensions. The link is a research dependency, not a claim that the hub currently validates this thesis.

## Status

- Conceptual draft captured from the working synthesis.
- Formal definitions and falsifiers registered in `claims/claims.json`.
- No empirical results are claimed.
- No market, language, or human-subject experiment has been run here. A learned synthetic classifier C4 instrument is now included; no LLM or production-AI experiment has been run.
- A v4.1 semantic substrate experiment has deterministic local and `gpt-5.6-luna` Codex receipts with equal context-slot and claim budgets; token counts are recorded because sampled documents are not token-equal.
- Bibliography is intentionally a verification ledger, not invented metadata.

## Layout

- `papers/draft.md` — working paper draft.
- `claims/claims.json` — typed claims, dependencies, evidence ceilings, and falsifiers.
- `docs/ARGUMENT-MAP.md` — dependency order for the argument.
- `docs/RESEARCH-BOUNDARY.md` — what is and is not established.
- `docs/RELATED-WORK-LEDGER.md` — sources to retrieve and verify before citation.
- `docs/FOUNDATIONAL-CITATIONS.md` — verified source notes for Shannon, Hayek, Grossman–Stiglitz, and Vaswani.
- `docs/FORMAL-MODEL.md` — standalone mathematical specification and claim boundary.
- `docs/EXPERIMENT-ATTENTION-REGIME-SHIFT.md` — synthetic experiment contract for C1/C4.
- `docs/EXPERIMENT-ADJUDICATION-LIMITED-EXPLORATION.md` — completed synthetic Experiment 3 for pricing adjudication and noise.
- `docs/EXPERIMENT-MODEL-C4.md` — learned synthetic classifier C4 test with constrained scouts and bounded adjudication.
- `docs/EXPERIMENT-SEMANTIC-C4.md` — v4 textual-context, claim, and bounded-adjudication experiment.
- `docs/PAPER-QUALITY-GATES.md` — Steph-derived scholarly selection-pressure rubric.
- `src/attention_experiment.py` — dependency-free attention/compression instrument.
- `src/adjudication_experiment.py` — adjudication-limited exploration instrument for Experiment 3.
- `artifacts/attention-v1/` — machine-readable synthetic receipt.
- `artifacts/attention-v2/` — machine-readable Experiment 3 receipt.
- `artifacts/attention-v3/` — machine-readable model-level C4 receipt.
- `artifacts/attention-v4/` — historical OpenRouter receipt plus corrected local and `gpt-5.6-luna` Codex v4.1 receipts.
- `artifacts/quality-gates/` — mechanical paper quality-gate receipt.
- `game/attention-game.html` — local-only timed reading game: the paper disappears, then a causal-compression quiz produces a downloadable receipt.
- `docs/HUB-CONNECTION.md` — explicit relationship to the shared research hub.
- `scripts/validate.py` — dependency-free structural validator.
- `tests/test_repository.py` — executable repository invariants.

## Verify

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/quality_gate.py
python3 -m src.attention_experiment --output artifacts/attention-v1/attention-regime-shift.json
open game/attention-game.html
```

A passing validator establishes repository structure and claim metadata only. The quality gate establishes mechanical consistency of the declared draft and claim ledger; it does not establish the theory, empirical predictions, or any causal result.

The current receipt contains an information-abundance sweep and a cost-matched attention-diversity sweep. Both remain synthetic instrument results. C1 and C4 retain `prospective` evidence status; the receipt demonstrates the simulator's behavior, not a human or market effect.

## Attention game

The game is a self-contained local instrument for testing the paper's progressive-compression claim. Select a reading budget, read the bounded paper, then answer thesis/mechanism/economics/boundary/transfer questions after the source disappears. It reports a single-run score and `U(T)/T` efficiency and can export a JSON receipt. These are protocol observations, not evidence about human reader populations; population claims require controlled versions, randomized readers, and preregistered questions.
