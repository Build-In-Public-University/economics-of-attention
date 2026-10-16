import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game/attention-game.html"


class AttentionGameArtifactTests(unittest.TestCase):
    def test_game_is_self_contained_and_local_only(self):
        text = GAME.read_text()
        self.assertIn("No network calls", text)
        self.assertIn("crypto.randomUUID", text)
        self.assertNotIn("fetch(", text)
        self.assertNotIn("https://", text)

    def test_game_enforces_bounded_reading_then_quiz(self):
        text = GAME.read_text()
        for marker in ("data-seconds=\"30\"", "data-seconds=\"180\"", "data-seconds=\"900\"", "endReading", "the paper vanishes", "Download receipt"):
            self.assertIn(marker, text)

    def test_questions_cover_consequential_model_not_trivia(self):
        text = GAME.read_text()
        for marker in ("Thesis", "Mechanism", "Economic constraint", "Evidence boundary", "Transfer", "U(T)/T"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()