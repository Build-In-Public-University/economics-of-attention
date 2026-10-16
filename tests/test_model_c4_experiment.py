import unittest

from src.model_c4_experiment import ModelC4Config, run_model_c4


class ModelC4Tests(unittest.TestCase):
    def test_receipt_has_matched_sampling_and_regime_results(self):
        result = run_model_c4(ModelC4Config(seeds=(0, 1), calibration_examples=40, test_examples=80))
        self.assertEqual(result["status"], "synthetic_fixture_not_empirical")
        self.assertEqual(result["config"]["sampling_operations"], 105)
        self.assertEqual(len(result["results"]), 6 * 5)
        self.assertEqual({row["explorers"] for row in result["results"]}, {0, 1, 2, 5, 10, 20})

    def test_heterogeneous_views_recover_shifted_signal(self):
        result = run_model_c4(ModelC4Config(seeds=tuple(range(5)), calibration_examples=100, test_examples=200))
        row = next(row for row in result["results"] if row["explorers"] == 20 and row["adjudication_budget"] == 10)
        self.assertGreater(row["heterogeneous_shifted"]["novel_signal_coverage"], row["homogeneous_shifted"]["novel_signal_coverage"])
        self.assertGreater(row["heterogeneous_shifted"]["accuracy"], row["homogeneous_shifted"]["accuracy"])

    def test_adjudication_is_bounded(self):
        result = run_model_c4(ModelC4Config(seeds=(0, 1), calibration_examples=40, test_examples=80))
        for row in result["results"]:
            self.assertLessEqual(row["heterogeneous_shifted"]["evaluated_candidates"], row["adjudication_budget"])
            self.assertEqual(row["heterogeneous_shifted"]["sampling_operations"], 105)


if __name__ == "__main__":
    unittest.main()
