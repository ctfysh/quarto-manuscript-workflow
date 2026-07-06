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
- 没有 `filters:` 配置 → Agent 添加 `abstract.lua` 过滤器
- 没有设置 `lang:` → Agent 添加 `lang: en`

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
- *在 _quarto.yml 中添加了 abstract.lua 过滤器*
- *搜索并补上了 Liu 2022 的 DOI 到 references.bib*

*⚠️ 需要你手动处理的问题：*
- *`@eq-1` — 文档中未找到对应的公式标签*
- *`figures/raw-data.png` — 文件存在但正文未引用*

*这是渲染好的 .docx。"*
