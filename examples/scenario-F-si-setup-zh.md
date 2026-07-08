# 场景 F：为现有项目添加 Supporting Information

**研究者：** *"我有一篇写好的稿件，还有补充材料（额外的方法和图表）。能帮我设置一个 Supporting Information 文件吗？"*

研究者已有一个可用的 Quarto 稿件项目（例如场景 A–D 的输出），现在需要添加 SI。

---

## 初始状态

```
project/
├── _quarto.yml              # 主稿件配置 (project.type: manuscript)
├── index.qmd                # YAML frontmatter: 标题、作者、摘要、关键词、filters
├── references.bib
├── template.docx
├── american-chemical-society.csl
├── scripts/
│   └── abstract.lua
├── figures/                 # 包含 fig-main.png, fig-setup.png
└── .gitignore
```

`_quarto.yml`：

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
lang: en
cite-method: natbib
format:
  docx:
    reference-doc: template.docx
    csl: american-chemical-society.csl
    filters:
      - scripts/abstract.lua
execute:
  freeze: false
bibliography: references.bib
```

`index.qmd` 前置元数据：

```markdown
---
title: "城市水道中微塑料表征研究"
author:
  - name: 陈明
    affiliation: 城市大学
    corresponding: true
    email: ming.chen@cityu.edu
  - name: 李贝丝
    affiliation: 城市大学
filters:
  - authors-block
abstract: |
  本研究对城市水道中的微塑料污染进行了表征。
keywords:
  - 微塑料
  - 城市水道
  - 聚合物表征
bibliography: references.bib
---
```

正文中已引用 SI 内容：

```markdown
## 方法 {#sec-methods}

