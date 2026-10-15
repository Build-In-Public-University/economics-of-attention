"""Synthetic attention/compression regime-shift instrument.

This measures representational retention and action accuracy under a declared
feature budget. It is not a model of human cognition or market behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
import random
from statistics import mean, pstdev
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    feature_count: int = 100
    causal_width: int = 5
    observer_budget: int = 5
    explorer_count: int = 20
    trials: int = 2000
    seeds: tuple[int, ...] = tuple(range(20))
    stable_causal: tuple[int, ...] = (0, 1, 2, 3, 4)
    shifted_causal: tuple[int, ...] = (50, 51, 52, 53, 54)

    def validate(self) -> None:
        if self.feature_count <= 0 or self.causal_width <= 0:
            raise ValueError("feature_count and causal_width must be positive")
        if self.observer_budget <= 0 or self.explorer_count <= 0:
            raise ValueError("observer budgets and explorer count must be positive")
        if self.trials <= 0 or not self.seeds:
            raise ValueError("trials and seeds must be non-empty")
        for causal in (self.stable_causal, self.shifted_causal):
            if len(causal) != self.causal_width or any(i >= self.feature_count for i in causal):
                raise ValueError("causal features must fit the declared feature space")


def _sign(value: int) -> int:
    return 1 if value >= 0 else -1


def _accuracy(rng: random.Random, support: set[int], causal: set[int], config: ExperimentConfig) -> float:
    """Score an observer whose representation preserves only `support`.

    The observer forms the best available action from the retained causal
    features. Missing causal features remain unobserved, not imputed.
    """
    retained = support & causal
    correct = 0
    for _ in range(config.trials):
        values = [1 if rng.random() >= 0.5 else -1 for _ in range(config.causal_width)]
        truth = _sign(sum(values))
        observed = sum(values[i] for i, feature in enumerate(sorted(causal)) if feature in retained)
        if _sign(observed) == truth:
            correct += 1
    return correct / config.trials


def _condition(config: ExperimentConfig, seed: int, causal: tuple[int, ...], stable: bool) -> dict[str, dict[str, float | int]]:
    rng = random.Random(seed)
    expert = set(config.stable_causal)
    novice = set(rng.sample(range(config.feature_count), config.observer_budget))
    explorers = [set(rng.sample(range(config.feature_count), config.observer_budget)) for _ in range(config.explorer_count)]
    heterogeneous = expert | set().union(*explorers)
    causal_set = set(causal)
    local = {
        "expert": (expert, 1),
        "novice": (novice, 1),
        "heterogeneous": (heterogeneous, config.explorer_count + 1),
    }
    out: dict[str, dict[str, float | int]] = {}
    salts = {"expert": 11, "novice": 23, "heterogeneous": 37}
    for name, (support, observer_count) in local.items():
        score_rng = random.Random(seed * 1009 + salts[name])
        out[name] = {
            "accuracy": _accuracy(score_rng, support, causal_set, config),
            "novel_signal_coverage": len(support & causal_set) / config.causal_width,
            "retained_features": len(support),
            "observer_count": observer_count,
        }
    return out


def _aggregate(rows: list[dict[str, dict[str, float | int]]]) -> dict[str, dict[str, float | int]]:
    names = rows[0].keys()
    result: dict[str, dict[str, float | int]] = {}
    for name in names:
        result[name] = {}
        for metric in ("accuracy", "novel_signal_coverage", "retained_features", "observer_count"):
            values = [float(row[name][metric]) for row in rows]
            result[name][metric] = mean(values)
            if metric in ("accuracy", "novel_signal_coverage"):
                result[name][f"std_{metric}"] = pstdev(values)
    return result


def run_experiment(config: ExperimentConfig | None = None) -> dict:
    config = config or ExperimentConfig()
    config.validate()
    stable = [_condition(config, seed, config.stable_causal, True) for seed in config.seeds]
    shifted = [_condition(config, seed, config.shifted_causal, False) for seed in config.seeds]
    return {
        "schema_version": "1.0",
        "status": "synthetic_fixture_not_empirical",
        "instrument": "attention_compression_regime_shift",
        "claim_targets": ["C1", "C4"],
        "config": {
            "feature_count": config.feature_count,
            "causal_width": config.causal_width,
            "observer_budget": config.observer_budget,
            "explorer_count": config.explorer_count,
            "trials_per_seed": config.trials,
            "seeds": list(config.seeds),
            "stable_causal_features": list(config.stable_causal),
            "shifted_causal_features": list(config.shifted_causal),
        },
        "conditions": {"stable": _aggregate(stable), "regime_shift": _aggregate(shifted)},
        "interpretation_boundary": "This instrument measures a declared synthetic representation mechanism; it is not evidence about human, market, or production-model performance.",
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(run_experiment(), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
