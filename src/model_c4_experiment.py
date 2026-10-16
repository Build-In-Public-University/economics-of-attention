"""Model-level C4 experiment with constrained specialists, scouts, and adjudication.

This remains a synthetic instrument. Agents learn feature scores from calibration
examples, but the task, views, costs, and regime change are all declared fixtures.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import random
from statistics import mean, pstdev


@dataclass(frozen=True)
class ModelC4Config:
    feature_count: int = 40
    causal_width: int = 5
    view_budget: int = 5
    total_agents: int = 21
    calibration_examples: int = 120
    test_examples: int = 300
    trials: int = 300
    seeds: tuple[int, ...] = tuple(range(20))
    explorers: tuple[int, ...] = (0, 1, 2, 5, 10, 20)
    adjudication_budgets: tuple[int, ...] = (5, 10, 20, 40, 65)
    stable_causal: tuple[int, ...] = (0, 1, 2, 3, 4)
    shifted_causal: tuple[int, ...] = (20, 21, 22, 23, 24)

    def validate(self) -> None:
        if self.feature_count <= 0 or self.causal_width <= 0:
            raise ValueError("feature_count and causal_width must be positive")
        if len(self.stable_causal) != self.causal_width or len(self.shifted_causal) != self.causal_width:
            raise ValueError("causal sets must match causal_width")
        if max(self.shifted_causal) >= self.feature_count:
            raise ValueError("causal features must fit the feature space")
        if self.view_budget <= 0 or self.total_agents <= 0 or self.calibration_examples <= 0:
            raise ValueError("budgets and sample counts must be positive")
        if max(self.explorers, default=0) > self.total_agents - 1:
            raise ValueError("explorers cannot exceed non-specialist agents")


def _examples(rng: random.Random, causal: tuple[int, ...], count: int, feature_count: int) -> tuple[list[list[int]], list[int]]:
    features: list[list[int]] = []
    labels: list[int] = []
    causal_set = set(causal)
    for _ in range(count):
        row = [1 if rng.random() >= 0.5 else -1 for _ in range(feature_count)]
        total = sum(row[index] for index in causal_set)
        features.append(row)
        labels.append(1 if total >= 0 else -1)
    return features, labels


def _correlations(features: list[list[int]], labels: list[int], support: set[int]) -> dict[int, float]:
    if not features:
        return {index: 0.0 for index in support}
    return {index: sum(row[index] * label for row, label in zip(features, labels)) / len(labels) for index in support}


def _accuracy(features: list[list[int]], labels: list[int], weights: dict[int, float]) -> float:
    correct = 0
    for row, label in zip(features, labels):
        score = sum(weight * row[index] for index, weight in weights.items())
        if (1 if score >= 0 else -1) == label:
            correct += 1
    return correct / len(labels) if labels else 0.0


def _run_one(config: ModelC4Config, seed: int, explorers: int, budget: int, regime: str, heterogeneous: bool) -> dict[str, float | int]:
    rng = random.Random(seed * 1009 + explorers * 9176 + budget * 37 + (1 if regime == "shifted" else 0))
    causal = config.stable_causal if regime == "stable" else config.shifted_causal
    calibration_x, calibration_y = _examples(rng, causal, config.calibration_examples, config.feature_count)
    test_x, test_y = _examples(rng, causal, config.test_examples, config.feature_count)
    specialist = set(config.stable_causal)
    if heterogeneous and explorers:
        scout_views = [set(rng.sample(range(config.feature_count), config.view_budget)) for _ in range(explorers)]
    else:
        scout_views = [specialist.copy() for _ in range(explorers)]
    candidates = specialist | set().union(*scout_views) if scout_views else specialist
    support_correlations = _correlations(calibration_x, calibration_y, candidates)
    if heterogeneous:
        ranked = sorted(candidates, key=lambda index: (abs(support_correlations[index]), index), reverse=True)
        selected_indices = ranked[: min(budget, len(ranked))]
    else:
        selected_indices = sorted(specialist)
    weights = {index: support_correlations[index] for index in selected_indices}
    accuracy = _accuracy(test_x, test_y, weights)
    false_positives = len(set(selected_indices) - set(causal))
    candidate_count = len(candidates)
    evaluated = min(candidate_count, budget) if heterogeneous else len(specialist)
    sampling_operations = config.total_agents * config.view_budget
    observation_cost = sampling_operations * 0.0005
    adjudication_cost = evaluated * 0.001
    false_positive_cost = false_positives * 0.001
    return {
        "accuracy": accuracy,
        "candidate_count": candidate_count,
        "selected_count": len(selected_indices),
        "novel_signal_coverage": len(set(selected_indices) & set(causal)) / config.causal_width,
        "false_positive_rate": false_positives / len(selected_indices) if selected_indices else 0.0,
        "sampling_operations": sampling_operations,
        "evaluated_candidates": evaluated,
        "net_utility": accuracy - observation_cost - adjudication_cost - false_positive_cost,
    }


def _aggregate(rows: list[dict[str, float | int]]) -> dict[str, float | int]:
    result: dict[str, float | int] = {}
    for key in rows[0]:
        values = [float(row[key]) for row in rows]
        result[key] = mean(values)
        if key in {"accuracy", "net_utility", "novel_signal_coverage"}:
            result[f"std_{key}"] = pstdev(values)
    return result


def run_model_c4(config: ModelC4Config | None = None) -> dict:
    config = config or ModelC4Config()
    config.validate()
    rows = []
    for explorers in config.explorers:
        for budget in config.adjudication_budgets:
            stable_h = _aggregate([_run_one(config, seed, explorers, budget, "stable", False) for seed in config.seeds])
            shifted_h = _aggregate([_run_one(config, seed, explorers, budget, "shifted", False) for seed in config.seeds])
            stable_d = _aggregate([_run_one(config, seed, explorers, budget, "stable", True) for seed in config.seeds])
            shifted_d = _aggregate([_run_one(config, seed, explorers, budget, "shifted", True) for seed in config.seeds])
            rows.append({"explorers": explorers, "adjudication_budget": budget, "homogeneous_stable": stable_h, "homogeneous_shifted": shifted_h, "heterogeneous_stable": stable_d, "heterogeneous_shifted": shifted_d})
    optima = []
    for regime in ("stable", "shifted"):
        best = max(rows, key=lambda row: row[f"heterogeneous_{regime}"]["net_utility"])
        optima.append({"regime": regime, "explorers": best["explorers"], "adjudication_budget": best["adjudication_budget"], "net_utility": best[f"heterogeneous_{regime}"]["net_utility"]})
    return {
        "schema_version": "1.0",
        "status": "synthetic_fixture_not_empirical",
        "instrument": "model_c4_constrained_views",
        "claim_targets": ["C4"],
        "config": {"feature_count": config.feature_count, "view_budget": config.view_budget, "total_agents": config.total_agents, "sampling_operations": config.total_agents * config.view_budget, "calibration_examples": config.calibration_examples, "test_examples": config.test_examples, "seeds": list(config.seeds), "explorers": list(config.explorers), "adjudication_budgets": list(config.adjudication_budgets)},
        "policies": {"homogeneous": "all agents repeatedly inspect the stable specialist support", "heterogeneous": "specialists plus constrained scouts propose features to a bounded correlation adjudicator"},
        "results": rows,
        "optima": optima,
        "interpretation_boundary": "This is a synthetic model-level mechanism test. It is not evidence about human cognition, markets, or production AI systems.",
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(run_model_c4(), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
