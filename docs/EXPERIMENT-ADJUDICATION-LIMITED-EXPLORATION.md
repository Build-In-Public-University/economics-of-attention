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

- unfiltered exploration reached shifted-regime accuracy `0.7913` but net utility `0.4022` after declared observation, adjudication, and false-positive costs;
- noisy top-`J` adjudication reached shifted-regime accuracy `0.7703` and net utility `0.6120`;
- the oracle upper bound reached accuracy `0.7945` and net utility `0.6880`.

The unfiltered policy's candidate count rose from `5.0` with no explorers to `66.45` with 20 explorers, while its net utility fell from `0.4675` to `0.4022`. The top-`J` policy kept evaluated candidates bounded at `J`, but its false-positive rate remained `0.865` at the highest diversity setting. This is an instrument result under the declared proxy costs, not evidence of a universal interior optimum. The cost coefficients and noisy adjudication signal are explicit fixture assumptions, not measured human costs.

## Evidence boundary

This is a prospective protocol. A future receipt may validate simulator behavior under the declared adjudication contract; it cannot establish human, institutional, market, or production-model effects without separate evidence.
