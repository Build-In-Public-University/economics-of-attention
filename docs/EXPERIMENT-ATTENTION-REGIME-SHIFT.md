# Attention regime-shift experiment

## Contract

This synthetic instrument targets C1 and C4. It creates 100 binary observable features. Five features determine the label in each regime. Each observer has a 5-feature attention budget.

- Expert: retains the five causal features learned in the stable regime.
- Novice: samples five features uniformly.
- Heterogeneous network: combines the expert with 20 independent flat exploratory observers; an adjudicator uses the union of retained supports.

For each trial, the action is the sign of the retained causal feature sum. Missing causal features are unobserved, not imputed. The instrument measures representational retention and action accuracy, not human learning.

## Predictions

Stable regime:

`accuracy(expert) > accuracy(novice)`.

Regime shift, where the five causal features move to previously irrelevant dimensions:

`accuracy(heterogeneous) > accuracy(expert)` and `novel_signal_coverage(heterogeneous) > novel_signal_coverage(expert)`.

## Run

```bash
python3 -m src.attention_experiment --output artifacts/attention-v1/attention-regime-shift.json
python3 -m unittest discover -s tests -v
```

## Evidence boundary

The output is labeled `synthetic_fixture_not_empirical`. It demonstrates behavior of the declared simulator and parameterization. It does not establish a general law about human expertise, institutions, markets, or neural networks. The heterogeneous condition has more total observers and therefore more total feature-processing cost than the expert condition; the result is an exploration-capacity demonstration, not a cost-normalized superiority claim.
