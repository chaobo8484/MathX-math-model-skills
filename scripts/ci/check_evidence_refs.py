#!/usr/bin/env python3
"""CI: research-evidence 接线校验。

1. skills/research-evidence/SKILL.md 存在且 frontmatter 合法。
2. 除 research-evidence 外，无技能直调 firecrawl_* 脚本或提及 FIRECRAWL_API_KEY。
3. CONTEXT.md 提及 research-evidence（工具默认已接线）。
4. setup-mathx 含 evidence_backend（四问已落盘）。
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[2]
errors: list[str] = []

# 1. skill exists + frontmatter
sk = root / "skills" / "research-evidence" / "SKILL.md"
if not sk.exists():
    errors.append("skills/research-evidence/SKILL.md missing")
else:
    text = sk.read_text(encoding="utf-8").lstrip("\ufeff")
    if not text.startswith("---"):
        errors.append("research-evidence: missing frontmatter")
    else:
        fm = text.split("---", 2)[1] if text.count("---") >= 2 else ""
        if "name:" not in fm or "description:" not in fm:
            errors.append("research-evidence: frontmatter missing name/description")

# 2. no direct firecrawl use outside research-evidence
for p in sorted(root.glob("skills/*/SKILL.md")):
    if p.parent.name == "research-evidence":
        continue
    t = p.read_text(encoding="utf-8")
    # Allowed: backend choice names (setup-mathx Q4) and key-source references
    # of the form env:FIRECRAWL_API_KEY (name only). Block script calls and
    # real key handling.
    t_scrubbed = t.replace("env:FIRECRAWL_API_KEY", "")
    if "firecrawl_" in t_scrubbed or "FIRECRAWL_API_KEY" in t_scrubbed:
        errors.append(f"{p.parent.name}: must not call firecrawl directly; route via research-evidence")
for p in sorted(root.glob("skills/*/assets/scripts/*.py")):
    if "research-evidence" in p.parts:
        continue
    t = p.read_text(encoding="utf-8")
    if "FIRECRAWL_API_KEY" in t or "firecrawl" in t.lower():
        errors.append(f"{p}: must not touch firecrawl outside research-evidence")

# 3. CONTEXT wiring
ctx = (root / "CONTEXT.md").read_text(encoding="utf-8")
if "research-evidence" not in ctx:
    errors.append("CONTEXT.md: missing research-evidence backend line")

# 4. setup-mathx Q4
setup = (root / "skills" / "setup-mathx" / "SKILL.md").read_text(encoding="utf-8")
if "evidence_backend" not in setup:
    errors.append("setup-mathx: missing evidence_backend (Q4)")

if errors:
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)
    sys.exit(1)
print("evidence refs OK: research-evidence wired, no direct firecrawl use")
