import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game/clean-session.html"
PDF = ROOT / "game/standard-paper.pdf"


class CleanSessionTests(unittest.TestCase):
    def test_control_artifact_exists_and_is_a_pdf(self):
        self.assertTrue(PDF.exists())
        self.assertGreater(PDF.stat().st_size, 1000)
        self.assertEqual(PDF.read_bytes()[:5], b"%PDF-")

    def test_same_questions_and_hidden_arm_contract_are_present(self):
        text = GAME.read_text()
        for marker in ("standard_pdf", "progressive", "BUDGET=180", "source removed", "attention-clean-session-v0.1", "question_ids"):
            self.assertIn(marker, text)
        self.assertIn("standard-paper.pdf", text)
        self.assertIn("progressive-compression reading surface", text)

    def test_clean_session_has_no_network_dependency(self):
        text = GAME.read_text()
        self.assertNotIn("fetch(", text)
        self.assertNotIn("https://", text)

    def test_receipt_separates_reading_and_quiz_time(self):
        text = GAME.read_text()
        for marker in ("reading_seconds", "quiz_response_seconds", "U(T_R)/T_R"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()