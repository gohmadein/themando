"""Download all split parts first, then run: py -3 restore.py"""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
entries = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))['files']
for entry in entries:
    parts = entry['assets']
    if len(parts) < 2:
        continue
    paths = [root / item['name'] for item in parts]
    if not all(p.is_file() for p in paths):
        print('Missing parts:', entry['path'])
        continue
    output = root / Path(entry['path']).name
    digest = hashlib.sha256()
    with output.open('xb') as dest:
        for path in paths:
            with path.open('rb') as source:
                for block in iter(lambda: source.read(8 * 1024**2), b''):
                    dest.write(block)
                    digest.update(block)
    if digest.hexdigest() != entry['sha256']:
        raise RuntimeError('Checksum mismatch: ' + str(output))
    print('Restored and verified:', output.name)
