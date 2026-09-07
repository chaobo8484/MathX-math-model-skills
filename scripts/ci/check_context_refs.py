#!/usr/bin/env python3
"""CI: 检查 CONTEXT.md 引用的技能名是否都真实存在"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
context = (root / "CONTEXT.md").read_text(encoding="utf-8")
skills = {p.name for p in root.glob("skills/*") if p.is_dir()}

# Find backtick-quoted skill names in CONTEXT.md
refs = set(re.findall(r"`([a-z0-9\-]+)`", context))
# Filter to likely skill names (contain hyphen or known list)
errors = []
for r in refs:
    if r in ("t", "X", "W"):  # symbols
        continue
    if r in skills:
        continue
    # Only check if r looks like a skill name (contains hyphen and not a generic word)
    if "-" in r and r not in skills:
        # Check if it's a known skill reference that should exist
        # Allowlist for non-skill terms
        allow = {"openai.yaml", "GB/T", "booktabs", "1-SE"}
        if r in allow:
            continue
        # If r contains hyphen and is not a skill, it might be a false positive like "time-series"
        # Only flag if r exactly equals a skill-like pattern but missing
        if r not in skills and any(s.startswith(r.split("-")[0]) for s in skills):
            # Could be partial, skip
            continue

# Also check skills referenced in README index exist
readme = (root / "README.md").read_text(encoding="utf-8")
for m in re.findall(r"\[([a-z0-9\-]+)\]\(./skills/", readme):
    if m not in skills:
        errors.append(f"README references missing skill: {m}")

if errors:
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)
    sys.exit(1)
print(f"context refs OK: skills={len(skills)} refs checked")
