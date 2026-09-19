#!/usr/bin/env python3
"""
intake-organize.py — 开工工作区整编（setup-mathx 步骤 0）

用户拿到赛题时的典型工作区：散放的原题 PDF（约两页，说明全部题目，
可能是 A–E 全套）+ 附件（XLSX/CSV 等，或装在 附件/ 目录里）。本脚本按题目
分文件夹归位：

  <workdir>/A题/A题.pdf + 附件A/ + src/ + figs/
  <workdir>/B题/B题.pdf + 附件B/ + src/ + figs/
  ...

题下按问细分（q1/charts_q1/data_q1/script_q1/cleaned_data）由
scaffold-questions.py 接手，本脚本只管题目级归位。

规则：
- 只动顶层散件；已存在的题目文件夹、docs/、.git 等一律不动。
- 默认 dry-run 只出方案（verdict OPEN）；确认无误后 --apply 执行。
- 附件名带字号（附件A/A题附件/A_data）自动归位该题；多题共用一个无字号
  附件包、或题数不明时 HOLD，把问题写进报告的 need_user，由 Agent 问用户
  后再定（--problems 指定题号可解一部分）。
- 多题共用的总题 PDF 留根目录不动，不挡其他归位。
- 下游（ingest-inputs 吃附件、latex-typesetting 出稿）只认整编后的位置。

Usage:
  python intake-organize.py --workdir <dir> --out report.json
  python intake-organize.py --workdir <dir> --out report.json --apply
  python intake-organize.py --workdir <dir> --out report.json --problems A,B --apply
"""
from __future__ import annotations
import argparse, json, pathlib, re, shutil, sys

PROBLEM_DIR_RE = re.compile(r"^([A-E])\s*题$")
PDF_LETTER_RES = (
    re.compile(r"([A-E])\s*题"),
    re.compile(r"problem[\s_\-]*([A-E])", re.IGNORECASE),
    re.compile(r"^([A-E])[\s_\-]"),
)
ATTACH_DIR_RE = re.compile(r"^(附件|attach|data)", re.IGNORECASE)
ATTACH_LETTER_RES = (
    re.compile(r"附件\s*([A-E])"),
    re.compile(r"([A-E])\s*题?\s*附件"),
    re.compile(r"^([A-E])[\s_\-]"),
    re.compile(r"attach[\s_\-]*([A-E])", re.IGNORECASE),
    re.compile(r"([A-E])\s*题"),
)
ATTACH_EXTS = {".xlsx", ".xls", ".csv", ".txt", ".dat", ".mat",
               ".sav", ".dta", ".json", ".db"}
TEXT_LETTER_RE = re.compile(r"([A-E])\s*题")
TEXT_COUNT_RE = re.compile(r"共\s*(\d+)\s*道")
PROTECTED = {"docs", ".git", ".github", ".claude-plugin", "skills",
             "scripts", "assets", "__pycache__"}

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


def pdf_letters(pdf: pathlib.Path) -> tuple[set[str], list[str]]:
    """从题 PDF 前两页文本取题号证据；无 pypdf 或无文本层时返回空集。"""
    if not HAS_PYPDF:
        return set(), ["无 pypdf，跳过 PDF 文本取证"]
    try:
        reader = PdfReader(str(pdf))
    except Exception as e:
        return set(), [f"PDF 解析失败 {pdf.name}: {e}"]
    text = ""
    for page in reader.pages[:2]:
        try:
            text += page.extract_text() or ""
        except Exception:
            pass
    if not text.strip():
        return set(), [f"{pdf.name} 无文本层（疑似扫描件），题数走文件名"]
    letters = set(TEXT_LETTER_RE.findall(text))
    notes = [f"{pdf.name} 文本提及题号: {sorted(letters) or '无'}"]
    m = TEXT_COUNT_RE.search(text)
    if m:
        notes.append(f"{pdf.name} 声明共 {m.group(1)} 道")
    return letters, notes


