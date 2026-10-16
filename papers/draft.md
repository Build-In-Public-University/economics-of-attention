# The Economics of Attention

## From Shannon Entropy to Hayekian Prices to Transformers

### Why information abundance makes discrimination—not information—the scarce resource

## Abstract

Modern information systems have become exceptionally good at producing, transmitting, storing, and copying information. Understanding has not scaled in proportion. This paper proposes that the bottleneck moves under abundance: from access to information toward the selective discrimination of consequential distinctions.

The framework treats an observer as a finite system that maps a potentially observable environment through an attention policy, compresses the selected representation, chooses an action, and updates its policy from feedback. Meaning is defined operationally as the improvement in achievable action value produced by preserving a distinction. Attention is sustainable when this expected action improvement exceeds the cost of sensing, processing, storing, interpreting, delaying, and switching attention.

The paper places this model beside Shannon's semantic-neutral information theory, Hayek's distributed-knowledge price signal, Grossman–Stiglitz's costly-information constraint, and Transformer attention's query-conditioned relational weighting. The claim is structural rather than historical: these systems instantiate related resource-constrained selection problems, not identical mechanisms. The paper develops propositions about information abundance, compression residuals, heterogeneous attention, alpha decay, linguistic priors, and semantic hysteresis, then specifies falsifiable tests. No empirical result is claimed in this draft.

## 1. The post-information problem

Let the environment produce potentially observable information:

\[
X_t=(x_{1,t},\ldots,x_{n,t}), \qquad H(X_t).
\]

An observer has bounded resources \(B_i<\infty\). As information production becomes cheaper, \(n_t\) and potentially \(H(X_t)\) rise while the observer's processing capacity remains bounded. The observer cannot process every available variable. It must select.

Under scarcity, the problem is obtaining information. Under abundance, the problem is deciding what deserves processing. The central thesis is:

\[
\boxed{\text{Information abundance shifts scarcity from information to efficient discrimination.}}
\]

This is not a claim that more information is intrinsically harmful. It is a claim about a fixed-capacity observer facing an expanding candidate set.

## 2. Attention and compression

Let attention depend on objective or query \(q_{i,t}\) and prior conceptual structure \(w_{i,t}\):

\[
Y_{i,t}=A_{i,t}(X_t\mid q_{i,t},w_{i,t}), \qquad Z_{i,t}=\phi_i(Y_{i,t}).
\]

The representation \(Z\) is smaller than the environment and therefore lossy. There may be distinct states \(S_1\neq S_2\) for which \(Z(S_1)=Z(S_2)\), even though the distinction later changes action value. Compression is therefore both the source of efficiency and the source of model blindness.

The attention policy creates a partition of reality: its support is what the observer can distinguish in the current decision window, while variables outside that support are operationally invisible. Every compression step discards distinctions, even when it does not delete the underlying data. A discarded distinction becomes consequential when a regime change moves it across the action boundary. The relevant review question is therefore not only “how much information is available?” but “which distinctions can this observer literally see, which are suppressed, and what would make a suppressed distinction matter?”

The observer acts through:

\[
a^*_{i,t}=\arg\max_a E[U_i(a,S_t)\mid Z_{i,t}].
\]

The full theory is a control loop:

\[
S_t\rightarrow X_t\rightarrow A_t\rightarrow Z_t\rightarrow a_t\rightarrow r_t\rightarrow A_{t+1}.
\]

## 3. Meaning as action-relevant information

Define the action-relative meaning of an observation \(x\) as:

\[
M_i(x\mid Z)=\max_a E[U_i(a,S)\mid Z,x]-\max_a E[U_i(a,S)\mid Z].
\]

This is a definition of a decision-relevant quantity, not a claim that all meaning is exhausted by instrumental utility. It distinguishes uncertainty reduction from consequential uncertainty reduction. High Shannon information can have negligible \(M\); a small signal can have large \(M\) when it changes an important decision.

## 4. Costly attention and efficiency

Attention cost includes sensing, acquisition, processing, storage, interpretation, delay, coordination, and switching:

\[
C_i(A)=C_{sensing}+C_{processing}+C_{storage}+C_{interpretation}+C_{delay}.
\]

With hysteresis penalty \(\lambda_iD(A,A_{i,t-1})\), the proposed optimization is:

\[
A^*_{i,t}=\arg\max_A\left\{E\left[\max_a E[U_i(a,S_t)\mid\phi(A(X_t\mid q,w))]\right]-C_i(A)-\lambda_iD(A,A_{i,t-1})\right\}.
\]

