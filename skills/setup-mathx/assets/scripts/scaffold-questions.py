#!/usr/bin/env python3
"""
scaffold-questions.py — 按问脚手架（setup-mathx 步骤 0，接 intake-organize.py）

intake-organize.py 把工作区按题目分好文件夹后，本脚本在每个题目文件夹下
按问建目录。约定（全项目统一，下游技能只认这里）：

  <A题>/q1/charts_q1/       该问图表输出
  <A题>/q1/data_q1/         该问原始数据（附件中分出的部分，raw）
  <A题>/q1/script_q1/       该问脚本（清洗/分析代码）
  <A题>/q1/cleaned_data/    该问清洗后数据（ingest-inputs 输出，processed）
  <A题>/q2/ ...             同上
  <A题>/main.py             总入口浓缩索引（论文附录提交版，不直接运行；
                           已存在永不覆盖，函数名 TODO 由 Agent 填实）

规则：
- 问数优先从原题 PDF 文本探测（问题一/二/三、第X问、Q1/Q2…）；探不到则 HOLD
  问用户，--questions 可直接指定（覆盖探测）。
- 只建目录不搬文件；已存在的非空目录复用并警告，不覆盖不删除。
- 默认 dry-run 只出方案（verdict OPEN）；确认后 --apply 执行。

Usage:
  python scaffold-questions.py --problem-dir <A题目录> --out report.json
  python scaffold-questions.py --problem-dir <A题目录> --out report.json --questions 4 --apply
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9}
QUESTION_RES = (
    re.compile(r"问题\s*([一二三四五六七八九])"),
    re.compile(r"第\s*([一二三四五六七八九\d])\s*问"),
    re.compile(r"问题\s*(\d)"),
    re.compile(r"\bQ\s*([1-9])\b", re.IGNORECASE),
)
SUBDIRS = ("charts_q{i}", "data_q{i}", "script_q{i}", "cleaned_data")
MAIN_PY = "main.py"

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


def build_main_py(problem: str, n: int) -> str:
    """按模板生成 main.py（各问浓缩索引，函数名留 TODO 由 Agent 填实）。"""
    blocks, calls = [], []
    for i in range(1, n + 1):
        blocks.append(
            f"# ---------------- Q{i}：TODO（一句话说明本问做什么） ----------------\n"
            f"# 核心脚本：q{i}/script_q{i}/TODO_脚本名.py\n"
            f"# 输入：q{i}/data_q{i}/TODO → 清洗：q{i}/cleaned_data/TODO → "
            f"图表：q{i}/charts_q{i}/TODO\n"
            f"# from script_q{i}.TODO_模块名 import main as q{i}_main  # TODO：填实\n")
        calls.append(f"    # q{i}_main()  # TODO：填实后取消注释")
    template = pathlib.Path(__file__).resolve().parent.parent / "templates" / "main.py"
    text = template.read_text(encoding="utf-8")
    return (text.replace("@PROBLEM@", problem).replace("@N@", str(n))
                .replace("@BLOCKS@", "\n".join(blocks)).replace("@CALLS@", "\n".join(calls)))


def detect_questions(problem_dir: pathlib.Path) -> tuple[int | None, list[str]]:
    """从题目文件夹内 PDF 文本探测问数；探不到返回 None。"""
    evidence: list[str] = [f"pypdf 可用: {HAS_PYPDF}"]
    if not HAS_PYPDF:
        return None, evidence + ["无 pypdf，问数请 --questions 指定"]
    pdfs = sorted(problem_dir.glob("*.pdf"))
    if not pdfs:
        return None, evidence + ["题目文件夹内无 PDF，问数请 --questions 指定"]
    found: set[int] = set()
    for pdf in pdfs:
        try:
            reader = PdfReader(str(pdf))
        except Exception as e:
            evidence.append(f"{pdf.name} 解析失败: {e}")
            continue
        text = ""
        for page in reader.pages[:4]:
            try:
                text += page.extract_text() or ""
            except Exception:
                pass
        for rx in QUESTION_RES:
            for m in rx.findall(text):
                found.add(CN_NUM[m] if m in CN_NUM else int(m))
        evidence.append(f"{pdf.name} 文本探测到问号: {sorted(found) or '无'}")
    if not found:
        return None, evidence
    return max(found), evidence


def main():
    parser = argparse.ArgumentParser(description="按问脚手架")
    parser.add_argument("--problem-dir", type=pathlib.Path, required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--questions", type=int, default=0,
                        help="问数（覆盖自动探测）")
    parser.add_argument("--apply", action="store_true", help="建目录（默认只出方案）")
    args = parser.parse_args()

    problem_dir = args.problem_dir
    if not problem_dir.is_dir():
        print(f"题目文件夹不存在: {problem_dir}", file=sys.stderr); sys.exit(1)

    if args.questions:
        n, evidence = args.questions, [f"问数由 --questions 指定: {args.questions}"]
    else:
        n, evidence = detect_questions(problem_dir)

    need_user: list[str] = []
    warnings: list[str] = []
    plan: list[str] = []
    reused: list[str] = []
    if not n or n < 1 or n > 9:
        need_user.append("问数探测不到：请确认本题有几问后 --questions <N> 重跑")
        verdict = f"HOLD — {need_user[0]}"
    else:
        for i in range(1, n + 1):
            for sub in SUBDIRS:
                d = problem_dir / f"q{i}" / sub.format(i=i)
                rel = d.relative_to(problem_dir).as_posix()
                if d.exists():
                    reused.append(rel)
                    if d.is_dir() and any(d.iterdir()):
                        warnings.append(f"复用非空目录：{rel}")
                else:
                    plan.append(rel)
        main_py = problem_dir / MAIN_PY
        if main_py.exists():
            reused.append(MAIN_PY)
            warnings.append("main.py 已存在，不覆盖（附录版以人工填实为准）")
        else:
            plan.append(MAIN_PY)
        if args.apply:
            for rel in plan:
                if rel == MAIN_PY:
                    (problem_dir / MAIN_PY).write_text(
                        build_main_py(problem_dir.name, n), encoding="utf-8")
                else:
                    (problem_dir / rel).mkdir(parents=True, exist_ok=True)
            verdict = f"PASS — q1..q{n} 脚手架就绪（新建 {len(plan)}，复用 {len(reused)}，含 main.py）"
        else:
            verdict = f"OPEN — q1..q{n} 方案就绪（新建 {len(plan)}，复用 {len(reused)}，含 main.py），确认后 --apply 执行"

    report = {"problem_dir": str(problem_dir), "questions": n or 0,
              "evidence": evidence, "plan": plan, "reused": reused, "warnings": warnings,
              "need_user": need_user, "applied": bool(args.apply), "verdict": verdict}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"scaffold: questions={n or '?'} new={len(plan)} reused={len(reused)} [{verdict}]")
    print(f"报告: {args.out}")


if __name__ == "__main__":
    main()
