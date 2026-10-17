#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'pilot-ab'/'site'
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.is_dir(): shutil.rmtree(p)
    else: p.unlink()
for source,target in {
    'ab-index-v1.html':'index.html',
    'static-session-v1.html':'static-session-v1.html',
    'context-session-v1.html':'context-session-v1.html',
    'question-set-v1.json':'question-set-v1.json',
    'progressive-stimulus-v1.html':'progressive-stimulus-v1.html',
    'standard-paper.pdf':'standard-paper.pdf',
}.items():
    data=(ROOT/'game'/source).read_bytes()
    if source.endswith('.html'):
        text=data.decode().replace('</head>','<script>window.ATTENTION_EVENT_ENDPOINT="/api/events";</script></head>',1)
        (OUT/target).write_text(text)
    else: (OUT/target).write_bytes(data)
print(f'built {len(list(OUT.iterdir()))} files at {OUT}')
