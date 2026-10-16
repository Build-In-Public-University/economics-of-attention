# Experiment 3: adjudication-limited exploration

## Purpose

Experiments 1 and 2 establish two bounded synthetic mechanisms:

- information abundance dilutes undirected sampling under a fixed budget;
- non-redundant attention improves shifted-regime coverage when aggregate observer slots are matched.

Experiment 3 tests the missing cost term: exploratory diversity creates candidates that must be adjudicated. The first deterministic run is recorded at `artifacts/attention-v2/adjudication-limited-exploration.json`.

## Contract

Hold the total observer count, per-observer feature budget, feature environment, causal regimes, and random seeds fixed. Vary exploratory attention diversity as in Experiment 2. Add an adjudication budget `J`, measured as the maximum number of candidate feature claims the network can evaluate per decision window.

Candidate policies:

1. `homogeneous`: repeated expert support;
2. `diverse_unfiltered`: union of expert and exploratory supports, with all candidates passed to adjudication;
3. `diverse_top_j`: union support ranked by a declared calibration score, retaining at most `J` candidates;
4. `oracle`: retains only currently causal features as an upper-bound control.

## Outcomes

Report separately:

- shifted-regime novel-signal coverage;
- stable-regime action accuracy;
- shifted-regime action accuracy;
- false-positive candidate rate;
- adjudication operations consumed;
- abstention or delay when `J` is exceeded;
- net utility under a declared cost model.

Do not collapse these into one score before checking that the cost units and action values are compatible.

## Prediction

At low diversity, blindness dominates. As diversity rises, novel-signal coverage and shifted-regime accuracy improve. At high diversity with fixed `J`, unfiltered candidates increase false-positive burden, delay, or abstention. A costed policy should therefore have an interior operating region:

`A* = argmax_A [V(A) - C_observation(A) - C_adjudication(A)]`.

The prediction is conditional. If the adjudicator receives free oracle knowledge, or if irrelevant candidates carry no processing or error cost, the frontier cannot be identified by this instrument.

## First synthetic run

With `J=20`, 21 observers, 105 total attention slots, and 20 exploratory observers:

- unfiltered exploration reached shifted-regime accuracy `0.7913` but net utility `0.3637` after declared sampling, adjudication, and false-positive costs;
- noisy top-`J` adjudication reached shifted-regime accuracy `0.7703` and net utility `0.5734`;
- the oracle upper bound reached accuracy `0.7945` and net utility `0.6495`.

The homogeneous control now has a constant unique candidate count of `5.0` at every diversity level while still charging `105` sampling operations. This separates gross sampling from unique candidate distinctions. The unfiltered policy's candidate count rises from `5.0` to `66.45`; its shifted accuracy rises from `0.5036` to `0.7913`, while net utility falls from `0.3736` to `0.3637`. The top-`J` policy keeps evaluated candidates bounded at `J` and reaches net utility `0.5734` at maximum exploration. These are instrument results under explicit proxy costs, not evidence of human or market behavior.

The corrected regime-probability and budget sensitivity sweep scores each candidate against the active causal regime before mixing outcomes. At regime-change probability `0.5`, expected top-`J` net utility is `0.6016`, `0.6373`, `0.6385`, `0.5951`, and `0.4811` for `J={5,10,20,40,65}` respectively. The optimum is fixture-dependent: at probability `0.0`, `J=20` wins narrowly; at probability `1.0`, `J=10` wins. The result supports a conditional exploration/adjudication frontier, not a universal optimum.

## Evidence boundary

The completed receipt validates simulator behavior under the declared adjudication contract. It cannot establish human, institutional, market, or production-model effects without separate evidence.
