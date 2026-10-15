import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class RepositoryInvariants(unittest.TestCase):
    def test_claims_have_falsifiers_and_evidence_ceiling(self):
        payload = json.loads((ROOT / "claims/claims.json").read_text())
        self.assertGreater(len(payload["claims"]), 0)
        for claim in payload["claims"]:
            self.assertTrue(claim["falsifier"])
            self.assertTrue(claim["evidence_ceiling"])

    def test_boundary_preserves_non_empirical_status(self):
        readme = (ROOT / "README.md").read_text()
        boundary = (ROOT / "docs/RESEARCH-BOUNDARY.md").read_text()
        self.assertIn("No empirical results are claimed", readme)
        self.assertIn("Not established", boundary)

    def test_hub_connection_is_explicit(self):
        connection = (ROOT / "docs/HUB-CONNECTION.md").read_text()
        self.assertIn("dynamic-verification-knowledge", connection)
        self.assertIn("local_pointer_only", connection)

    def test_c1_is_calibrated_to_the_abundance_instrument(self):
        claims = json.loads((ROOT / "claims/claims.json").read_text())
        c1 = next(claim for claim in claims["claims"] if claim["id"] == "C1")
        self.assertIn("candidate observations", c1["wording"])
        self.assertIn("preferentially allocates", c1["wording"])
        self.assertIn("signal dilution", c1["falsifier"])

    def test_experiment_3_remains_synthetic(self):
        receipt = json.loads((ROOT / "artifacts/attention-v2/adjudication-limited-exploration.json").read_text())
        self.assertEqual(receipt["status"], "synthetic_fixture_not_empirical")
        self.assertEqual(receipt["config"]["adjudication_budget"], 20)

if __name__ == "__main__":
    unittest.main()
