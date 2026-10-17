import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game/attention-game.html"


class AttentionGameArtifactTests(unittest.TestCase):
    def test_game_is_self_contained_and_local_only(self):
        text = GAME.read_text()
        self.assertIn("No external network calls", text)
        self.assertIn("crypto.randomUUID", text)
        self.assertNotIn("https://", text)
        self.assertIn("question-set-v1.json", text)

    def test_game_enforces_bounded_reading_then_quiz(self):
        text = GAME.read_text()
        for marker in ("data-seconds=\"30\"", "data-seconds=\"180\"", "data-seconds=\"900\"", "endReading", "the paper vanishes", "Download receipt"):
            self.assertIn(marker, text)

    def test_questions_cover_consequential_model_not_trivia(self):
        text = GAME.read_text()
        for marker in ("question-set-v1.json", "U(T_R)/T_R"):
            self.assertIn(marker, text)

    def test_receipt_separates_reading_and_quiz_time(self):
        text = GAME.read_text()
        for marker in ("declared_budget_seconds", "actual_reading_seconds", "quiz_response_seconds", "U(T_R)/T_R"):
            self.assertIn(marker, text)

    def test_receipt_carries_frozen_provenance(self):
        text = GAME.read_text()
        for marker in ("artifact_versions", "control_pdf_sha256", "question_set_sha256", "protocol_sha256"):
            self.assertIn(marker, text)
    def test_receipt_marks_repeat_exposure(self):
        text = GAME.read_text()
        for marker in ("participant_id", "prior_exposure", "attention_game_seen"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()