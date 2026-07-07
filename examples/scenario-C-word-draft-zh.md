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
title: "长江沉积物中微塑料分布特征研究"
author:
  - name: 张伟
    affiliation: 南京大学
    corresponding: true
abstract: |
  <!-- TODO: 提取或撰写摘要 -->
bibliography: references.bib
---

## 引言 {#sec-intro}

淡水系统中微塑料污染已成为重大环境问题 [@smith2020]。与海洋环境
不同，河流沉积物中微塑料的分布和归趋仍鲜有表征 [@zhang2021]。
已有研究报道了多条中国主要河流中的微塑料丰度，但长江——亚洲最长的
河流——在文献中仍缺乏充分的表征。了解长江沉积物中微塑料的空间分布、
聚合物组成及潜在来源，对于评估淡水生物群面临的生态风险、制定有针对性
的污染控制策略具有重要意义。

## 方法 {#sec-methods}

### 研究区域 {#sec-study-area}

在长江中下游约 1,200 公里沿线的 15 个点位（从宜昌至上海）采集了
表层沉积物样品（0–5 cm 深度），每个点位采集三份平行样。采样使用
Van Veen 抓斗式采泥器，于 2022 年 11–12 月枯水期完成。采样点涵盖
城市、农业和工业区等不同土地利用类型，以全面反映长江流域微塑料
污染状况。

### 实验室分析 {#sec-lab}

沉积物中的微塑料采用氯化钠溶液（密度 1.2 g cm⁻³）密度分离法提取，
随后用湿式过氧化氢氧化去除天然有机质。在体视显微镜下对颗粒进行分拣和
计数，并使用傅里叶变换红外光谱（FTIR）衰减全反射（ATR）模式进行聚合物
鉴定。每个颗粒按形态（纤维、碎片、薄膜、球形）、颜色和聚合物类型进行
分类。

## 结果 {#sec-results}

微塑料浓度范围为每千克干沉积物 120–850 颗粒（图 1）。

![采样点及微塑料浓度](figures/fig1-map.png){#fig-map}

![各采样点聚合物组成](figures/fig3-polymer-distribution.png){#fig-polymers}

聚乙烯（PE）和聚丙烯（PP）是最主要的聚合物类型，分别占颗粒总数的
42% 和 28%，表明包装和农用薄膜是主要来源。所有采样点中，纤维是最
常见的形态（平均占 54%），其次为碎片（31%）和薄膜（11%）。微塑料
丰度与沉积物粒径之间未发现显著相关性，表明水动力条件和距城市中心的
距离等因素对微塑料沉积起更重要的作用。

## 讨论 {#sec-discussion}

本研究观察到的浓度与珠江 [@wang2022] 及多瑙河 [@kumar2019] 的报道值
相当，表明大型河流系统中的微塑料污染呈现相似的累积模式，主要受城市化
和工业活动驱动。

## 结论 {#sec-conclusion}

本研究系统评估了长江沉积物中的微塑料污染状况，发现污染广泛存在，
浓度范围为每千克干沉积物 120–850 颗粒。聚乙烯和聚丙烯在聚合物组成中
占主导地位，表明包装和农业源是主要贡献者。这些发现为未来监测工作建立
了关键基线，并强调了制定标准化分析方法的必要性，以实现在全球淡水生态
系统间的有意义的比较。

## 参考文献 {#sec-references}

::: {#refs}
:::
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

扩展安装完成、项目配置就绪后，Agent 执行渲染：

```bash
quarto render
```

输出：已排版的 `.docx`，ES&T 引用格式，图片就位，可直接提交。
