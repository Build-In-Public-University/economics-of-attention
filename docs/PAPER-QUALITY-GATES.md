# Scholarly quality gates for the paper

This rubric is adapted from the selection pressure visible in Steph Macurdy's `Logistics of Dispersed Knowledge` (October 2026). It is a review instrument, not evidence that Steph endorses this paper.

The paper should not pass because its prose is coherent. Each major non-definitional claim should survive the following gates.

| Gate | Required question | Hard gate |
|---|---|---|
| Lineage | What unresolved problem does the claim inherit from prior theory? | yes |
| Mechanism | Can the causal or procedural chain be written as arrows? | yes |
| Cost | Who pays for observing, discriminating, retaining, adjudicating, being wrong, or revising? | yes |
| Partition | What can the observer literally see, and what is outside its support? | yes |
| Compression | What information is deliberately discarded, and when could it matter? | yes |
| Consequence | What action, value, prediction, allocation, or learning changes? | yes |
| Evidence level | What is the highest epistemic level actually established? | yes |
| Negative boundary | What plausible stronger interpretation is explicitly rejected? | yes |
| Citation lineage | Are inherited claims tied to verified sources? | yes |
| Falsification | What observation would make the claim be revised? | yes |
| Concrete example | Does the abstraction survive one running case? | no |
| Faithful compression | Can the section reduce to one equation or transformation without distortion? | no |
| Reader attention | Can a reader recover the problem, mechanism, contribution, evidence level, and limitation at `30s -> 3m -> 15m -> full audit` resolutions? | no |

## Required evidence ladder

The repository uses this boundary explicitly:

`simulator behavior -> learned synthetic classifier -> semantic substrate -> production-model behavior -> human/institutional/market behavior`

A receipt may support only the level it actually exercised. A provider-backed semantic run is still a constructed corpus and protocol result. It is not external validation.

## Steph-derived tests applied here

- Prices and claims are partial representations, not complete world states.
- Cost must be connected to the hidden property or decision consequence; arbitrary work is not automatically informative.
- The observation partition is a design variable: who controls what is visible?
- Verification narrows and relocates trust; it does not abolish it.
- A predicate establishes only the distinctions it tests.

## Repository enforcement

`scripts/quality_gate.py` performs the mechanical subset of this review. It checks that the draft contains lineage, mechanism, costs, partition, consequences, explicit boundaries, falsifiers, one running synthetic case, and the four reader resolutions, and that every bounded hypothesis in the claims ledger has a falsifier and evidence ceiling. It deliberately does not pretend to automate scholarly judgment about whether the example is illuminating or whether a citation actually supports an inherited claim.

The report also emits a claim-by-gate matrix for C1–C7. `lineage_presence` means only that a dependency is registered; it is not source support. `source_support` is therefore marked `manual_review` until each inherited claim is checked against the relevant primary source. A `review_required` report is an intentional selection-pressure state: document-level ingredients may pass while individual claims still fail a hard gate.

A hard-gate failure should return the paper to revision rather than be averaged away by strong prose. The meta-question is:

`What had to be true for this paragraph to survive?`
