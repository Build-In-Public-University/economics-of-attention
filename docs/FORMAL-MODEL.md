# Formal model specification

## Scope

This document freezes the mathematical core independently of the prose draft. Equations here are definitions or bounded hypotheses unless a later receipt supplies a proof or observation. The model is an abstract resource-allocation model; it does not assert that people, markets, or neural networks implement the same mechanism.

## Primitive objects

At time `t`, observer `i` faces:

- `S_t`: latent world state.
- `X_t`: potentially observable information, with components `x_j,t`.
- `q_i,t`: objective, query, or decision context.
- `w_i,t`: prior conceptual/language structure.
- `A`: an attention policy mapping `(X_t, q_i,t, w_i,t)` to a selected or weighted representation `Y_A`.
- `phi`: a compression map from `Y_A` to retained representation `Z_A`.
- `a`: an action from feasible set `mathcal A_i`.
- `U_i(a,S_t)`: observer-specific utility or decision value.

A simple weighted attention policy is:

`Y_A = sum_j alpha_j x_j`, with `alpha_j >= 0` and `sum_j c_j(alpha_j) <= B_i`.

The budget `B_i` is in declared resource units: time, compute, energy, money, or a vector of these. A scalar comparison requires a declared conversion or remains undefined.

## Central optimization

Define the value of a policy as expected optimal action value after selection and compression:

`V_i(A | X_t,q_i,t,w_i,t) = E[max_a E[U_i(a,S_t) | phi(A(X_t | q_i,t,w_i,t))]]`.

The central policy is:

`A*_i,t = argmax_A [ V_i(A) - C_i(A) - lambda_i D(A,A_i,t-1) ]`.

Where:

- `C_i(A)` is total attention cost: sensing, acquisition, processing, storage, interpretation, delay, coordination, and execution overhead.
- `D(A,A_i,t-1) >= 0` is a declared distance between the new and prior attention policies.
- `lambda_i >= 0` converts policy change into the same units as value.
- `V_i(A)` and `C_i(A)` must use the same decision horizon and compatible units.

The argmax may be set-valued. If no policy has positive net value, abstention or the baseline policy is permitted. If `lambda=0`, there is no hysteresis penalty. If `C(A)=infinity`, the policy is infeasible. If `V` is unavailable, the optimization is a proposal, not an executable decision rule.

## Action-relative meaning

For an observation `x` and retained state `Z`, define:

`M_i(x | Z) = max_a E[U_i(a,S) | Z,x] - max_a E[U_i(a,S) | Z]`.

This is consequential uncertainty reduction, not Shannon information. It is relative to an observer, an action set, a utility function, and a conditioning state. It can be negative when processing `x` induces a worse action or delay.

## Attention efficiency

For baseline policy `A_0`:

`eta_A = (V_i(A)-V_i(A_0)) / C_i(A)`.

`eta_A > 1` is meaningful only when numerator and denominator share compatible units. If value is dimensionless utility and cost is minutes, the ratio is not interpretable until a conversion is declared. The weaker unit-safe statement is:

`V_i(A)-V_i(A_0) > C_i(A)`.

## Compression and blind spots

Compression is lossy when there exist `S_1 != S_2` such that:

`phi(A(X(S_1))) = phi(A(X(S_2)))`

while some feasible action has different value across the states. The existence of a collision alone is not a failure: it becomes a blind spot only when the discarded distinction becomes consequential within the decision horizon.

## Heterogeneous observers

For observers `i=1..m`, define retained supports `support(A_i)`. The network's available support is:

`O_network = union_i support(A_i)`.

This union is only an observational capacity. It becomes collective decision value only if aggregation `G` can preserve, test, and adjudicate minority observations. Heterogeneity can increase cost, conflict, and false positives; the theory predicts a conditional advantage under regime change, not a universal advantage.

## Synthetic experiment mapping

The attention-regime-shift instrument instantiates a finite feature environment with 100 binary features, a 5-feature causal target, a 5-feature per-observer budget, one trained/stable expert support, flat random novice supports, and 20 exploratory observers. It measures:

- action accuracy from retained causal features;
- novel-signal coverage after a causal regime shift;
- retained feature count and observer count as cost proxies.

The receipt is `synthetic_fixture_not_empirical`. It tests the representational mechanism under an explicit synthetic contract; it does not estimate human attention costs, establish market alpha, or validate Transformer behavior.

## Information abundance and attention diversity

For an uninformed observer sampling `b` features uniformly from `N`, the expected probability of retaining a particular feature is:

`P(random observer retains x) = b/N`.

For `m` independent observers, the probability that at least one retains that feature is:

`P(novel feature preserved) = 1 - (1 - b/N)^m`.

This assumes independent uniform sampling, no replacement within an observer, and a feature not already fixed in a shared filter. It is an analytical expectation for the synthetic contract, not a result about real observers.

Define support-based attention diversity as:

`D_A = |union_i support(A_i)| / sum_i |support(A_i)|`.

With equal per-observer budgets `b`, the denominator is `m*b`. Perfectly homogeneous observers have `D_A = 1/m` when their shared support has size `b`; non-overlapping supports approach `D_A = 1`. The quantity measures non-redundant support, not semantic diversity or intelligence.

The cost-matched C4 comparison holds observer count, per-observer budget, and total attention slots constant. It varies how many observers explore outside the learned expert support. Therefore any difference in shifted-regime coverage is not attributable to gross slot count within this synthetic contract, although the instrument still abstracts away sensing quality and adjudication costs.

## Claim boundary

Definitions: the optimization, meaning, efficiency, and support quantities above.

Mechanism hypothesis: lossy compression creates structured blind spots; heterogeneous support can preserve residual causal dimensions.

Empirical conjectures: C1 and C4 in `claims/claims.json`, plus all market, language, and expertise claims. Those require controlled extensions with independent outcomes and cost accounting.