样品采集按既定方案执行（采样点地图见补充图 S1）。详细的提取步骤见
[补充方法](#sec-supp-methods)。聚合物鉴定参数见补充表 S1。

## 结果

...
```

---

## 第 1 步：创建 `si.qmd`

纯 Markdown，无前置元数据。所有配置在 SI 项目配置中。

````markdown
# Supporting Information

## 补充方法 {#sec-supp-methods}

使用不锈钢抓斗采样器在城市水道沿线 12 个点位采集样品。每个样品通过 5 mm
筛网去除大颗粒杂质，然后在 30% H₂O₂ 中于 65 °C 消化 48 小时。

![沿城市水道 12 个采样点分布图。](figures/fig-setup.png){#fig-s1}

| 参数 | 仪器 | 检测限 |
|-----------|------------|-----------------|
| 粒径 | 体视显微镜 | 50 μm |
| 聚合物类型 | μ-FTIR | — |
| 质量 | 微量天平 | 0.1 mg |
: 微塑料表征仪器参数。{#tbl-s1}

$$ C = \frac{N}{V} $$ {#eq-conc}

## 参考文献

::: {#refs}
:::
````

---

## 第 2 步：创建 SI 项目配置（`_quarto-si.yml`）

放在项目根目录。CSL 必须与主稿件使用的期刊一致。

```yaml
project:
  type: default

title: "Supporting Information"

crossref:
  fig-title: "Figure S"
  tbl-title: "Table S"
  eq-title: "Equation S"

format:
  docx:
    reference-doc: template.docx
    csl: american-chemical-society.csl
    filters:
      - scripts/abstract.lua         # 与主稿共享——无 abstract 时无影响

bibliography: references.bib
```

**注意**：元数据（作者、摘要、关键词）在 `index.qmd` 前置元数据中，不在 `_quarto.yml` 中。这样 `si.qmd` 保持纯 Markdown，不会继承元数据。

---

## 第 3 步：复制后处理脚本

```bash
cp <skill-assets>/assets/scripts/fix-si-numbering.py scripts/
```

该脚本对公式编号进行后处理（`(1)` → `(S1)`）并处理图表题注 SEQ 域代码（作为旧版 Quarto 的回退方案）。仅使用 stdlib（`xml.etree.ElementTree`），无需额外包。

---

## 第 4 步：创建渲染包装脚本（`scripts/render-si.sh`）

将渲染和后处理合并为一个命令。该脚本在 `_supplementary/` 中创建独立项目，复制共享资源，渲染并运行公式编号修正：

```bash
#!/usr/bin/env bash
# render-si.sh — 一键 SI 渲染：独立项目 + 后处理
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SI_DIR="${PROJECT_DIR}/_supplementary"

mkdir -p "${SI_DIR}"

cp "${PROJECT_DIR}/si.qmd" "${SI_DIR}/"
for asset in template.docx references.bib; do
    [ -f "${PROJECT_DIR}/${asset}" ] && cp "${PROJECT_DIR}/${asset}" "${SI_DIR}/"
done
for f in "${PROJECT_DIR}/"*.csl; do
    [ -f "${f}" ] && cp "${f}" "${SI_DIR}/"
done

sed '/output-dir:/d' "${PROJECT_DIR}/_quarto-si.yml" > "${SI_DIR}/_quarto.yml"
if ! grep -qE '\[@[A-Za-z]' "${SI_DIR}/si.qmd" 2>/dev/null; then
    sed -i '' '/^bibliography:/d; /^    csl:/d' "${SI_DIR}/_quarto.yml"
fi

cd "${SI_DIR}"
quarto render
python3 "${SCRIPT_DIR}/fix-si-numbering.py" si.docx
```

> **为什么不用 `quarto render --profile si`？** 当主项目使用 `project.type: manuscript` 时，profile 合并机制会阻止公式渲染为 OMML 数学对象。独立子目录方式完全避免了这个问题。

---

## 第 5 步：验证元数据位置

确认 `_quarto.yml` 中不包含 `authors:`、`abstract:` 或 `keywords:`。这些必须只放在 `index.qmd` 前置元数据中：

```yaml
# ❌ 错误——_quarto.yml 中放元数据会污染项目根配置：
# _quarto.yml
author:
  - name: 陈明
...

# ✅ 正确——作用域限定在 index.qmd，SI 是纯 Markdown：
# index.qmd
---
author:
  - name: 陈明
...
---
```

---

## 第 6 步：起飞前检查

- ✅ `si.qmd` 已创建，包含 SI 内容和交叉引用标签
- ✅ `_quarto-si.yml` 中 `project.type` 为 `default`（非 `manuscript`）
- ✅ `_quarto-si.yml` 包含带 S 前缀标题的 `crossref` 配置
- ✅ `scripts/fix-si-numbering.py` 已复制且可用
- ✅ `scripts/render-si.sh` 已创建且可执行
- ✅ `.gitignore` 已包含 `_supplementary/`
- ✅ 元数据在 `index.qmd` 前置元数据中，不在 `_quarto.yml` 中
- ✅ 主稿与 SI 之间的交叉引用使用纯文本（如"补充图 S1"），而非 `@fig-s1`
- ✅ `index.qmd` 中每个纯文本 SI 引用都有对应的 `{#fig-...}` / `{#tbl-...}` 标签存在于 `si.qmd`

---

## 第 7 步：渲染两个文件

```bash
# 主稿件
quarto render

# Supporting Information
bash scripts/render-si.sh
```

---

## 结果

```
project/
├── _quarto.yml              # 主稿件配置
├── _quarto-si.yml           # SI profile
├── index.qmd                # YAML frontmatter + 正文
├── si.qmd                   # 纯 Markdown SI 内容
├── scripts/
│   ├── abstract.lua
│   ├── fix-si-numbering.py  # 公式 S 前缀后处理器
│   └── render-si.sh         # 一键 SI 渲染脚本
├── figures/
├── _manuscript/
│   └── index.docx           # 主稿件（图 1、表 1）
├── _supplementary/
│   └── si.docx              # SI（图 S1、表 S1、公式 S1）
├── template.docx
├── american-chemical-society.csl
├── references.bib
└── .gitignore
```

**Agent：** *"SI 已配置完成。运行 `quarto render` 渲染主稿件，`bash scripts/render-si.sh` 渲染 SI。SI 中的公式编号会自动后处理为 `(S1)` 格式。如果需要添加更多图表或章节，随时告诉我。"*
