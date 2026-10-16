# v4.1 semantic C4 substrate-change experiment

## Contract

v4.1 changes the substrate from structured feature coordinates to bounded textual evidence and natural-language claims, while correcting the v4 context and claim-budget confounds.

- Corpus: stable operational documents plus residual documents containing shifted-regime facts.
- Context budget: both conditions receive six document slots. Homogeneous observers repeatedly receive three stable documents; heterogeneous scouts receive six sampled slots across stable and residual documents.
- Heterogeneous scouts: receive different bounded document subsets, not additional total context.
- Observer output: claims with source, claim text, and topic.
- Claim-generation budget: each observer emits at most `B_C=3` claims.
- Adjudicator: ranks claims by lexical action-change proxy relative to the stable summary, without a hard-coded shifted-topic ontology, and retains at most `B_J=4` claims.
- Receipts: context hashes, request hashes, output hashes, adapter, model, endpoint, and latency for provider calls.
- Each decision row also records `context_slots` and whitespace-token `input_token_count`; future provider comparisons should equalize or price token counts rather than treating document count as sufficient cost accounting.

Two adapters are included:

1. `local`: deterministic claim extraction for contract and pipeline verification;
2. `codex`: Hermes `openai-codex` adapter targeting `gpt-5.6-luna`;
3. `provider`: OpenAI-compatible semantic generation through a configured endpoint. The prior `gpt-4o-mini` receipt is historical and is not the current target.

## v4.1 local result

Across five seeds, both policies generate exactly three claims from equal six-slot context budgets. Homogeneous shifted contexts produced zero novel claims. Heterogeneous shifted contexts exposed seven novel claims under the bounded adjudicator. Residual shifted documents remain available during the stable window as currently irrelevant evidence; therefore heterogeneous stable windows can expose residual claims without implying that the regime has already changed. The local adapter is deliberately deterministic and is not a language-model result.

## Provider replication status

The prior OpenRouter receipt completed with 20 decision windows using `gpt-4o-mini`; it is retained as historical provenance only. The corrected v4.1 Codex receipt now runs 20 decision windows through Hermes `openai-codex` with `gpt-5.6-luna`. Homogeneous shifted contexts exposed zero novel claims; heterogeneous shifted contexts exposed twelve. The token counts are not equal across heterogeneous sampled views, so this is a provider replication with recorded token residuals, not a fully token-cost-matched result.

## Boundary

The corpus, regime shift, context assignments, claim schema, and adjudication rules are constructed. The local adapter is a deterministic parser; the provider adapter is one model/API configuration. Neither result establishes a general claim about language, human cognition, markets, or production systems.

Run:

```bash
python3 -m src.semantic_c4_experiment --adapter local --output artifacts/attention-v4/semantic-c4-local-v41.json
python3 -m src.semantic_c4_experiment --adapter codex --model gpt-5.6-luna --output artifacts/attention-v4/semantic-c4-codex-v41.json
python3 -m src.semantic_c4_experiment --adapter provider --model gpt-5.6-luna --output artifacts/attention-v4/semantic-c4-provider-gpt-5.6-luna.json
python3 -m unittest tests.test_semantic_c4_experiment -v
```
