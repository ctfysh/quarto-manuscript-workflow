# 场景 D：完整稿子 — 只排版，不修改内容

**研究者：** *"稿子写好了，帮我排版成 Water Research 的格式，给我 .docx。"*

研究者提供：`final-draft.md`（一篇完整的 Markdown 稿件）

---

## 第 1 步：读取验证

Agent 检查全部章节——内容完整，无 TODO，无缺口：

```
✅ 标题："Occurrence and Removal of Microplastics in Drinking Water Treatment Plants"
✅ 作者：6 位作者及单位
✅ 摘要：约 200 字
✅ 引言：约 800 字
✅ 方法：约 1200 字（采样、提取、FTIR 分析）
✅ 结果：约 1500 字，含 4 张图片
✅ 讨论：约 1000 字
✅ 结论：约 300 字
✅ 参考文献：42 条
✅ 图片：4 处引用
✅ 补充材料：正文中已引用
```

**Agent：** *"稿件内容完整，直接套 Water Research 模板渲染。"*

无访谈、无 TODO 块、无缺口分析。直接跳至模板应用。

---

## 第 2 步：套用模板

Agent 复制 `water-research.csl` 和 `template.docx`，生成 `_quarto.yml`：

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
lang: en
format:
  docx:
    reference-doc: template.docx
    csl: water-research.csl
  pdf:                       # 同时配置 PDF 输出
    csl: water-research.csl
execute:
  freeze: true               # 定稿渲染 — freeze
bibliography: references.bib
filters:
  - abstract.lua
```

稿件已有作者格式，无需 `authors-block` 扩展。

---

## 第 3 步：起飞前检查

- ✅ `.gitignore` 已设置
- ✅ `freeze: true`（定稿渲染）
- ✅ `lang: en` 匹配期刊
- ✅ `cite-method: citeproc`（Water Research）
- ✅ 正文语言全英文，无混杂
- ✅ 4 张图片路径均有效
- ✅ 所有 `[@key]` 在参考文献中有对应条目
- ✅ 无 TODO/FIXME/XXX 残留
- ✅ 图片分辨率达标（≥300 DPI）

---

## 第 4 步：渲染

```bash
quarto render
```

---

## 交付

**Agent：** *"已完成。稿件已按 Water Research 格式排版。"*

交付文件：`_manuscript/index.docx`

换刊只需一句话：

**研究者：** *"改成投 Journal of Hazardous Materials。"*

**Agent：** *"切换模板中..."*
1. 复制（或下载）`journal-of-hazardous-materials.csl`
2. 写入 `_quarto-journal.yml`（仅覆盖格式相关配置）
3. 起飞前检查
4. 重新渲染

一分钟内交付新格式的稿件。
