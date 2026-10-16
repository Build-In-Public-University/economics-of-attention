# Model-level C4 experiment: constrained views and bounded adjudication

## Contract

This instrument tests whether a small model-level network with heterogeneous feature views can adapt to a hidden regime change better than a cost-matched homogeneous specialist network.

- Environment: 40 binary features; five stable causal features and five shifted causal features.
- Agents: 21 total, each with a five-feature view, for 105 gross sampling operations.
- Homogeneous control: all agents repeatedly inspect the stable specialist support.
- Heterogeneous condition: one stable specialist plus `E` constrained scouts with independently sampled five-feature views.
- Adjudicator: scores candidate features by calibration-set correlation with the active label and retains at most `J` features.
- Evaluation: fresh stable and shifted test windows, reporting accuracy, novel-signal coverage, candidate count, false positives, sampling operations, adjudication operations, and net utility.

The instrument varies `E={0,1,2,5,10,20}` and `J={5,10,20,40,65}`. Gross sampling is held at 105 operations in every cell; heterogeneity changes non-redundant support, not total view slots.

## Predictions

Under the stable regime, the homogeneous specialist should be efficient because its retained support matches the trained causal structure. Under the shifted regime, scouts should expose previously suppressed features and bounded adjudication should recover more novel signal than the homogeneous control without retaining every candidate.

The relevant comparison is not raw accuracy alone:

`homogeneous specialists` versus `specialists + heterogeneous scouts + bounded adjudicator`

at matched gross sampling cost.

## Result

The default receipt contains 150 cells and is labeled synthetic. At maximum exploration and `J=10`, heterogeneous shifted accuracy is `0.8448` versus homogeneous `0.4990`, with novel-signal coverage `0.95` and net utility `0.7771`. At `J=20`, heterogeneous accuracy is `0.8232` and net utility `0.7353`: retaining more candidates does not automatically create more net value.

The shifted-regime best heterogeneous cell in this fixture is `E=20, J=5`, with net utility `0.8127`. The stable-regime best cell is `E=5, J=5`, with net utility `0.9350`. These are grid optima, not universal policies or mathematical phase transitions.

## Evidence boundary

This is a synthetic model-level mechanism test. The agents learn declared feature correlations from calibration examples, but the task, feature views, costs, and regime change are constructed. The receipt does not establish effects in humans, markets, institutions, or production AI systems.

Run:

```bash
python3 -m src.model_c4_experiment --output artifacts/attention-v3/model-c4-constrained-views.json
python3 -m unittest tests.test_model_c4_experiment -v
```
