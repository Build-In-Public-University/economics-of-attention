import unittest

from src.attention_experiment import ExperimentConfig, run_experiment


class AttentionExperimentTests(unittest.TestCase):
    def test_receipt_has_declared_conditions_and_metrics(self):
        result = run_experiment(ExperimentConfig(seeds=(0, 1), trials=200))
        self.assertEqual(result["status"], "synthetic_fixture_not_empirical")
        self.assertIn("stable", result["conditions"])
        self.assertIn("regime_shift", result["conditions"])
        self.assertIn("expert", result["conditions"]["regime_shift"])
        self.assertIn("heterogeneous", result["conditions"]["regime_shift"])

    def test_expert_beats_novice_in_stable_regime(self):
        result = run_experiment(ExperimentConfig(seeds=tuple(range(8)), trials=1000))
        stable = result["conditions"]["stable"]
        self.assertGreater(stable["expert"]["accuracy"], stable["novice"]["accuracy"])

    def test_heterogeneous_network_beats_expert_after_shift(self):
        result = run_experiment(ExperimentConfig(seeds=tuple(range(8)), trials=1000))
        shifted = result["conditions"]["regime_shift"]
        self.assertGreater(shifted["heterogeneous"]["accuracy"], shifted["expert"]["accuracy"])
        self.assertGreater(shifted["heterogeneous"]["novel_signal_coverage"], shifted["expert"]["novel_signal_coverage"])

    def test_information_abundance_sweep_holds_budget_fixed(self):
        result = run_experiment(ExperimentConfig(seeds=(0, 1), trials=200))
        sweep = result["information_abundance_sweep"]
        self.assertEqual([row["feature_count"] for row in sweep], [5, 10, 20, 50, 100, 200, 500, 1000])
        self.assertEqual({row["attention_budget"] for row in sweep}, {5})
        self.assertGreater(sweep[0]["random"]["accuracy"], sweep[-1]["random"]["accuracy"])
        self.assertGreater(sweep[0]["random"]["novel_signal_coverage"], sweep[-1]["random"]["novel_signal_coverage"])

    def test_cost_matched_homogeneous_network_loses_after_shift(self):
        result = run_experiment(ExperimentConfig(seeds=tuple(range(8)), trials=1000))
        sweep = result["attention_diversity_sweep"]
        homogeneous = next(row for row in sweep if row["exploratory_observers"] == 0)
        heterogeneous = next(row for row in sweep if row["exploratory_observers"] == 20)
        self.assertEqual(homogeneous["total_observers"], heterogeneous["total_observers"])
        self.assertEqual(homogeneous["total_attention_slots"], heterogeneous["total_attention_slots"])
        self.assertGreater(heterogeneous["regime_shift"]["accuracy"], homogeneous["regime_shift"]["accuracy"])
        self.assertGreater(heterogeneous["attention_diversity"], homogeneous["attention_diversity"])


if __name__ == "__main__":
    unittest.main()
