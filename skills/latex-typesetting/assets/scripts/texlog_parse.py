#!/usr/bin/env python3
"""
texlog_parse.py — TEX 构建日志 triage（P1）

对应 latex-typesetting/SKILL.md Build Sequence 3：
自上而下提取首错 + 计数分类（错误/未定义引用/overfull/字体替换），
输出修哪个先修哪个的顺序表。修错仍靠人，找错机器包。

Usage:
  python texlog_parse.py main.log --out report.json
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

def main():
    parser = argparse.ArgumentParser(description="TEX 日志 triage")
    parser.add_argument("log", type=pathlib.Path, help="LaTeX 构建日志")
    parser.add_argument("--out", type=pathlib.Path, required=True)
    args = parser.parse_args()

    if not args.log.exists():
        print(f"日志不存在: {args.log}", file=sys.stderr); sys.exit(1)
    text = args.log.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    errors = [l.strip()[:160] for l in lines if l.startswith("! ")]
    undefined = sorted(set(re.findall(r"Citation `([^']+)' undefined", text)))
    undef_refs = "There were undefined references" in text
    overfulls = [(i + 1, l.strip()[:120]) for i, l in enumerate(lines) if "Overfull" in l]
    big_overfull = [o for o in overfulls if (m := re.search(r"(\d+(?:\.\d+)?)pt too wide", o[1])) and float(m.group(1)) > 5]
    font_subs = sorted(set(re.findall(r"Font shape `([^']+)' .*instead", text)))
    rerun = "Rerun to get" in text

    gates = {
        "zero_errors": len(errors) == 0,
        "n_errors": len(errors),
        "first_error": errors[0] if errors else "",
        "undefined_zero": len(undefined) == 0 and not undef_refs,
        "undefined": undefined,
        "overfull_total": len(overfulls),
        "overfull_gt_5pt": [(ln, s) for ln, s in big_overfull],
        "font_substitutions": font_subs,
        "needs_rerun": rerun,
    }
    if errors:
        verdict = f"HOLD — 先修首错：{errors[0][:80]}"
    elif undefined or undef_refs:
        verdict = "HOLD — 未定义引用归零后重编"
    elif big_overfull:
        verdict = f"HOLD — {len(big_overfull)} 处 overfull>5pt 待修"
    elif rerun:
        verdict = "OPEN — 重跑一遍（bib/引用需多遍）后重验"
    else:
        verdict = "PASS — 零错误；剩余警告逐个认领（字体替换等）"

    report = {"log": str(args.log), "gates": gates, "verdict": verdict}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"log: errors={len(errors)} undefined={len(undefined)} overfull={len(overfulls)} (>5pt {len(big_overfull)}) [{verdict}]")
    print(f"报告: {args.out}")

if __name__ == "__main__":
    main()