For a baseline value \(V_0\) and value under \(A\), define attention efficiency:

\[
\eta_A=\frac{V_A-V_0}{C(A)}.
\]

The local viability condition is \(V_A-V_0>C(A)\), with units and horizon specified by the application. This is the paper's central accounting identity, not a measured law.

## 5. Markets as distributed attention

A market contains heterogeneous costly observers. Their actions are generated from different attention policies and aggregated into price:

\[
X_{distributed}\rightarrow\{A_i(X)\}\rightarrow\{a_i\}\rightarrow p.
\]

Price is a low-dimensional, lossy compression of dispersed knowledge: it changes behavior without transmitting every underlying observation. Grossman–Stiglitz supplies the constraint that if all information were costlessly and perfectly incorporated, incentives to acquire information would disappear. Residual uncertainty is therefore not merely a defect; it is part of the incentive structure for observation.

Alpha is defined here as the temporary private value of an unsocialized consequential distinction. If an observer identifies \(z\) such that conditioning on \(z\) improves action, imitation and capital diffusion should increase market attention to \(z\), reducing private excess value:

\[
\text{residual}\rightarrow\text{attention}\rightarrow\text{profit}\rightarrow\text{imitation}\rightarrow\text{recompression}.
\]

This is a bounded hypothesis, not a claim about any particular strategy.

## 6. Transformer attention as structural analogue

Transformer attention computes query-conditioned relational weighting:

\[
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V.
\]

The relevant analogy is structural: abundant context is not treated uniformly; relevance is computed relative to a query. A market participant's query might be “what changes expected return under this horizon and risk constraint?” The analogy does not imply that markets literally execute Transformer layers, that human cognition is mathematically identical to neural attention, or that Vaswani et al. proposed an economic theory.

Multiple observers can be represented as heterogeneous attention functions \(A_1(X),\ldots,A_m(X)\). The collective observable capacity is approximately the union of their retained supports, but only if an adjudication mechanism allows minority observations to be evaluated rather than suppressed.

## 7. Expertise, language, and hysteresis

Expertise is learned low-cost compression in familiar environments. It can reduce noise while increasing the risk that a formerly irrelevant variable is suppressed after a regime change. Novices process more noise but may preserve weak signals that experts have learned to ignore. The resulting design hypothesis is not “novices are better”; it is that robust networks need enough heterogeneity to expose residuals and enough expertise to evaluate them.

Language transmits attention priors. A word can package expected salient distinctions, ignored distinctions, and causal relationships, reducing the cost of reproducing a previously useful filter. This is a restrained linguistic-relativity claim: language changes the cost and default weighting of distinctions without determining all possible thought.

Semantic hysteresis appears when historically invested categories resist replacement:

\[
V(A_{new})-V(A_{old})<\lambda D(A_{new},A_{old}).
\]

Credentials, titles, metrics, and institutional routines can persist because the cost of changing the attention infrastructure exceeds the perceived gain. The old compression then becomes a potential blind spot.

## 8. Propositions and tests

1. Information abundance: under a fixed attention budget, increasing the candidate set reduces expected retention of consequential features for undirected sampling, while a discriminative policy can protect retention.
2. Action-relevant meaning: action-change measures predict consequential behavior better than surprise alone.
3. Attention efficiency: persistent filters have positive expected action value net of operating cost.
4. Compression residuals: systems optimized on stable distributions fail more often on causal features outside their retained representation after regime change.
5. Heterogeneous attention: heterogeneous systems detect novelty better than homogeneous expert systems under controlled regime shifts, provided minority observations survive adjudication.
6. Socialization of distinctions: newly profitable signals lose excess value as attention diffuses toward them.
7. Linguistic attention: labels change feature weighting and valuation for otherwise identical inputs.
8. Semantic hysteresis: historically established categories update more slowly under contradictory evidence than neutral new categories.

Empirical claims remain prospective with respect to external systems. Synthetic receipts establish behavior of the declared instruments only; they do not establish effects in humans, markets, institutions, or production AI systems. The associated claim ledger records the falsifiers and evidence ceilings.

## 9. Implications and limits

The framework suggests that AI scaling will increasingly face an allocation problem: more context without better routing, retrieval, sparsity, specialization, or adaptive memory reproduces the human information-abundance problem inside machine systems. Institutions likewise need forgetting, dissent, anomaly detection, and heterogeneous observation rather than unrestricted measurement alone.

