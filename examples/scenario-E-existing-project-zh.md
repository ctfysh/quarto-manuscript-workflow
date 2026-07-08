# 场景 E：已有 Quarto 项目 — 检查与修复

**研究者：** *"我自己用 Quarto 写了篇文章，能帮我检查一下配置是否正确，然后渲染出来吗？"*

研究者提供：一个已有 Quarto 项目目录。

---

## 第 1 步：验证 `_quarto.yml`

Agent 读取项目配置并逐项检查：

```yaml
project:
  type: manuscript               # ✅ 正确
manuscript:
  article: index.qmd             # ✅ 文件存在
format:
  docx:
    reference-doc: template.docx # ⚠️ 引用了但项目根目录没有
    csl: nature.csl              # ⚠️ 引用了但项目根目录没有
execute:
  freeze: false                  # ✅ 编辑阶段
bibliography: references.bib     # ✅ 文件存在
```

**发现问题：**
- `template.docx` 和 `nature.csl` 被引用但不存在 → Agent 从 skill 资产中复制过去
- 没有 `filters:` 配置 → Agent 复制 `abstract.lua` 到 `scripts/abstract.lua` 并添加 `scripts/abstract.lua` 过滤器
- 没有设置 `lang:` → Agent 添加 `lang: en`

### Agent 执行修复：

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
format:
  docx:
    reference-doc: template.docx
    csl: nature.csl
    filters:
      - scripts/abstract.lua
lang: en
execute:
  freeze: false
bibliography: references.bib

> **注意：** 此项目已有作者格式，无需安装 `authors-block` 扩展。

## 研究者的 `index.qmd`：

```markdown
---
title: "淡水环境中微塑料污染的综合评估"
author:
  - name: "陈伟"
    affiliations: "华东大学环境科学系"
    corresponding: true
  - name: "Sarah Johnson"
    affiliations: "加利福尼亚大学水资源研究所"
abstract: |
  微塑料污染已成为全球淡水生态系统面临的普遍环境威胁。本研究对华东地区15个淡水站点进行了微塑料污染综合评估，结合野外采样、光谱表征和生态风险建模。结果表明，研究区域普遍存在微塑料污染，平均丰度为每立方米1,850 ± 420个颗粒，主要成分为聚乙烯和聚丙烯纤维。我们发现了微塑料丰度与上游工业活动之间的显著相关性，并估算出区域生态风险指数从中等到高等不等。这些发现强调了建立标准化监测协议和制定针对性缓解策略的紧迫性。
bibliography: references.bib
---

## 引言

微塑料污染（直径小于5毫米的塑料颗粒）已成为人类世最紧迫的环境挑战之一 [@liu2022]。虽然初期研究主要集中在海洋环境，但越来越多的证据表明，淡水系统可能成为微塑料从陆源向海洋汇输送的重要通道。河流、湖泊和水库通过废水排放、城市径流、工业排放和大气沉降接收微塑料输入，但与海洋研究相比，针对淡水污染的综合性评估仍然有限。

微塑料分布的空间格局与城市和工业区的距离密切相关 @fig-sampling。然而，标准化的采样、提取和鉴定方法仍然缺乏，这使得跨研究比较面临挑战。

## 方法 {#sec-methods}

### 采样方案

于2026年3月至6月期间，在长三角地区的15个站点采集水样。每个站点使用不锈钢桶收集三份表层水样（每份50升），通过300 μm不锈钢筛过滤。保留物被冲洗至玻璃瓶中，并在4°C下运送到实验室。

### 实验室分析

微塑料提取采用饱和NaCl溶液（1.2 g/cm³）的密度分离法，随后通过0.45 μm玻璃纤维过滤器过滤。在体视显微镜下目视识别颗粒，并使用衰减全反射模式的傅里叶变换红外光谱（FTIR）进行化学表征。

### 统计分析

生态风险评估采用聚合物危害指数（PHI）和潜在生态风险指数（PERI），基于已建立的方法进行。微塑料丰度与土地利用变量之间的相关性分析采用Spearman秩相关。

## 结果

所有采样点共鉴定出8,325个疑似微塑料颗粒，平均丰度为每立方米1,850 ± 420个颗粒 @fig-results。最高浓度出现在YZ-07站点（3,210颗粒/m³），该站点位于一个大型纺织制造区下游约2公里处；最低浓度出现在YZ-15站点（420颗粒/m³），该站点为保护区湿地。

| 聚合物类型 | 丰度 (%) | 平均粒径 (μm) | PHI 评分 |
|:---|---:|---:|---:|
| 聚乙烯 | 42.3 | 820 ± 310 | 11 |
| 聚丙烯 | 28.7 | 650 ± 280 | 4 |
| 聚苯乙烯 | 12.5 | 440 ± 190 | 30 |
| 聚酯 | 9.8 | 510 ± 220 | 425 |
| 其他 | 6.7 | 560 ± 250 | — |

: 所有采样点检测到的微塑料聚合物组成、粒径分布和危害评分 {#tbl-comparison}

微塑料丰度与距工业区距离之间的关系遵循对数衰减模型（R² = 0.87，@eq-1）。基于PERI框架的生态风险评估将15个站点中的6个分类为高风险，PHI值主要由聚酯纤维贡献，尽管其丰度相对较低。

## 讨论

我们的发现表明，长三角地区的淡水微塑料污染既普遍又具有生态显著性。聚乙烯和聚丙烯纤维的主导地位与全球产量和该地区普遍的纺织工业排放相一致。聚酯纤维尽管丰度较低，却成为生态危害评分的主要驱动因素，这一发现凸显了聚合物特异性风险评估的重要性。

微塑料丰度与工业区邻近度之间的强相关性强调了点源污染在淡水污染中的作用。然而，即使在偏远站点也存在广泛分布的微塑料，这表明存在显著的大气传输和扩散性污染途径，需要进一步研究。

## 结论

本研究首次对长三角淡水系统中的微塑料污染进行了综合评估。我们的结果建立了基线污染水平，识别了关键的聚合物特异性风险驱动因素，并展示了综合风险评估框架在淡水微塑料污染评估中的实用性。未来的研究应关注季节性动态、生物摄入以及标准化监测协议的制定，以支持监管行动。

## 参考文献
```

