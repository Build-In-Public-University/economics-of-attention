import unittest

from src.adjudication_experiment import AdjudicationConfig, run_adjudication_experiment


class AdjudicationExperimentTests(unittest.TestCase):
    def test_receipt_declares_adjudication_budget_and_controls(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        self.assertEqual(result["status"], "synthetic_fixture_not_empirical")
        self.assertIn("diversity_sweep", result)
        self.assertIn("diverse_top_j", result["policies"])
        self.assertIn("oracle", result["policies"])

    def test_unfiltered_exploration_pays_more_candidate_cost(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        rows = result["diversity_sweep"]
        low = next(row for row in rows if row["exploratory_observers"] == 0)
        high = next(row for row in rows if row["exploratory_observers"] == 20)
        self.assertGreater(high["diverse_unfiltered"]["candidate_count"], low["diverse_unfiltered"]["candidate_count"])
        self.assertGreater(high["diverse_unfiltered"]["adjudication_cost"], low["diverse_unfiltered"]["adjudication_cost"])

    def test_top_j_bounds_candidates_and_reports_false_positives(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        for row in result["diversity_sweep"]:
            top_j = row["diverse_top_j"]
            self.assertLessEqual(top_j["evaluated_candidates"], result["config"]["adjudication_budget"])
            self.assertGreaterEqual(top_j["false_positive_rate"], 0.0)
            self.assertLessEqual(top_j["false_positive_rate"], 1.0)

    def test_net_utility_is_not_identical_to_accuracy(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        rows = result["diversity_sweep"]
        self.assertTrue(any(row["diverse_unfiltered"]["net_utility"] != row["diverse_unfiltered"]["accuracy"] for row in rows))


if __name__ == "__main__":
    unittest.main()
