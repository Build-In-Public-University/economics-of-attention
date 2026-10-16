# v4 semantic C4 substrate-change experiment

## Contract

v4 changes the substrate from structured feature coordinates to bounded textual evidence and natural-language claims.

- Corpus: stable operational documents plus residual documents containing shifted-regime facts.
- Homogeneous observers: receive the same high-value stable subset.
- Heterogeneous scouts: receive different bounded document subsets.
- Observer output: claims with source, claim text, and topic.
- Adjudicator: ranks claims and retains at most `J=4` claims.
- Receipts: context hashes, request hashes, output hashes, adapter, model, endpoint, and latency for provider calls.

Two adapters are included:

1. `local`: deterministic claim extraction for contract and pipeline verification;
2. `provider`: OpenAI-compatible semantic generation through a configured endpoint, targeting the requested `gpt-5.6-luna` model. The prior `gpt-4o-mini` receipt is historical and is not the current target.

## Local result

Across five seeds, homogeneous shifted contexts produced zero novel claims. Heterogeneous shifted contexts exposed four novel claims under the bounded adjudicator. The local adapter is deliberately deterministic and is not a language-model result.

## Provider replication status

The prior provider receipt completed with 20 decision windows using `gpt-4o-mini`; it is retained as historical provenance only. The current target is `gpt-5.6-luna`. The configured OpenRouter model catalog does not expose that literal model ID, so no replacement provider receipt is claimed. The local receipt remains runnable; a provider rerun requires an endpoint that actually serves `gpt-5.6-luna`.

## Boundary

The corpus, regime shift, context assignments, claim schema, and adjudication rules are constructed. The local adapter is a deterministic parser; the provider adapter is one model/API configuration. Neither result establishes a general claim about language, human cognition, markets, or production systems.

Run:

```bash
python3 -m src.semantic_c4_experiment --adapter local --output artifacts/attention-v4/semantic-c4-local.json
python3 -m src.semantic_c4_experiment --adapter provider --model gpt-5.6-luna --output artifacts/attention-v4/semantic-c4-provider-gpt-5.6-luna.json
python3 -m unittest tests.test_semantic_c4_experiment -v
```
