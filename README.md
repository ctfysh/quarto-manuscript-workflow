# Quarto Manuscript Workflow

[**English**](#english) | [**中文**](#中文)

An AI-agent skill for academic manuscript production. Hand the agent your materials (notes, Word draft, figures, or just an idea) and get back a journal-formatted `.docx`. No `.qmd` syntax to write, no Quarto commands to run. **Slash command: `/quarto-manuscript-workflow`**

---

## English

### How to use

Activate the skill in three ways:

| Way | Example | How it works |
|-----|---------|-------------|
| **Slash command** | `/quarto-manuscript-workflow I want to submit this draft to ES&T` | Symlinked in `~/.config/opencode/skills/` → loads skill automatically |
| **Natural language** | "Help me format this paper for Nature" | The orchestrator detects manuscript intent and loads the skill automatically |
| **Explicit skill call** | "Load the manuscript skill" | Triggers `skill(name="quarto-manuscript-workflow")` directly |

Once activated, tell the agent your materials and target journal. Everything else is automated.

![Quarto Manuscript Workflow overview](assets/banner-en.png)

### Examples by scenario

| Scenario | What you have | Example |
|----------|--------------|---------|
| A | Just an idea, nothing written | [`examples/scenario-A-ideas-only-en.md`](examples/scenario-A-ideas-only-en.md) |
| B | Scattered notes, slides, emails | [`examples/scenario-B-fragments-en.md`](examples/scenario-B-fragments-en.md) |
| C | A complete Word/Markdown draft | [`examples/scenario-C-word-draft-en.md`](examples/scenario-C-word-draft-en.md) |
| D | Final manuscript, need formatting | [`examples/scenario-D-complete-manuscript-en.md`](examples/scenario-D-complete-manuscript-en.md) |
| E | Existing Quarto project, need QA | [`examples/scenario-E-existing-project-en.md`](examples/scenario-E-existing-project-en.md) |
| F | Need Supporting Information with SI setup | [`examples/scenario-F-si-setup-en.md`](examples/scenario-F-si-setup-en.md) |
| G | Got reviewer comments, need revision | [`examples/scenario-G-revision-en.md`](examples/scenario-G-revision-en.md) |

### What makes this different

| Problem | Solution |
|---------|----------|
| Fragments (notes, slides, chats, half a draft) | Agent classifies → IMRaD assembly → marks uncertainty |
| Only an idea + target journal | 2-question interview → full scaffold with TODO blocks |
| Complete Word/Markdown draft | Parse styles → extract figures/citations → generate bib from DOIs → IMRaD check → apply template |
| Iterate on structure | Reorder sections, swap figures, add citations, re-render on demand |
| Don't know what's missing | Coverage report: ✅ Intro ✅ Methods ❌ Results — all gaps at once |
| **Need Supporting Information** | Create si.qmd + _quarto-si.yml → set up standalone render → post-process equation numbers |

The agent never blocks on missing material — inserts `<!-- TODO: ... -->` and keeps going.

### Input → Output

| You give… | Agent does… |
|-----------|-------------|
| Journal name | Looks up CSL, copies reference-doc, generates `_quarto.yml` |
| `.docx` / Markdown / notes / slides | Parses into `.qmd` sections, extracts figures, generates bib entries |
| Topic + journal (e.g. "microplastics review for Nature") | 2-question interview → full scaffold with TODOs |
| "Swap to ES&T" | Swaps CSL + config, re-renders |
| "Methods after Results" | Reorders sections, re-renders |

Output: rendered `.docx` with journal CSL, reference-doc typography, auto-placed figures, abstract from YAML, optional SI with S-prefix numbering.

### Adaptive workflow

Agent picks the flow based on your materials, not a fixed pipeline:

- **Ideas only** → 2 questions → scaffold + TODOs → template → render
- **Fragments** → classify → assemble → coverage report → template → render
- **Full draft** → parse → extract → template → render
- **Existing Quarto project** → verify config → check cross-refs → re-render
- **Revision request** → edit → pre-flight → render → deliver

### Pre-flight checklist (agent runs this before render)

- `.gitignore` covers `_manuscript/`, `_freeze/`, `_supplementary/`
- `freeze:` matches phase (`false` editing, `true` final)
- `lang:` matches journal (all current → `en`)
- `cite-method` matches journal (default `citeproc`; ACS/ES&T → `natbib`)
- CSL + reference-doc from same journal
- Body language matches `lang:`; mark uncertain segments with `<!-- LANG-CHECK -->`
- Every `[@key]` has matching `references.bib` entry
- Every `@fig-`/`@tbl-`/`@eq-`/`@sec-` label is unique
- No `TODO`/`FIXME`/`XXX` remain (unless acknowledged)
- All figure paths resolve
- **If SI exists**: `_quarto-si.yml` `project.type` is `default`, `crossref` present
- **If SI exists**: `bash scripts/render-si.sh` runs without error
- **If SI exists**: equation numbers show `(S1)` not `(1)`
- **If SI exists**: cross-references between main and SI use plain text, not `@fig-` (no automated check — agent must verify manually)
- **If SI exists**: every plain-text SI ref in `index.qmd` has a matching `{#fig-...}` label in `si.qmd`

---

## 中文

### 使用方法

三种方式激活 skill：

| 方式 | 示例 | 原理 |
|------|------|------|
| **斜杠命令** | `/quarto-manuscript-workflow 帮我把这篇稿子投 ES&T` | symlink 到 `~/.config/opencode/skills/` → 自动加载 skill |
| **自然语言** | "帮我整理稿件投 Nature" | 编排器检测到稿件意图，自动加载 skill |
| **显式调用** | "加载 manuscript skill" | 直接触发 `skill(name="quarto-manuscript-workflow")` |

激活后告诉 Agent 你的素材和目标期刊即可，剩下全自动。

![Quarto Manuscript Workflow 概览](assets/banner-zh.png)

### 场景示例

| 场景 | 你的素材 | 示例 |
|------|----------|------|
| A | 只有想法 | [`examples/scenario-A-ideas-only-zh.md`](examples/scenario-A-ideas-only-zh.md) |
| B | 零散的笔记、PPT、邮件 | [`examples/scenario-B-fragments-zh.md`](examples/scenario-B-fragments-zh.md) |
| C | 完整的 Word/Markdown 稿 | [`examples/scenario-C-word-draft-zh.md`](examples/scenario-C-word-draft-zh.md) |
| D | 写好的稿子，只要排版 | [`examples/scenario-D-complete-manuscript-zh.md`](examples/scenario-D-complete-manuscript-zh.md) |
| E | 已有 Quarto 项目，需要检查 | [`examples/scenario-E-existing-project-zh.md`](examples/scenario-E-existing-project-zh.md) |
| F | 需要 Supporting Information，配置 SI 独立渲染 | [`examples/scenario-F-si-setup-zh.md`](examples/scenario-F-si-setup-zh.md) |
| G | 收到审稿意见，需要修改 | [`examples/scenario-G-revision-zh.md`](examples/scenario-G-revision-zh.md) |

### 这套 skill 解决了什么问题

| 问题 | 做法 |
|------|------|
| 碎片材料（笔记、PPT、聊天、半成品） | 分类 → IMRaD 组装 → 标记不确定段落 |
| 只有想法 + 目标期刊 | 问 2 个问题 → 搭建骨架 + TODO |
| 完整的 Word/Markdown 稿 | 解析样式 → 提取图表和引用 → 构建 `.qmd` → 套模板 |
| 反复调整结构 | 调顺序、换图、补引用，按需重新渲染 |
| 不知道缺什么 | 覆盖率报告：✅ 引言 ✅ 方法 ❌ 结果，一次展示所有缺口 |

Agent 从不因缺内容阻塞——插入 `<!-- TODO: ... -->` 后继续推进。

### 输入 → 输出

| 你给… | Agent… |
|-------|--------|
| 期刊名称 | 查找 CSL，复制 reference-doc，生成 `_quarto.yml` |
| `.docx` / Markdown / 笔记 / 幻灯片 | 解析到 `.qmd`，提取图片，通过 DOI 生成 bib |
| 选题 + 期刊（如"微塑料综述，投 Nature"） | 问 2 个问题 → 搭建骨架 + TODO |
| "改投 ES&T" | 换 CSL 和配置，重新渲染 |
| "把方法移到结果后面" | 重排章节，重新渲染 |

输出：已排版的 `.docx`，含期刊 CSL、reference-doc 版式、自动排图、摘要移至正文、可选 SI（S 前缀编号）。

### 自适应工作流

Agent 根据素材类型自动选择策略：

- **只有想法** → 问 2 个问题 → 骨架 + TODO → 套模板 → 渲染
- **碎片材料** → 分类 → 拼装 → 缺口报告 → 套模板 → 渲染
- **完整稿子** → 解析 → 提取 → 套模板 → 渲染
- **已有 Quarto 项目** → 验证配置 → 检查交叉引用 → 重新渲染
- **修改请求** → 编辑 → 起飞前检查 → 渲染 → 交付

### 起飞前检查（Agent 每次渲染前自动执行）

- `.gitignore` 已包含 `_manuscript/`、`_freeze/`、`_supplementary/`
- `freeze:` 与当前阶段匹配（编辑中 = `false`，定稿 = `true`）
- `lang` 与期刊语言一致（当前全部期刊 → `en`）
- `cite-method` 与所选期刊一致（默认 `citeproc`；ACS/ES&T → `natbib`）
- CSL 和 reference-doc 来自同一期刊
- 正文语言与 `lang` 匹配，不确定的标记 `<!-- LANG-CHECK -->`
- 每个 `[@key]` 在 `references.bib` 中有对应条目
- 每个 `@fig-`/`@tbl-`/`@eq-`/`@sec-` 标签唯一
- 无残留 `TODO`/`FIXME`/`XXX`（已确认的除外）
- 所有图片路径可解析
- **如含 SI**：`_quarto-si.yml` 中 `project.type` 为 `default`，含 `crossref`
- **如含 SI**：`bash scripts/render-si.sh` 运行无报错
- **如含 SI**：方程编号显示 `(S1)` 而非 `(1)`
- **如含 SI**：跨文件引用使用纯文本，非 `@fig-`（无自动检查，Agent 需手动验证）
- **如含 SI**：`index.qmd` 中每个纯文本 SI 引用都有对应的 `{#fig-...}` 标签存在于 `si.qmd`
