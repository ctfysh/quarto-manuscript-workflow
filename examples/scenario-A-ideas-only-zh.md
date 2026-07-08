# 场景 A：只有想法 — 从主题到项目骨架

**研究者：** *"我想写一篇关于水生生态系统中微塑料的综述，投 Nature。"*

---

## 第 1 步：结构化访谈（2 个问题）

**Agent：** "好，确认两个问题：

1. **标题？** — 暂定标题即可，之后可以改。
2. **章节结构？** — 标准 IMRaD，还是你有特定大纲？"

**研究者：** *"标题：'淡水生态系统中微塑料污染：来源、归趋与生态影响'。标准 IMRaD 就行。"*

---

## 第 2 步：搭建项目骨架

Agent 创建初始项目结构：

```
microplastics-review/
├── _quarto.yml              # 项目配置 + Nature 模板
├── index.qmd                # 稿件正文，空缺处插 TODO
├── references.bib           # 空文件，后续添加文献
├── figures/                 # 空目录，后续添加图片
├── scripts/
│   └── abstract.lua         # 从 skill assets 复制
├── template.docx            # 从 skill assets 复制
├── nature.csl               # 从 skill journal-templates/ 复制
└── .gitignore               # _manuscript/, _freeze/, _supplementary/
```

第 3 步安装 `authors-block` 扩展后，目录还会包含 `_extensions/kapsner/authors-block/`。

`index.qmd` 中所有缺失部分用 TODO 块标记：

```markdown
---
title: "淡水生态系统中微塑料污染：来源、归趋与生态影响"
author:
  - name: "第一作者"  # TODO: 替换为实际作者信息
    affiliation: "某大学"
    corresponding: true
  - name: "第二作者"  # TODO: 替换为实际作者信息
    affiliation: "某大学"
date: today
abstract: |
  <!-- TODO: 摘要 — 150–250 字，概述范围、主要发现和结论 -->
filters:
  - authors-block                # 作者单位扩展
bibliography: references.bib
---

## 引言 {#sec-intro}

<!-- TODO: 引言（约 500 字）
  - 塑料生产和环境释放背景
  - 定义：原生 vs 次生微塑料
  - 海洋系统中已知的生态影响
  - 空白：淡水系统研究远少于海洋
  - 论点：本综述综合当前淡水微塑料研究现状 -->

## 方法 {#sec-methods}

<!-- TODO: 方法（约 300 字）
  - 文献检索策略（数据库、关键词、纳入/排除标准）
  - 文献筛选流程（PRISMA 流程图 @fig-prisma）
  - 数据提取方法 -->

## 结果 {#sec-results}

<!-- TODO: 结果（约 1000 字）
  - 淡水系统中的分布与检出
  - 来源与输入途径
  - 对淡水生物的生态效应
  - 关键研究汇总表（@tbl-studies） -->

## 讨论 {#sec-discussion}

<!-- TODO: 讨论（约 600 字）
  - 主要发现综合
  - 与海洋微塑料文献对比
  - 知识空白与未来研究方向
  - 方法学挑战 -->

## 结论 {#sec-conclusion}

<!-- TODO: 结论（约 200 字）
  - 关键发现总结
  - 对政策与管理的启示
  - 紧迫的研究需求 -->

# 参考文献

<!-- TODO: 添加参考文献 -->
```

---

## 第 3 步：套用 Nature 模板

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
    csl: nature.csl
    filters:
      - scripts/abstract.lua          # 将摘要从 YAML 移至正文
  pdf:
    reference-doc: template.docx
    csl: nature.csl
    filters:
      - scripts/abstract.lua
    cite-method: citeproc
execute:
  freeze: false
bibliography: references.bib
```

然后：
- 运行 `quarto add kapsner/authors-block` 安装第三方扩展
- 在 `index.qmd` frontmatter 中添加 `filters: [authors-block]`（不在 `_quarto.yml` 中，将 filter 限定在文章范围内，而非项目配置）

---

## 第 4 步：起飞前检查

- ✅ `.gitignore` 已包含 `_manuscript/`、`_freeze/` 和 `_supplementary/`
- ✅ `freeze: false`（编辑阶段）
- ✅ `lang: en` 匹配 Nature（英文期刊）
- ✅ `cite-method: citeproc`（Nature，不在例外列表）
- ✅ CSL 和 reference-doc 来自同一期刊
- ✅ 正文语言与 `lang: en` 一致（TODO 块为中文占位，正文待填充）

---

## 第 5 步：渲染

```bash
quarto render
```

输出：`_manuscript/index.docx`，使用 Nature 引用格式和版式。

---

## 交付

Agent 交付 `.docx` 和缺口报告：

```
✅ 项目骨架搭建完成，已套用 Nature 模板
✅ 可直接在 microplastics-review/index.qmd 中编辑

📋 待填充内容：
  🔴 作者信息    → 缺失
  🟡 摘要        → index.qmd 中有 TODO
  🟡 引言        → index.qmd 中有 TODO
  🟡 方法        → index.qmd 中有 TODO
  🟡 结果        → index.qmd 中有 TODO
  🟡 讨论        → index.qmd 中有 TODO
  🟡 结论        → index.qmd 中有 TODO
  🟡 参考文献    → 需要在 references.bib 中添加
  🟡 图片        → 放入 figures/ 目录
```

研究者填充 TODO 后，随时可让 Agent 重新渲染。