---

## 第 2 步：检查交叉引用

Agent 扫描 `index.qmd` 中所有 `@` 引用并验证：

```
文档中的引用：
  @fig-sampling    → ✅ figures/sampling-map.png 存在
  @fig-results     → ✅ figures/results-overview.png 存在
  @tbl-comparison  → ✅ 结果章节中找到了管道表格
  @sec-methods     → ✅ 找到了 ## 方法 章节
  @eq-1            → ❌ 文档中没有标注为 {#eq-1} 的公式
  @liu2022         → ❌ references.bib 中没有 liu2022 条目
```

**发现问题：**
- `@eq-1` 引用断裂——公式缺少或标签错误
- `@liu2022` 缺少参考文献条目

Agent 能修的当场修（搜索 DOI 添加 bib 条目），不能修的标记报告。

---

## 第 3 步：检查图片

```
figures/
├── sampling-map.png       → ✅ 600 DPI，已被引用
├── results-overview.png   → ✅ 300 DPI，已被引用
└── raw-data.png           → ⚠️ 文件存在但正文未引用
```

---

## 第 4 步：语言检查

Agent 检测正文全部为英文 → ✅ 与 `lang: en` 一致。

---

## 第 5 步：起飞前检查

- ✅ `.gitignore` 存在
- ✅ `freeze: false`（编辑阶段）
- ✅ `lang: en` 匹配
- ✅ `cite-method: citeproc`（之前未设置 → 使用默认值）
- ✅ CSL 和 reference-doc 现在已可用
- ⚠️ `@eq-1` 交叉引用断裂 → 报告给研究者
- ⚠️ `@liu2022` 参考文献条目已通过 DOI 搜索补上
- ⚠️ `raw-data.png` 未被引用 → 报告给研究者

---

## 第 6 步：渲染

```bash
quarto render
```

---

## 交付

**Agent：** *"项目已修复并渲染完成。已修复的问题：*

- *将缺失的 template.docx 和 nature.csl 复制到项目根目录*
- *创建 scripts/ 目录并在 _quarto.yml 中添加了 scripts/abstract.lua 过滤器*
- *在 _quarto.yml 中添加了 `lang: en`*
- *搜索并补上了 Liu 2022 的 DOI 到 references.bib*

*⚠️ 需要你手动处理的问题：*
- *`@eq-1` — 文档中未找到对应的公式标签*
- *`figures/raw-data.png` — 文件存在但正文未引用*

*这是渲染好的 .docx。"*
