"""Prospective adjudication-limited exploration experiment.

This is a synthetic instrument for measuring the tradeoff between novel-signal
coverage and the cost of evaluating an expanding candidate set. It is not
human, market, or production-model evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import random
from statistics import mean, pstdev


@dataclass(frozen=True)
class AdjudicationConfig:
    feature_count: int = 100
    causal_width: int = 5
    observer_budget: int = 5
    total_observers: int = 21
    adjudication_budget: int = 20
    trials: int = 2000
    seeds: tuple[int, ...] = tuple(range(20))
    exploratory_counts: tuple[int, ...] = (0, 1, 2, 5, 10, 20)
    stable_causal: tuple[int, ...] = (0, 1, 2, 3, 4)
    shifted_causal: tuple[int, ...] = (50, 51, 52, 53, 54)

    def validate(self) -> None:
        if self.feature_count <= 0 or self.causal_width <= 0:
            raise ValueError("feature_count and causal_width must be positive")
        if self.observer_budget <= 0 or self.total_observers <= 0:
            raise ValueError("observer budget and observer count must be positive")
        if self.adjudication_budget <= 0 or self.trials <= 0 or not self.seeds:
            raise ValueError("adjudication budget, trials, and seeds must be positive")
        if max(self.exploratory_counts, default=0) > self.total_observers - 1:
            raise ValueError("exploratory observers cannot exceed non-expert observers")
        for causal in (self.stable_causal, self.shifted_causal):
            if len(causal) != self.causal_width or any(i >= self.feature_count for i in causal):
                raise ValueError("causal features must fit the feature space")


def _accuracy(rng: random.Random, support: set[int], causal: set[int], config: AdjudicationConfig) -> float:
    retained = support & causal
    correct = 0
    ordered_causal = sorted(causal)
    for _ in range(config.trials):
        values = [1 if rng.random() >= 0.5 else -1 for _ in ordered_causal]
        truth = 1 if sum(values) >= 0 else -1
        observed = sum(value for value, feature in zip(values, ordered_causal) if feature in retained)
        if (1 if observed >= 0 else -1) == truth:
            correct += 1
    return correct / config.trials


def _mean_metrics(rows: list[dict[str, float | int]]) -> dict[str, float | int]:
    result: dict[str, float | int] = {}
    for key in rows[0]:
        values = [float(row[key]) for row in rows]
        result[key] = mean(values)
        if key in {"accuracy", "novel_signal_coverage", "false_positive_rate", "net_utility"}:
            result[f"std_{key}"] = pstdev(values)
    return result


def _one_policy(config: AdjudicationConfig, seed: int, explorers: int, policy: str, active_causal: tuple[int, ...] | None = None, adjudication_budget: int | None = None) -> dict[str, float | int]:
    rng = random.Random(seed + explorers * 10007)
    expert = set(config.stable_causal)
    if policy == "homogeneous":
        candidates = expert
    else:
        exploratory_supports = [set(rng.sample(range(config.feature_count), config.observer_budget)) for _ in range(explorers)]
        candidates = expert | set().union(*exploratory_supports) if exploratory_supports else expert
    causal = set(active_causal or config.shifted_causal)
    budget = adjudication_budget if adjudication_budget is not None else config.adjudication_budget

    if policy == "homogeneous":
        selected = expert
        evaluated = len(selected)
    elif policy == "diverse_unfiltered":
        selected = candidates
        evaluated = len(candidates)
    elif policy == "diverse_top_j":
        scored = []
        for feature in candidates:
            # Imperfect but declared adjudication signal: causal candidates are
            # easier to recognize, while noise creates false positives.
            score = (1.0 if feature in causal else 0.0) + rng.gauss(0.0, 0.55)
            scored.append((score, feature))
        scored.sort(reverse=True)
        selected = {feature for _, feature in scored[: budget]}
        evaluated = min(len(candidates), budget)
    elif policy == "oracle":
        selected = set(sorted(candidates & causal)[: budget])
        evaluated = min(len(candidates), budget)
    else:
        raise ValueError(f"unknown policy: {policy}")

    accuracy = _accuracy(random.Random(seed * 31 + explorers + len(policy)), selected, causal, config)
    false_positives = len(selected - causal)
    false_positive_rate = false_positives / len(selected) if selected else 0.0
    coverage = len(selected & causal) / config.causal_width
    sampling_operations = config.total_observers * config.observer_budget
    observation_cost = sampling_operations * 0.001
    adjudication_cost = evaluated * 0.002
    false_positive_cost = false_positives * 0.003
    net_utility = accuracy - observation_cost - adjudication_cost - false_positive_cost

    return {
        "accuracy": accuracy,
        "novel_signal_coverage": coverage,
        "candidate_count": len(candidates),
        "sampling_operations": sampling_operations,
        "evaluated_candidates": evaluated,
        "false_positive_rate": false_positive_rate,
        "adjudication_cost": adjudication_cost,
        "net_utility": net_utility,
    }


def run_adjudication_experiment(config: AdjudicationConfig | None = None) -> dict:
    config = config or AdjudicationConfig()
    config.validate()
    policies = ["homogeneous", "diverse_unfiltered", "diverse_top_j", "oracle"]
    sweep = []
    for explorers in config.exploratory_counts:
        row: dict[str, object] = {
            "exploratory_observers": explorers,
            "total_observers": config.total_observers,
            "total_attention_slots": config.total_observers * config.observer_budget,
        }
        for policy in policies:
            stable_metrics = [_one_policy(config, seed, explorers, policy, config.stable_causal) for seed in config.seeds]
            shifted_metrics = [_one_policy(config, seed, explorers, policy, config.shifted_causal) for seed in config.seeds]
            shifted = _mean_metrics(shifted_metrics)
            stable = _mean_metrics(stable_metrics)
            shifted["stable_accuracy"] = stable["accuracy"]
            shifted["stable_net_utility"] = stable["net_utility"]
            row[policy] = shifted
        sweep.append(row)
    sensitivity = []
    for budget in (5, 10, 20, 40, 65):
        for probability in (0.0, 0.25, 0.5, 0.75, 1.0):
            rows = []
            for seed in config.seeds:
                stable = _one_policy(config, seed, max(config.exploratory_counts), "diverse_top_j", config.stable_causal, budget)
                shifted = _one_policy(config, seed, max(config.exploratory_counts), "diverse_top_j", config.shifted_causal, budget)
                rows.append({"stable_accuracy": stable["accuracy"], "stable_net_utility": stable["net_utility"], "stable_false_positive_rate": stable["false_positive_rate"], "accuracy": shifted["accuracy"], "net_utility": shifted["net_utility"], "false_positive_rate": shifted["false_positive_rate"]})
            sensitivity.append({
                "adjudication_budget": budget,
                "regime_change_probability": probability,
                "expected_accuracy": mean((1 - probability) * row["stable_accuracy"] + probability * row["accuracy"] for row in rows),
                "expected_net_utility": mean((1 - probability) * row["stable_net_utility"] + probability * row["net_utility"] for row in rows),
                "false_positive_rate": mean((1 - probability) * row["stable_false_positive_rate"] + probability * row["false_positive_rate"] for row in rows),
            })
    return {
        "schema_version": "1.0",
        "status": "synthetic_fixture_not_empirical",
        "instrument": "adjudication_limited_exploration",
        "claim_targets": [],
        "config": {
            "feature_count": config.feature_count,
            "causal_width": config.causal_width,
            "observer_budget": config.observer_budget,
            "total_observers": config.total_observers,
            "total_attention_slots": config.total_observers * config.observer_budget,
            "adjudication_budget": config.adjudication_budget,
            "trials_per_seed": config.trials,
            "seeds": list(config.seeds),
            "exploratory_counts": list(config.exploratory_counts),
            "adjudication_signal": "causal candidates receive mean score 1.0; irrelevant candidates mean 0.0; Gaussian noise sigma 0.55",
        },
        "policies": {
            "homogeneous": "all observers share the expert support",
            "diverse_unfiltered": "all union candidates are retained",
            "diverse_top_j": "union candidates ranked by noisy adjudication and truncated at J",
            "oracle": "causal candidates retained up to J; upper-bound control",
        },
        "diversity_sweep": sweep,
        "regime_probability_sweep": sensitivity,
        "interpretation_boundary": "This instrument prices declared observation, adjudication, and false-positive proxies. It is not evidence about human, market, or production-model performance.",
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(run_adjudication_experiment(), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
