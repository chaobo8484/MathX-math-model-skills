# mathx-config 示例（由 setup-mathx 写入 docs/agents/mathx-config.md）

> 本文件为示例，实际配置由 `setup-mathx` 按“四问”写入 `docs/agents/mathx-config.md`，其余技能有就读。`evidence_key_source` 只记来源，永不记值。

```yaml
# 四问落盘
data_dir: ./data
template_version: 国赛2026
latex_compiler: XeLaTeX
output_format: TEX
plot_backend: matplotlib
venue: 国赛
evidence_backend: none
evidence_key_source: env:FIRECRAWL_API_KEY
```

技能读取约定：`if docs/agents/mathx-config.md exists then read it`（`CONTEXT.md:37`）。
