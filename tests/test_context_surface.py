import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACE = ROOT / 'game/context-surface-v1.html'


class ContextSurfaceTests(unittest.TestCase):
    def test_context_surface_has_pre_reading_demo_and_start_gate(self):
        text = SURFACE.read_text()
        for marker in ('10-second interaction demo', 'id="demo"', 'id="start" disabled', 'demoCompleted'):
            self.assertIn(marker, text)

    def test_selection_resolution_and_context_cache_are_present(self):
        text = SURFACE.read_text()
        for marker in ('selectionInfo', 'modeFor', 'context_id', 'attention_context_cache_v1', 'context_request', 'context_demo', 'Go deeper'):
            self.assertIn(marker, text)

    def test_context_surface_loads_canonical_stimulus(self):
        text = SURFACE.read_text()
        self.assertIn("fetch('progressive-stimulus-v1.html')", text)
        self.assertNotIn('Environment → expert compression → discarded residual', text)

    def test_context_requests_record_span_resolution_without_raw_network_dependency(self):
        text = SURFACE.read_text()
        for marker in ('selected_text', 'selection_words', 'opened_at', 'cached', 'localStorage'):
            self.assertIn(marker, text)
        self.assertNotIn('https://', text)


if __name__ == '__main__':
    unittest.main()
