# 场景 C：Word 稿 → 从 .docx 到期刊就绪的 .qmd

**研究者：** *"这是我写好的 Word 稿，帮我排成 Environmental Science & Technology 的格式。"*

研究者提供：`manuscript-draft.docx`

---

## 第 1 步：解析 Word 样式

Agent 打开 `.docx`，将 Word 样式映射为 `.qmd` 结构：

```
Word 样式            →  .qmd 元素
────────────────────────────────────
Title                →  YAML title:
Authors              →  YAML authors:
Heading 1 "引言"     →  ## 引言 {#sec-intro}
Heading 1 "方法"     →  ## 方法 {#sec-methods}
Heading 2 "研究区域" →  ### 研究区域 {#sec-study-area}
Heading 2 "实验室分析" → ### 实验室分析 {#sec-lab}
Heading 1 "结果"     →  ## 结果 {#sec-results}
Heading 1 "讨论"     →  ## 讨论 {#sec-discussion}
Heading 1 "结论"     →  ## 结论 {#sec-conclusion}
正文（Normal）       →  段落文本
嵌入图片             →  ![](figures/fig1.png){#fig-map}
```

---

## 第 2 步：提取图表

Agent 从 Word 中提取 5 张嵌入图片：

```
figures/
├── fig1-map.png
├── fig2-concentrations.png
├── fig3-polymer-distribution.png
├── fig4-sediment-profile.png
└── fig5-comparison.png
```

每张图片按 Word 中的图注自动生成 `@fig-` 标签。

---

## 第 3 步：识别引用

Agent 扫描正文中的行内引用：

| 文中引用 | 处理 |
|---------|------|
| `(Smith et al., 2020)` | 搜索 DOI → 加入 `references.bib` |
| `(Zhang & Li, 2021)` | 搜索 DOI → 加入 `references.bib` |
| `(Kumar et al., 2019)` | 搜索 DOI → 加入 `references.bib` |
| `(Wang, 2022)` | 未找到 DOI → 标记 `<!-- TODO: 查找 Wang 2022 的 DOI -->` |

引用格式转换为 `[@smith2020]`、`[@zhang2021]` 等。

---

## 第 4 步：生成 .qmd

Agent 生成完整的 `index.qmd`（格式配置放在 `_quarto.yml` 中）：

```markdown
---
title: "Microplastic Distribution in Yangtze River Sediments"
author:
  - name: Wei Zhang
    affiliation: Nanjing University
abstract: |
  <!-- TODO: 提取或撰写摘要 -->
bibliography: references.bib
---

## 引言 {#sec-intro}

淡水系统中微塑料污染已成为重大环境问题 [@smith2020]。与海洋环境
不同，河流沉积物中微塑料的分布和归趋仍鲜有表征 [@zhang2021]...

...正文继续...

## 方法 {#sec-methods}

### 研究区域 {#sec-study-area}

在长江沿线 15 个点位采集了沉积物样品...

### 实验室分析 {#sec-lab}

样品采用密度分离和 FTIR 光谱进行分析...

## 结果 {#sec-results}

微塑料浓度范围为每千克干沉积物 120–850 颗粒（图 1）。

![采样点及微塑料浓度](figures/fig1-map.png){#fig-map}

![各采样点聚合物组成](figures/fig3-polymer-distribution.png){#fig-polymers}

## 讨论 {#sec-discussion}

本研究观察到的浓度与珠江报道值相当 [@wang2022 <!-- TODO: 验证 DOI -->]...

## 结论 {#sec-conclusion}

...

## 参考文献 {#sec-references}
```

---

## 第 5 步：IMRaD 检查

```
✅ 引言 — 已填充
✅ 方法 — 已填充（研究区域 + 实验室分析完整）
✅ 结果 — 已填充（3 张图片引用）
✅ 讨论 — 已填充
✅ 结论 — 已填充但偏短（约 80 字）
❌ 摘要 — 缺失，标记为 TODO
```

---

## 第 6 步：套用 ES&T 模板 + 渲染

Agent 生成 `_quarto.yml`：

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
lang: en
format:
  docx:
    reference-doc: template.docx
    csl: environmental-science-and-technology.csl
  pdf:
    csl: environmental-science-and-technology.csl
    cite-method: natbib               # ES&T 例外
execute:
  freeze: false
bibliography: references.bib
filters:
  - abstract.lua
  - authors-block
```

然后运行 `quarto add kapsner/authors-block` 安装扩展，生成 `_extensions/kapsner/authors-block/`。

```
✅ figures/ 目录已创建，内含 5 张提取图片
✅ references.bib 含 3 条有效条目（1 条 TODO）
```

```bash
quarto render
```

输出：已排版的 `.docx`，ES&T 引用格式，图片就位，可直接提交。
