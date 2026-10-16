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

    def test_homogeneous_control_has_constant_unique_support_but_same_sampling_budget(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        for row in result["diversity_sweep"]:
            homogeneous = row["homogeneous"]
            self.assertEqual(homogeneous["candidate_count"], 5)
            self.assertEqual(homogeneous["sampling_operations"], 105)

    def test_sensitivity_sweep_varies_adjudication_budget_and_shift_probability(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        self.assertTrue(result["regime_probability_sweep"])
        self.assertEqual({row["adjudication_budget"] for row in result["regime_probability_sweep"]}, {5, 10, 20, 40, 65})
        self.assertEqual({row["regime_change_probability"] for row in result["regime_probability_sweep"]}, {0.0, 0.25, 0.5, 0.75, 1.0})

    def test_regime_risk_scores_candidates_against_active_regime(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1), trials=200))
        rows = result["regime_probability_sweep"]
        stable = next(row for row in rows if row["adjudication_budget"] == 20 and row["regime_change_probability"] == 0.0)
        shifted = next(row for row in rows if row["adjudication_budget"] == 20 and row["regime_change_probability"] == 1.0)
        self.assertGreater(stable["expected_accuracy"], shifted["expected_accuracy"])
        self.assertLessEqual(stable["false_positive_rate"], shifted["false_positive_rate"])

    def test_reports_paired_uncertainty_and_two_budget_frontier(self):
        result = run_adjudication_experiment(AdjudicationConfig(seeds=(0, 1, 2), trials=100))
        paired = result["paired_budget_comparison"]
        self.assertEqual(len(paired["j10_vs_j20"]), 3)
        self.assertEqual(paired["j10_wins"] + paired["j20_wins"] + paired["ties"], 3)
        frontier = result["attention_frontier"]
        self.assertEqual(len(frontier), 6 * 5 * 5)
        self.assertEqual(len(result["attention_frontier_optima"]), 5)
        low_risk = next(row for row in result["attention_frontier_optima"] if row["regime_change_probability"] == 0.0)
        self.assertEqual(low_risk["co_optimal_adjudication_budgets"], [5, 10, 20, 40, 65])


if __name__ == "__main__":
    unittest.main()
