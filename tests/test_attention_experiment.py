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


if __name__ == "__main__":
    unittest.main()
