#!/usr/bin/env python3
"""CI: compile every gate/tool script in the repo.

Covers skills/*/assets/scripts/*.py and scripts/ci/*.py.
Fails on first syntax error with file + line.
"""
import pathlib
import py_compile
import sys

root = pathlib.Path(__file__).resolve().parents[2]
targets = sorted(root.glob("skills/*/assets/scripts/*.py")) + sorted((root / "scripts" / "ci").glob("*.py"))

if not targets:
    print("FAIL: no scripts found", file=sys.stderr)
    sys.exit(1)

failed = 0
for p in targets:
    try:
        py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"FAIL: {p.relative_to(root)}: {e}", file=sys.stderr)
        failed += 1

if failed:
    sys.exit(1)
print(f"compile OK: {len(targets)} scripts")
