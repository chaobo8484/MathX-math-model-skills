# Progressive Disclosure 分层引用规范

> 对应诊断报告 P1-4：所有内容堆在一个 SKILL.md 里会稀释注意力，且浪费 context。参考 `mattpocock/skills` 的 `references/*.md` 与 `patent-disclosure` 的 `references/*.schema.yaml` 做法。

## 阈值

- 单个 `SKILL.md` 超过 **150 行**，或包含 **大表格/阈值表/LaTeX 模板** 且正文已超 100 行时，触发拆分审查。
- 当前审计（2026-09-06）：34 个技能最大 122 行（`ahp`），**无超阈**，故本轮不强制拆分，仅建立规范与示范。

## 目录约定

```
skills/<name>/
  SKILL.md                # 仅留 Operating Posture / Hard Rules / Build Sequence 步骤 + 指针
  assets/
    references/
      <topic>.md          # 大表格、阈值表、模板原文
      <topic>.schema.yaml # 若有结构化 schema
    scripts/
      <name>_gate.py      # 门禁脚本（P0-2）
```

## 写法

SKILL.md 中用指针替代正文堆砌：

```markdown
> 详表见 `assets/references/saaty-scale.md`，阈值见 `assets/references/ri-table.md`。
```

而非把整张表贴进 SKILL.md。Agent 按需再读 reference 文件，主流程保持精简。

## 示范

- `skills/ahp/assets/references/` 已建两份示范：`saaty-scale.md`（1–9 标度）与 `ri-table.md`（Saaty RI 表），供后续技能参照。
- 后续新增阈值表（如 `genetic-algorithm` 的参数表、`differential-equation` 的离散格式表）沿用此模式。

## 验收

- CI 将校验：`SKILL.md` 超 150 行且未在 `assets/references/` 留指针的 PR 需附理由。
