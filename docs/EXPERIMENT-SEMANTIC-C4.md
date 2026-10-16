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
2. `provider`: OpenAI-compatible semantic generation through the configured OpenRouter endpoint, using `openai/gpt-4o-mini` in the recorded replication.

## Local result

Across five seeds, homogeneous shifted contexts produced zero novel claims. Heterogeneous shifted contexts exposed four novel claims under the bounded adjudicator. The local adapter is deliberately deterministic and is not a language-model result.

## Provider replication

The provider receipt completed with 20 decision windows. It records request and output hashes rather than silently treating model output as ground truth. In the recorded run, homogeneous shifted contexts produced zero novel claims; heterogeneous shifted contexts produced four. This is a provider-backed synthetic replication, not evidence about production AI behavior.

## Boundary

The corpus, regime shift, context assignments, claim schema, and adjudication rules are constructed. The local adapter is a deterministic parser; the provider adapter is one model/API configuration. Neither result establishes a general claim about language, human cognition, markets, or production systems.

Run:

```bash
python3 -m src.semantic_c4_experiment --adapter local --output artifacts/attention-v4/semantic-c4-local.json
python3 -m src.semantic_c4_experiment --adapter provider --model openai/gpt-4o-mini --output artifacts/attention-v4/semantic-c4-provider.json
python3 -m unittest tests.test_semantic_c4_experiment -v
```