The two synthetic sweeps expose a cycle rather than a one-directional overload law: abundance pressures observers toward compression; compression creates structured blind spots under regime change; non-redundant exploration repairs some blind spots; and the resulting candidate set must eventually be compressed again. Experiment 3 explicitly prices sampling, adjudication, and false-positive proxies. Its corrected regime-risk sweep produces a fixture-dependent exploration–compression frontier, not a universal optimum.

### Synthetic results: exploration as insurance against compression failure

The synthetic instruments separate three mechanisms. First, under a fixed attention budget, abundance dilutes undirected sampling while a learned filter protects known consequential features. Second, the same compression that produces low-cost performance in the stable regime creates blindness when causality shifts. Third, the two-budget Experiment 3 frontier allocates attention differently as the probability of compression failure rises. At low regime risk, the representative optimum is `E=0` with all `J` values co-optimal because only five candidates exist; at `p=0.5`, the highest observed policy is `(E,J)=(10,10)` with expected net utility `0.6393`; at `p=0.75` and `p=1`, it is `(20,10)` with utilities `0.6114` and `0.5856`. The first two low-risk rows are ties, and the receipt uses the smallest-budget tie-break rather than treating `J=5` as uniquely superior.

The paired `J=10` versus `J=20` comparison at maximum exploration and `p=0.5` gives mean difference `0.00125`, standard deviation `0.06113`, a 95% normal-approximation interval `[-0.02554,0.02804]`, and a 10–10 seed-level win split. The point estimate is therefore not a meaningful claim of superiority. The stronger result is the policy transition across environmental risk:

\[
\text{low regime risk}\rightarrow\text{exploit existing compression}
\]
\[
\text{intermediate risk}\rightarrow\text{partial exploration + bounded adjudication}
\]
\[
\text{high regime risk}\rightarrow\text{broader exploration + bounded adjudication}.
\]

In this fixture, exploration is insurance against compression failure. Expertise is cheap exploitation of a known regime; exploration pays to preserve access to distinctions the current model suppresses; adjudication prevents that insurance from becoming unbounded noise. This is a synthetic mechanism result, not evidence about human, market, or production-model behavior.

The next instrument instantiates C4 as a learned synthetic classifier with constrained feature views rather than only abstract support sets. Twenty-one classifiers receive five-feature views, preserving 105 gross sampling operations in every cell. A homogeneous network repeatedly inspects the stable specialist support; a heterogeneous network adds scouts with independently sampled views, then uses a calibration-based adjudicator capped at `J` retained features. In the default receipt, at maximum exploration and `J=10`, shifted accuracy is `0.8448` for the heterogeneous network versus `0.4990` for the homogeneous control, with heterogeneous net utility `0.7771`. At `J=20`, accuracy falls to `0.8232` and net utility to `0.7353`, illustrating that retaining more candidate information is not equivalent to producing more value. The classifiers infer feature relevance from finite calibration examples, but this is not a test of LLMs, neural networks, or independently capable AI agents, and it is not evidence about production AI systems.

A fourth instrument changes the substrate rather than adding abstraction to the feature classifier. The corrected v4.1 version cost-matches six document slots per condition, enforces a three-claim generation budget, and removes the shifted-topic ontology from adjudication. It presents bounded textual contexts, requires natural-language claims, and applies a fixed claim-budget adjudicator using an action-change proxy relative to the stable summary. In the deterministic local receipt, both conditions emit three claims; homogeneous shifted contexts expose zero novel claims while heterogeneous contexts expose seven across five decision seeds. A `gpt-5.6-luna` Codex receipt also exposes zero versus twelve novel claims across five seeds. Its sampled views have unequal token counts, which are recorded rather than hidden; the provider result is therefore a replication with a residual token-cost confound, not the final token-matched test. These receipts establish only behavior of the constructed document/claim pipeline. They do not establish open-ended semantic reasoning or production-model performance.

The framework does not establish that more diversity is always better, that all residuals deserve attention, or that a single scalar captures intelligence. The proposed ratio requires compatible units, explicit horizons, and a defined baseline. The model also leaves open how observers learn costs, how utility is measured under conflict, and how adjudication should trade minority preservation against noise.

## Conclusion

Shannon separated information transmission from semantic meaning. Hayek showed how distributed knowledge can coordinate through compressed price signals. Grossman and Stiglitz showed why costly information requires residual ignorance. Transformers demonstrate learned, query-conditioned weighting within abundant context.

Taken together, they motivate a resource-constrained selection problem:

\[
\boxed{\text{Adaptive intelligence is efficient preservation of consequential distinctions.}}
\]

The most adaptive system is not the one that sees the most. It is the one that ignores the most without ignoring what matters—and can discover when yesterday's noise has become today's signal.
