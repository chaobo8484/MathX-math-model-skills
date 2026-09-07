#!/usr/bin/env python3
"""CI: versioned_write.py 三拷贝同步校验。

paper-outline / latex-typesetting / polish-proofread 各持一份（技能须自包含
以便 marketplace 分发）。内容必须完全一致，改一处必须同步另两处。
"""
import hashlib
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[2]
copies = [
    root / "skills" / "paper-outline" / "assets" / "scripts" / "versioned_write.py",
    root / "skills" / "latex-typesetting" / "assets" / "scripts" / "versioned_write.py",
    root / "skills" / "polish-proofread" / "assets" / "scripts" / "versioned_write.py",
]

missing = [str(p) for p in copies if not p.exists()]
if missing:
    for m in missing:
        print(f"FAIL: missing {m}", file=sys.stderr)
    sys.exit(1)

hashes = {p: hashlib.md5(p.read_bytes()).hexdigest() for p in copies}
if len(set(hashes.values())) != 1:
    for p, h in hashes.items():
        print(f"FAIL: drift {p.relative_to(root)} md5={h}", file=sys.stderr)
    sys.exit(1)
print(f"versioned sync OK: 3 copies md5={next(iter(hashes.values()))[:8]}")
