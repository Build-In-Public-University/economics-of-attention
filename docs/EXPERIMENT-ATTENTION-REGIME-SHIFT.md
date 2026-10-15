# Attention regime-shift experiment

## Contract

This synthetic instrument targets C1 and C4. It creates binary observable features. Five features determine the label in each regime. Each observer has a fixed 5-feature attention budget.

- Expert: retains the five causal features learned in the stable regime.
- Novice: samples five features uniformly.
- Heterogeneous network: combines the expert with 20 independent flat exploratory observers; an adjudicator uses the union of retained supports.

The receipt now contains two controlled sweeps:

1. Information abundance: `N = {5, 10, 20, 50, 100, 200, 500, 1000}` while the observer budget remains `B=5`. Policies are random, expert, and mixed (four learned slots plus one exploratory slot).
2. Attention diversity: 21 total observers and 105 total attention slots in every row. The sweep replaces homogeneous expert observers with 0, 1, 2, 5, 10, or 20 exploratory observers, holding aggregate slots fixed.

For each trial, the action is the sign of the retained causal feature sum. Missing causal features are unobserved, not imputed. The instrument measures representational retention and action accuracy, not human learning.

## Predictions

Stable regime:

`accuracy(expert) > accuracy(novice)`.

Regime shift, where the five causal features move to previously irrelevant dimensions:

`accuracy(heterogeneous) > accuracy(expert)` and `novel_signal_coverage(heterogeneous) > novel_signal_coverage(expert)`.

For a particular shifted feature, the analytical expectation for `m` independent uniform explorers is `1 - (1 - B/N)^m`. At `B=5`, `N=100`, and `m=20`, this is approximately `0.642`.

## Run

```bash
python3 -m src.attention_experiment --output artifacts/attention-v1/attention-regime-shift.json
python3 -m unittest discover -s tests -v
```

## Evidence boundary

The output is labeled `synthetic_fixture_not_empirical`. It demonstrates behavior of the declared simulator and parameterization. It does not establish a general law about human expertise, institutions, markets, or neural networks. The original expert-versus-heterogeneous comparison has unequal total observer count; the new diversity sweep adds the cost-matched comparison required to isolate overlap from gross attention slots. Adjudication, sensing quality, and real-world coordination costs remain abstracted away.
