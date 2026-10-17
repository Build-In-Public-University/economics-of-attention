import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PilotArtifactTests(unittest.TestCase):
    def test_pilot_contract_and_public_files_exist(self):
        for path in (
            ROOT / 'docs/PILOT-PREREGISTRATION.md',
            ROOT / 'pilot/schema.sql',
            ROOT / 'pilot/functions/api/events.js',
            ROOT / 'pilot/wrangler.toml',
            ROOT / 'scripts/build_pilot.py',
        ):
            self.assertTrue(path.exists(), path)

    def test_event_endpoint_is_bounded_and_does_not_accept_identity_fields(self):
        text = (ROOT / 'pilot/functions/api/events.js').read_text()
        for marker in ('MAX_JSON_BYTES', 'ALLOWED_EVENTS', 'event_id', 'participant_id', 'score'):
            self.assertIn(marker, text)
        for forbidden in ('email', 'ip_address', 'raw_answers'):
            self.assertNotIn(forbidden, text)

    def test_game_surfaces_emit_funnel_events(self):
        for name in ('attention-game.html', 'clean-session.html'):
            text = (ROOT / 'game' / name).read_text()
            for marker in ('ATTENTION_EVENT_ENDPOINT', 'play_start', 'stimulus_ready', 'result'):
                self.assertIn(marker, text)

    def test_generated_pilot_surface_has_endpoint_injection(self):
        for name in ('index.html', 'standalone.html'):
            text = (ROOT / 'pilot/site' / name).read_text()
            self.assertIn('window.ATTENTION_EVENT_ENDPOINT="/api/events"', text)


if __name__ == '__main__':
    unittest.main()
