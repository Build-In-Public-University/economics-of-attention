import unittest
import inspect

from src.semantic_c4_experiment import Config, adjudicate, run


class SemanticC4Tests(unittest.TestCase):
    def test_local_contract_has_bounded_claims_and_receipts(self):
        result = run("local", config=Config(seeds=(0, 1)))
        self.assertEqual(result["status"], "synthetic_fixture_not_empirical")
        self.assertEqual(len(result["rows"]), 8)
        self.assertTrue(all(row["selected_count"] <= 4 for row in result["rows"]))
        self.assertTrue(all(row["context_hash"] for row in result["rows"]))
        self.assertTrue(all(row["candidate_count"] <= 3 for row in result["rows"]))
        for regime in ("stable", "shifted"):
            by_policy = [row for row in result["rows"] if row["regime"] == regime]
            self.assertEqual({row["context_slots"] for row in by_policy}, {6})

    def test_local_scout_view_exposes_shifted_claim(self):
        result = run("local", config=Config(seeds=(0, 1, 2, 3, 4)))
        homogeneous = sum(row["novel_claims"] for row in result["rows"] if row["policy"] == "homogeneous" and row["regime"] == "shifted")
        heterogeneous = sum(row["novel_claims"] for row in result["rows"] if row["policy"] == "heterogeneous" and row["regime"] == "shifted")
        self.assertEqual(homogeneous, 0)
        self.assertGreater(heterogeneous, 0)

    def test_adjudicator_has_no_shifted_topic_whitelist(self):
        source = inspect.getsource(adjudicate)
        self.assertNotIn("sensor_drift", source)
        self.assertNotIn("bypass_leak", source)
        self.assertNotIn("auxiliary_pump", source)


if __name__ == "__main__":
    unittest.main()
