"""Check that relative Markdown links in README.md / CHANGELOG.md resolve."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
broken = []
for name in ('README.md', 'CHANGELOG.md', 'windows/README.md'):
    path = root / name
    if not path.exists():
        broken.append(f'{name}: missing file')
        continue
    text = path.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if target.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        rel = target.split('#', 1)[0]
        if not rel:
            continue
        if not (path.parent / rel).exists():
            broken.append(f'{name}: {target}')
if broken:
    print('Broken links:')
    print('\n'.join(broken))
    raise SystemExit(1)
print('All relative links OK')