def main():
    parser = argparse.ArgumentParser(description="开工工作区整编")
    parser.add_argument("--workdir", type=pathlib.Path, required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--apply", action="store_true", help="执行搬移（默认只出方案）")
    parser.add_argument("--problems", type=str, default="",
                        help="强制题号逗号分隔，如 A,B（文件名/PDF 取证不明时用）")
    args = parser.parse_args()

    workdir = args.workdir
    if not workdir.is_dir():
        print(f"工作区不存在: {workdir}", file=sys.stderr); sys.exit(1)
    entries = sorted(workdir.iterdir(), key=lambda p: p.name)
    evidence: list[str] = [f"pypdf 可用: {HAS_PYPDF}"]

    # 1. 已整编题目文件夹
    problem_dirs = {p.name: p for p in entries
                    if p.is_dir() and PROBLEM_DIR_RE.match(p.name)}
    # 2. 散放原题 PDF（顶层 .pdf）
    loose_pdfs = [p for p in entries
                  if p.is_file() and p.suffix.lower() == ".pdf"]
    pdf_letter: dict[str, list[pathlib.Path]] = {}
    unlettered_pdfs: list[pathlib.Path] = []
    for pdf in loose_pdfs:
        letters = {m for rx in PDF_LETTER_RES for m in rx.findall(pdf.stem)}
        if len(letters) == 1:
            pdf_letter.setdefault(next(iter(letters)), []).append(pdf)
        else:
            unlettered_pdfs.append(pdf)
            tl, notes = pdf_letters(pdf)
            evidence.extend(notes)
    # 3. 附件包（顶层附件目录 + 散放数据文件）
    attach_dirs = [p for p in entries
                   if p.is_dir() and ATTACH_DIR_RE.match(p.name)
                   and p.name not in PROTECTED]
    loose_data = [p for p in entries
                  if p.is_file() and p.suffix.lower() in ATTACH_EXTS]

    forced = [s.strip().upper() for s in args.problems.split(",") if s.strip()]
    if forced and (bad := [s for s in forced if not re.fullmatch(r"[A-E]", s)]):
        print(f"--problems 非法题号: {bad}", file=sys.stderr); sys.exit(1)

    def attach_letter(name: str) -> str | None:
        """附件名取字号（附件A/A题附件/A_data/attachA）；多义或无字号返回 None。"""
        hits = {m.group(1).upper() for rx in ATTACH_LETTER_RES for m in rx.finditer(name)}
        return next(iter(hits)) if len(hits) == 1 else None

    attach_mapped: dict[str, list[pathlib.Path]] = {}
    attach_shared: list[pathlib.Path] = []
    for a in attach_dirs + loose_data:
        L = attach_letter(a.name)
        if L:
            attach_mapped.setdefault(L, []).append(a)
            evidence.append(f"{a.name} 字号归属 {L}题")
        else:
            attach_shared.append(a)

    letters = sorted(set(pdf_letter) | set(forced) | set(attach_mapped))
    moves: list[dict] = []
    need_user: list[str] = []
    warnings: list[str] = []
    kept_at_root: list[str] = []

    if len(letters) == 1:
        # 单题工作区：无字号散件默认归属该题（--problems 是最常见的确认方式）
        for pdf in unlettered_pdfs:
            pdf_letter.setdefault(letters[0], []).append(pdf)
            evidence.append(f"{pdf.name} 无字号，单题归属 {letters[0]}题")
        unlettered_pdfs = []

    if problem_dirs and not loose_pdfs and not attach_dirs and not loose_data:
        verdict = "PASS — 已按题目分文件夹，无散件可整"
    elif not letters and not unlettered_pdfs:
        need_user.append("顶层无原题 PDF，也无 --problems 指定：请给出赛题文件位置或题号")
        verdict = "HOLD — 无题目输入"
    else:
        if unlettered_pdfs and not letters:
            names = [p.name for p in unlettered_pdfs]
            if len(names) == 1:
                # 只有一份无字号题 PDF：问用户是哪道
                need_user.append(f"仅一份题 PDF（{names[0]}），文件名无题号：请确认题号后 --problems <题号> 重跑")
            else:
                need_user.append(f"多份 PDF 文件名无题号：{names}（用 --problems 指定题号后重跑）")
        elif unlettered_pdfs:
            # 多题共用的总题 PDF：留根目录，不挡归位
            for pdf in unlettered_pdfs:
                kept_at_root.append(pdf.name)
            warnings.append(f"总题 PDF 留根目录未动：{[p.name for p in unlettered_pdfs]}（多题共用，归位后按需取用）")
        # 附件归属：有字号直连；无字号单题直连；无字号多题 HOLD 问用户
        attach_plan: dict[str, list[pathlib.Path]] = {L: list(attach_mapped.get(L, [])) for L in letters}
        if attach_shared:
            if len(letters) == 1:
                attach_plan[letters[0]].extend(attach_shared)
            elif letters:
                names = [p.name for p in attach_shared]
                need_user.append(f"多题 {letters} 共用附件 {names}：请逐项指定归属题号（或声明共用只做一题）")
        for L in letters:
            dest = workdir / f"{L}题"
            if dest.exists():
                if dest.is_dir() and not any(dest.iterdir()):
                    warnings.append(f"{dest.name}/ 已存在空目录，复用")
                elif not problem_dirs.get(dest.name):
                    need_user.append(f"{dest.name}/ 已存在且非空：请确认复用或改名后再跑")
                    continue
            for pdf in pdf_letter.get(L, []):
                moves.append({"src": pdf.name, "dst": f"{L}题/{pdf.name}", "kind": "原题PDF"})
            for a in attach_plan.get(L, []):
                moves.append({"src": a.name, "dst": f"{L}题/{a.name}", "kind": "附件"})
        if need_user:
            verdict = f"HOLD — {need_user[0]}"
        elif not moves:
            verdict = "PASS — 无需搬移"
        elif args.apply:
            for m in moves:
                src, dst = workdir / m["src"], workdir / m["dst"]
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    need_user.append(f"目标已存在跳过：{m['dst']}")
                    continue
                shutil.move(str(src), str(dst))
            verdict = "PASS — 已按题目分文件夹归位（按问细分调 scaffold-questions.py）" if not need_user else "HOLD — 部分目标已存在"
        else:
            verdict = f"OPEN — 方案就绪（{len(moves)} 项搬移），确认后 --apply 执行"

    report = {"workdir": str(workdir),
              "state": {"problem_dirs": sorted(problem_dirs), "letters": letters,
                        "loose_pdfs": [p.name for p in loose_pdfs],
                        "attach_dirs": [p.name for p in attach_dirs],
                        "loose_data": [p.name for p in loose_data],
                        "kept_at_root": kept_at_root},
              "evidence": evidence, "moves": moves, "warnings": warnings,
              "need_user": need_user, "applied": bool(args.apply), "verdict": verdict}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"intake: letters={letters} moves={len(moves)} [{verdict}]")
    print(f"报告: {args.out}")


if __name__ == "__main__":
    main()
