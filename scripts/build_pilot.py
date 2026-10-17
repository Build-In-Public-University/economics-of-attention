#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'pilot' / 'site'
GAME = ROOT / 'game'
OUT.mkdir(parents=True, exist_ok=True)
for child in OUT.iterdir():
    if child.is_file() or child.is_symlink(): child.unlink()
    elif child.is_dir(): shutil.rmtree(child)

files = {
    'clean-session.html': 'index.html',
    'attention-game.html': 'standalone.html',
    'question-set-v1.json': 'question-set-v1.json',
    'clean-session-protocol-v1.json': 'clean-session-protocol-v1.json',
    'progressive-stimulus-v1.html': 'progressive-stimulus-v1.html',
    'standard-paper.pdf': 'standard-paper.pdf',
}
for source, target in files.items():
    text_or_bytes = (GAME / source).read_bytes()
    if source.endswith('.html'):
        text = text_or_bytes.decode()
        injection = '<script>window.ATTENTION_EVENT_ENDPOINT="/api/events";</script>'
        text = text.replace('</head>', injection + '</head>', 1)
        (OUT / target).write_text(text)
    else:
        (OUT / target).write_bytes(text_or_bytes)
print(f'built {len(files)} public files at {OUT}')
