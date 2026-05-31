---
name: quarto-manuscript-workflow
description: "Use when a researcher needs to produce a formatted academic manuscript — they have fragments (notes, PPT, Word, Markdown) rather than a complete draft, need journal-style formatting, or want to systematically organize existing materials for submission."
---

# Quarto Manuscript Workflow

## Overview — Agent handles Quarto, researcher handles content

This skill guides the AI agent to act as a **translation layer** between the researcher and Quarto. The researcher provides materials (notes, Word drafts, Markdown files, figures). The agent assembles them into a proper Quarto manuscript project, fills gaps with TODO placeholders, applies journal templates, iterates on revisions, and delivers a formatted .docx.

The researcher **never** writes .qmd syntax or runs quarto commands.

**Key experience:** Always renderable. Even incomplete manuscripts produce a .docx with TODO blocks showing what's missing.

## Core Concepts (for the AI agent)

- **Quarto manuscript project:** `quarto create project --type manuscript` — single source (`index.qmd`) produces DOCX/PDF/HTML
- **.qmd structure:** Markdown + YAML frontmatter (`---`) + cross-references (`@fig-`, `@sec-`, etc.)
- **Three-file journal template interface:** `_quarto-journal.yml` (format config) + `.csl` (citation style) + `template.docx` (Word reference doc)
- **Output pipeline:** `.qmd` → `quarto render` → `_manuscript/index.docx`

## Prerequisites

- **Quarto ≥1.3** — `quarto --version` to check
- **LaTeX distribution** — Required for PDF output (TinyTeX recommended: `quarto install tinytex`)
- **Pandoc** — Bundled with Quarto

## Intake Protocol: 材料导入

Collect and classify researcher input into three types:

| Input Type | Examples | Agent Strategy |
|------------|----------|----------------|
| **A: Fragments**  | Word snippets, PPT slides, meeting notes, emails, chat messages | Iterative puzzle assembly — ask clarifying questions, infer IMRaD placement, mark uncertain mappings as TODOs |
| **B: Markdown files** | Obsidian/Notion exports, .md files | Direct read, adapt wikilinks/tags to Quarto syntax, copy figures to `figures/` |
| **C: Complete Word draft** | Full .docx manuscript | Bulk convert — parse Word styles (Heading 1/2/3 → .qmd headings), extract figures, identify citations |

Intake flow — present coverage map to researcher:

```markdown
Agent: "我收到了你的材料。当前覆盖情况：
       ✅ Introduction — 来自基金申请的背景部分
       ✅ Methods — 来自实验 protocol
       ❌ Results — 只有 PPT 图，缺文字
       ⚠️ Discussion — 不完整
       ❌ Abstract — 缺失
       ❌ References — 只有 3 个 DOI
       请补充：1) Results 每张图的文字说明 2) Discussion 后半部分"
```

## Gap Handling Protocol: 材料不全怎么办

Three-color severity system:

| Severity | Examples | Agent Behavior |
|----------|----------|----------------|
| 🔴 Blocking | No body text at all | Stop, ask "你有草稿吗？还是只有想法？" |
| 🟡 Fillable | Missing a section, missing figure file, incomplete bib | Insert TODO block in .qmd, continue, batch questions |
| 🟢 Low priority | Missing ORCID, no journal selected, no abstract | Use defaults/placeholders, note for later |

### TODO block mechanism

For each 🟡 gap, insert a visible block in the .qmd:

```markdown
## Discussion {#sec-discussion}

<!-- TODO-BLOCK: Discussion 未完成 -->
> **需补充：**
> - Figure 3 结果的理论解释
> - 与既往研究对比（Liu 2021, Wang 2022 已在 bib）
> - 研究局限性
> - 预期 ~800 字
<!-- END-TODO-BLOCK -->
```

### Rules
- **Always renderable.** Never wait for complete materials. Every gap gets a TODO.
- **Batch questioning.** Collect all gaps → present a single structured gap report. Do NOT ask one question at a time.

## Content Assembly: 拼装 .qmd

Convert researcher input into proper .qmd syntax:

1. **Section structure** — Detect headings from input → `## 标题 {#sec-xxx}`
2. **Figures** — Copy files to `figures/` → `![Caption](figures/xxx.png){#fig-xxx}`
3. **Citations** — Generate bib entry from DOI → `[@key]` in text
4. **Formatting** — Preserve bold/italic/underline from Word
5. **Frontmatter** — Generate YAML (title, authors, abstract, keywords)
6. **IMRaD check** — Flag missing sections for researcher

### Markdown adaptation (Obsidian/Notion users)

| Source | Conversion |
|--------|------------|
| `[[wikilink]]` | `@fig-label` or `@sec-label` |
| `#tag` | keywords YAML |
| Notion tables | Quarto pipe tables |
| Existing Pandoc citation `[@key]` | Preserved |
| `![](attachments/fig.png)` | Copy to `figures/`, update path |

## Template Application: 套用期刊模板

1. **Select journal** from `journal-templates/` (or use default if undecided)
2. **Copy** `.csl` + `template.docx` to project root
3. **Merge** `_quarto-journal.yml` content into researcher's `_quarto.yml` under `format:`
4. **Notify** researcher of template applied and format defaults

Example merged `_quarto.yml`:

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
format:
  docx:
    reference-doc: template.docx
    csl: journal-style.csl
  pdf:
    csl: journal-style.csl
    cite-method: natbib
execute:
  freeze: true
