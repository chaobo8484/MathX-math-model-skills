#!/usr/bin/env python3
"""CI: 检查每个 SKILL.md 是否有合法 frontmatter（name/description）"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
skills = sorted(root.glob("skills/*/SKILL.md"))
errors = []
for p in skills:
    text = p.read_text(encoding="utf-8").lstrip("\ufeff")
    if not text.startswith("---"):
        errors.append(f"{p}: missing frontmatter ---")
        continue
    fm = text.split("---", 2)[1] if text.count("---") >= 2 else ""
    if "name:" not in fm:
        errors.append(f"{p}: frontmatter missing name")
    if "description:" not in fm:
        errors.append(f"{p}: frontmatter missing description")
    # name should match directory
    m = re.search(r"name:\s*(\S+)", fm)
    if m and m.group(1) != p.parent.name:
        errors.append(f"{p}: name {m.group(1)} != dir {p.parent.name}")
    # description should be Chinese + English keywords, not contain Use when
    if "Use when" in fm or "Trigger phrases" in fm:
        errors.append(f"{p}: description contains English residue Use when/Trigger phrases")

if errors:
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)
    sys.exit(1)
print(f"frontmatter OK: {len(skills)} skills")
