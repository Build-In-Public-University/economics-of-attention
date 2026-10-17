import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game/clean-session.html"
PDF = ROOT / "game/standard-paper.pdf"


class CleanSessionTests(unittest.TestCase):
    def test_control_artifact_exists_and_is_a_pdf(self):
        self.assertTrue(PDF.exists())
        self.assertGreater(PDF.stat().st_size, 1000)
        self.assertEqual(PDF.read_bytes()[:5], b"%PDF-")

    def test_question_manifest_freezes_full_stimuli(self):
        manifest = json.loads((ROOT / "game/question-set-v1.json").read_text())
        self.assertEqual(len(manifest["questions"]), 5)
        for question in manifest["questions"]:
            for field in ("id", "dimension", "prompt", "options", "correct_option"):
                self.assertIn(field, question)
            self.assertEqual(len(question["options"]), 4)

    def test_same_questions_and_hidden_arm_contract_are_present(self):
        text = GAME.read_text()
        for marker in ("standard_pdf", "progressive", "BUDGET=180", "source removed", "attention-clean-session-v0.1", "question_ids"):
            self.assertIn(marker, text)
        self.assertIn("standard-paper.pdf", text)
        self.assertIn("progressive-compression reading surface", text)

    def test_clean_session_has_no_network_dependency(self):
        text = GAME.read_text()
        self.assertNotIn("https://", text)
        self.assertIn("question-set-v1.json", text)

    def test_receipt_separates_reading_and_quiz_time(self):
        text = GAME.read_text()
        for marker in ("reading_seconds", "quiz_response_seconds", "U(T_R)/T_R"):
            self.assertIn(marker, text)

    def test_receipt_carries_frozen_provenance(self):
        text = GAME.read_text()
        for marker in ("artifact_versions", "control_pdf_sha256", "question_set_sha256", "protocol_sha256", "progressive_stimulus", "render_latency_ms", "stimulus_ready", "stimulus_load_failure"):
            self.assertIn(marker, text)
    def test_progressive_arm_uses_canonical_stimulus(self):
        text = GAME.read_text()
        self.assertTrue((ROOT / "game/progressive-stimulus-v1.html").exists())
        self.assertIn("progressive-stimulus-v1.html", text)
        self.assertNotIn("Environment → expert compression → discarded residual", text)

    def test_receipt_marks_repeat_exposure(self):
        text = GAME.read_text()
        for marker in ("participant_id", "prior_exposure", "attention_exposure_v1", "progressive_surface_sha256"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()