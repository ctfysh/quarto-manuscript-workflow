# 场景：审稿修改 — 从审稿意见到修订稿

**研究者：** *"我收到 Water Research 的小修意见。审稿人有三个修改要求。能帮我修改稿件并重新渲染吗？"*

研究者提供：
- 已有的 `index.qmd`、`_quarto.yml` 和项目文件
- 审稿意见

---

## 第 1 步：阅读审稿意见

Agent 阅读每一条意见并映射为具体操作：

| # | 意见 | 操作 |
|---|------|------|
| 1 | "图 2 分辨率太低，达不到出版要求（需 ≥300 DPI）" | 替换 `fig2-concentrations.png` 为高分辨率版 |
| 2 | "讨论部分应说明样本量的局限性（仅 6 座水厂）" | 在讨论中增加一段关于局限性的内容 |
| 3 | "请确认所有引用键都与参考文献列表匹配——我发现正文中有 [@smith2020] 但 references.bib 中没有" | 添加 Smith 2020 的文献条目 |

---

## 第 2 步：应用修改

Agent 编辑 `index.qmd`：

```diff
 ## 讨论 {#sec-discussion}
 
 常规处理工艺（72.3%）的去除效率与现有文献基本一致...
 
+### 研究局限性
+
+需要指出的是，本研究仅基于 6 座水厂的样本，可能无法涵盖所有处理工艺配置和原水条件。
+未来在更广泛地理区域、更大样本量的研究将有助于增强这些发现的普适性。
+此外，本次采样仅在夏季进行，未评估季节性变化——全年监测将更全面地反映微塑料去除动态。
+
 ## 结论 {#sec-conclusion}
```

Agent 同时：
- 用研究者提供的高分辨率版本替换 `figures/fig2-concentrations.png`
- 通过 CrossRef 自动查找 DOI 并将 `[@smith2020]` 添加到 `references.bib`

---

## 第 3 步：起飞前检查

- [x] `.gitignore` 已包含 `_manuscript/`、`_freeze/`、`_supplementary/`
- [x] `freeze: false`（编辑阶段——定稿前设为 `true`）
- [x] `lang: en` 与期刊一致
- [x] CSL 和 reference-doc 来自同一期刊（Water Research）
- [x] 正文语言与 `lang: en` 匹配
- [x] 每个 `[@key]` 在 `references.bib` 中都有对应条目——**已添加 Smith 2020**
- [x] 每个 `@fig-`/`@tbl-`/`@eq-`/`@sec-` 标签唯一
- [x] 无残留 `TODO`/`FIXME`/`XXX`
- [x] 所有图片路径可解析——**fig2-concentrations.png 已替换为 600 DPI 版本**
- [x] 图片分辨率 ≥300 DPI——**已通过 python3 PIL 确认**

---

## 第 4 步：渲染

```bash
quarto render
```

---

## 第 5 步：交付并附修改日志

**Agent：** *"三条审稿意见均已处理：*

| # | 修改内容 | 状态 |
|---|---------|------|
| 1 | 已将图 2 替换为 600 DPI 版本 | ✅ 完成 |
| 2 | 已在讨论部分增加"研究局限性"段落 | ✅ 完成 |
| 3 | 已通过 CrossRef 查找 DOI 并将 Smith 2020 添加到 references.bib | ✅ 完成 |

*修订稿已就绪：`_manuscript/index.docx`。`freeze:` 当前仍为 `false`——定稿前请设为 `true` 以锁定计算。如果有其他审稿意见需要处理，随时告诉我。"*
