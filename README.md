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
- No market, language, human-subject, or model experiment has been run here.
- Bibliography is intentionally a verification ledger, not invented metadata.

## Layout

- `papers/draft.md` — working paper draft.
- `claims/claims.json` — typed claims, dependencies, evidence ceilings, and falsifiers.
- `docs/ARGUMENT-MAP.md` — dependency order for the argument.
- `docs/RESEARCH-BOUNDARY.md` — what is and is not established.
- `docs/RELATED-WORK-LEDGER.md` — sources to retrieve and verify before citation.
- `docs/HUB-CONNECTION.md` — explicit relationship to the shared research hub.
- `scripts/validate.py` — dependency-free structural validator.
- `tests/test_repository.py` — executable repository invariants.

## Verify

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

A passing validator establishes repository structure and claim metadata only. It does not establish the theory, empirical predictions, or any causal result. The machine is a ledger with opinions about attention; reality still gets the final vote.