bibliography: references.bib
```

**If no journal selected** → use a default generic template. Render still works.

### Customization entry points

- **Paper size**: `format.pdf.papersize: a4` (or `letter`)
- **Main font**: `format.pdf.mainfont: Times New Roman`
- **Margins**: `format.pdf.geometry: margin=1in`
- **Line spacing**: Set in `template.docx` (for DOCX) or via LaTeX package (for PDF)

## Iteration Loop: 修改 → 渲染 → 交付

```markdown
Researcher says: "Figure 2 换一张新图"
Agent:           replaces figure file, updates caption in .qmd
                 → `quarto render` → delivers new .docx

Researcher says: "方法部分调到结果后面"
Agent:           reorders sections in .qmd
                 → `quarto render` → delivers new .docx

Researcher says: "加一篇 Smith 2023"
Agent:           finds DOI → adds bib entry → inserts [@smith2023]
                 → `quarto render` → delivers new .docx
```

## Render QA Checklist

Run before final delivery:

- [ ] Every `[@key]` has matching entry in `references.bib`
- [ ] Every `@fig-`, `@tbl-`, `@eq-`, `@sec-` label is unique
- [ ] No `TODO` / `FIXME` / `XXX` placeholders remain (unless acknowledged)
- [ ] `freeze` set correctly (`false` for editing, `true` for final)
- [ ] All figure paths resolve to existing files

## Submission Readiness

- [ ] File naming matches journal requirements
- [ ] Figure resolution ≥300 DPI
- [ ] Word/page count within journal limits
- [ ] Supplementary materials separate from main file
- [ ] Required sections present (data availability, author contributions, etc.)
- [ ] CSL matches target journal (verify citation format in .docx)

## Filters & Extensions

### Custom Lua filters

Save as `*.lua` in project root, reference in `_quarto.yml`:

```yaml
format:
  docx:
    filters:
      - abstract.lua
```

### Third-party extensions

```bash
quarto add kapsner/authors-block
```

Reference in `_quarto.yml`:

```yaml
format:
  docx:
    filters:
      - authors-block
```

## Cross-Referencing Conventions

| Type | Syntax | Label Example |
|------|--------|---------------|
| Equation | `$$...$$ {#eq-label}` | `@eq-energy` |
| Figure | `![Caption](path){#fig-label}` | `@fig-results` |
| Table | `: Caption {#tbl-label}` | `@tbl-demographics` |
| Section | `## Title {#sec-label}` | `@sec-methods` |

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Committing `_manuscript/`** | Output files in git history | Add `_manuscript/` to `.gitignore` |
| **`freeze: true` misunderstanding** | Edits not reflected in output | Set `false` during editing, `true` only for final render |
| **CSL + reference-doc conflict** | Citation formatting looks wrong | CSL controls bibliography; template.docx controls typography. Don't mix journal X CSL with journal Y template |
| **Missing `.gitignore`** | Build artifacts tracked | Commit `.gitignore` before first `quarto render` |
| **Wrong `cite-method` for PDF** | LaTeX compilation errors | Use `citeproc` for CSL-only, `natbib` or `biblatex` for LaTeX-native bibliographies |

## Commands Reference

```bash
quarto render              # Build all formats
quarto render index.qmd    # Build single file
quarto preview             # Live preview (HTML only)
quarto check               # Verify Quarto installation
quarto install tinytex     # Install LaTeX for PDF
```

## Journal Template Index

| Journal | Directory | Formats | Citation Style |
|---------|-----------|---------|----------------|
| ACS | `journal-templates/acs/` | DOCX, PDF | American Chemical Society |
| APA | `journal-templates/apa/` | DOCX, PDF | APA 7th edition |
| Nature | `journal-templates/nature/` | DOCX, PDF | Nature numeric |
| Elsevier (Harvard) | `journal-templates/elsevier-harvard/` | DOCX, PDF | Elsevier Harvard |
| Elsevier (Vancouver) | `journal-templates/elsevier-vancouver/` | DOCX, PDF | Elsevier Vancouver |
| Wiley | `journal-templates/wiley/` | DOCX, PDF | Wiley standard |
| Springer | `journal-templates/springer/` | DOCX, PDF | Springer standard |
| Taylor & Francis | `journal-templates/taylor-francis/` | DOCX, PDF | Taylor & Francis |
| IEEE | `journal-templates/ieee/` | DOCX, PDF | IEEE |
| Chicago | `journal-templates/chicago/` | DOCX, PDF | Chicago Manual of Style |
| MLA | `journal-templates/mla/` | DOCX, PDF | MLA |
| Water Research | `journal-templates/water-research/` | DOCX, PDF | Water Research |
| Environmental Science & Technology | `journal-templates/environmental-science-technology/` | DOCX, PDF | ES&T |
| Journal of Hydrology | `journal-templates/journal-of-hydrology/` | DOCX, PDF | Journal of Hydrology |
| Science of the Total Environment | `journal-templates/science-of-the-total-environment/` | DOCX, PDF | STOTEN |
| Ecology | `journal-templates/ecology/` | DOCX, PDF | Ecology (ESA) |
| Global Change Biology | `journal-templates/global-change-biology/` | DOCX, PDF | Global Change Biology |
| Geophysical Research Letters | `journal-templates/geophysical-research-letters/` | DOCX, PDF | GRL (AGU) |
| Biogeosciences | `journal-templates/biogeosciences/` | DOCX, PDF | Biogeosciences |
| Limnology and Oceanography | `journal-templates/limnology-and-oceanography/` | DOCX, PDF | L&O |
| Journal of Environmental Management | `journal-templates/journal-of-environmental-management/` | DOCX, PDF | JEMA |
| Journal of Cleaner Production | `journal-templates/journal-of-cleaner-production/` | DOCX, PDF | JCP |
