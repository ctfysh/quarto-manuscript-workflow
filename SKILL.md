---
name: quarto-manuscript-workflow
description: "Use when a researcher needs to produce a formatted academic manuscript — they have fragments (notes, PPT, Word, Markdown) rather than a complete draft, need journal-style formatting, or want to systematically organize existing materials for submission."
---

# Quarto Manuscript Workflow

## Overview

This skill sits between the researcher and Quarto. The researcher provides materials; the agent assembles them into a Quarto manuscript project, applies journal templates, revises, and delivers a formatted .docx. The researcher never writes .qmd syntax or runs commands.

## Core Concepts (for the AI agent)

- **Quarto manuscript project:** `quarto create project --type manuscript`. Single source (`index.qmd`) produces DOCX/PDF/HTML.
- **.qmd structure:** Markdown + YAML frontmatter (`---`) + cross-references (`@fig-`, `@sec-`, etc.)
- **Journal template library:** `assets/template.docx` + 22 `*.csl` files in `journal-templates/`. The agent dynamically generates `_quarto-journal.yml` per session. No per-journal config files on disk.
- **Output pipeline:** `.qmd` → `quarto render` → `_manuscript/index.docx`

## Prerequisites

- **Quarto ≥1.3**. Run `quarto --version`.
- **LaTeX** for PDF output (`quarto install tinytex`)

## Workflow (adaptive)

Agent auto-selects flow based on what the researcher provides:

### Scenario A: Ideas only, no materials

```
Researcher: "I want to write a review on microplastics in aquatic ecosystems"
→ Agent: structured interview (title? journal? IMRaD?)
→ Scaffold full project (all TODO blocks) → apply template → Render → deliver
```

No detail questions. Title + journal only, everything else as TODO.

### Scenario B: Fragments (notes, PPT slides, emails, chat messages)

Agent strategy: puzzle assembly.

1. **Classify** each fragment → Introduction / Methods / Results / Discussion / Unknown
2. **Infer** IMRaD placement from context, mark uncertain with `<!-- FUZZY -->`
3. **Assemble** into .qmd in IMRaD order
4. **Coverage report**: ✅ Intro ✅ Methods ❌ Results ⚠️ Discussion ❌ Abstract. Present all gaps at once, batch questions.

### Scenario C: Word draft / Markdown files

1. **Word → .qmd**: parse Word styles (Heading 1/2/3 → `## {#sec-xxx}`), extract figures, identify citations
2. **Markdown adaptation**: `[[wikilink]]` → `@fig-label`, `#tag` → keywords, Notion tables → pipe tables
3. **Figures**: ensure `figures/` directory exists, then copy figures from Word/attachments into it
4. **Citations**: generate bib entries from DOIs
5. **Frontmatter**: generate YAML (title, authors, abstract, keywords)
6. **IMRaD check**: flag missing sections
7. **Apply template** → Render → deliver

### Scenario D: Complete manuscript (already written)

```
Researcher: "Here's my draft, submit to Nature"
→ Agent: apply Nature template → Render → deliver
```

Skip assembly and gap analysis. Just identify journal, apply template, render.

### Scenario E: Existing Quarto project

```
Researcher: "Check if this Quarto project is formatted correctly"
→ Agent: verify `_quarto.yml` → check cross-references → re-render → deliver
```

Content untouched, format QA only.

---

### TODO block

```markdown
<!-- TODO: Discussion missing - ~800 words needed: theoretical explanation,
     comparison with Liu 2021/Wang 2022, limitations -->
```

### Core rules

- **Always renderable**. Never wait. Every gap → TODO block.
- **Batch questions**. One structured gap report, not individual Q&A.
- **Three-color severity:**

| Severity | Examples | Agent Behavior |
|----------|----------|----------------|
| 🔴 Blocking | No body text | Stop, ask for draft |
| 🟡 Fillable | Missing section/figure/bib | Insert TODO → continue |
| 🟢 Low priority | No ORCID/journal/abstract | Use defaults |

## Language normalization

After assembling or parsing user content and before template application, normalize all manuscript prose to match the target journal's language:

1. **Detect** language of each prose block (paragraphs, captions, section titles, table cells)
2. **Translate** any block that does not match the target language to the target language (e.g., Chinese notes → English for an English-language journal)
3. **Preserve** as-is: technical terms, citation keys (`[@key]`), DOIs, URLs, code, equations, LaTeX math, reference labels (`@fig-`, `@sec-`)
4. **Keep** `<!-- TODO -->` and `<!-- FUZZY -->` markers in English regardless of target language
5. **Mark uncertain** translations with `<!-- LANG-CHECK: original text -->`. Do not silently guess.
6. **Figure captions and table headers**: always normalize to target language

Applies to Scenario B (fragments → assembly), Scenario C (Word/Markdown → .qmd), and Scenario D (complete manuscript with mixed-language content). Scenario A (ideas only) and E (existing project) produce content in the target language from the start.

## Template Application

Researcher only says which journal. Agent handles everything:

1. **Look up** the journal → identify CSL file, `cite-method`, and target language
2. **Note language**: all current journals are English (`lang: en`); if adding a non-English journal the language must be set explicitly
3. **Copy** `assets/template.docx` + the matching `*.csl` to project root
4. **If CSL not bundled**: download from [CSL style repository](https://github.com/citation-style-language/styles) or [Zotero style search](https://www.zotero.org/styles)
5. **Generate config** depending on context:

   **New project**. Write complete `_quarto.yml` and install extensions:
    ```yaml
    project:
      type: manuscript
    manuscript:
      article: index.qmd
    lang: en
    format:
      docx:
        reference-doc: template.docx
        csl: <journal>.csl
      pdf:
        csl: <journal>.csl
        cite-method: citeproc       # or natbib
    execute:
      freeze: false                 # toggle to true for final render
    bibliography: references.bib
    filters:
      - abstract.lua
      - authors-block
    ```
   Then run `quarto add kapsner/authors-block` to install the third-party author affiliation extension.
   Create `figures/` directory (empty, for figures to be added).

   **Switching journals**. Write `_quarto-journal.yml` with only format overrides:
   ```yaml
   format:
     docx:
       csl: <journal>.csl
     pdf:
       csl: <journal>.csl
       cite-method: citeproc       # or natbib
   ```
   (Quarto merges `_quarto-journal.yml` into `_quarto.yml` automatically.)

6. **Notify** researcher of template applied
7. **Optionally offer SI setup**: If the researcher mentions Supporting Information, see the [Supporting Information](#supporting-information-si) section.
8. **Pre-flight check** before render:
   - ✅ `.gitignore` exists with `_manuscript/` and `_freeze/`
   - ✅ `freeze:` matches phase (`false` during editing, `true` for final)
   - ✅ `lang:` matches journal language (all current journals → `en`)
   - ✅ `cite-method` matches journal (default `citeproc`; ACS/ES&T → `natbib`)
   - ✅ CSL + reference-doc are from the same journal
   - ✅ Manuscript body language matches `lang:`. Auto-fix detected mismatches, mark uncertain segments with `<!-- LANG-CHECK -->`

### Customization entry points

- **Paper size**: `format.pdf.papersize: a4` (or `letter`)
- **Main font**: `format.pdf.mainfont: Times New Roman`
- **Margins**: `format.pdf.geometry: margin=1in`
- **Line spacing**: Set in `template.docx` (for DOCX) or via LaTeX package (for PDF)

## Supporting Information (SI)

Many journals require a separate Supporting Information (aka Supplementary Material) file alongside the main manuscript. Quarto's `project.type: manuscript` is designed for single-article output, so SI needs explicit handling.

### Architecture: dual-file independent render

```
index.qmd → quarto render              → _manuscript/index.docx     (Figure 1, Table 1)
si.qmd    → quarto render --profile si → _supplementary/si.docx     (Figure S1, Table S1)
```

Each file is rendered independently with its own config. SI uses a **Quarto profile** to bypass the `project.type: manuscript` constraint (see below).

### Step 1: Create `si.qmd`

Pure markdown, zero YAML frontmatter. All configuration lives in the profile.

```qmd
# Supporting Information

## Supplementary Methods

Detailed experimental procedures are described below.

## Supplementary Results

![Supplementary experimental data.](figures/placeholder.png){#fig-extra}

Refer to @fig-extra within this document.

| Parameter | Value |
|-----------|-------|
| Condition A | 42.3 ± 0.5 |
| Condition B | 17.8 ± 0.3 |
: Experimental parameters measured under standard conditions. {#tbl-params}

$$ y = \alpha + \beta x + \epsilon $$ {#eq-supplement}

## References

::: {#refs}
:::
```

### Step 2: Create the SI profile (`_quarto-si.yml`)

Quarto `project.type: manuscript` only renders the QMD referenced in `manuscript: article:`. Other QMDs in the project root are ignored. The **profile mechanism** is the workaround:

Copy the template from `assets/_quarto-si.yml` into the project root:

```bash
cp _extensions/quarto-manuscript-workflow/assets/_quarto-si.yml _quarto-si.yml
```

Template content:

```yaml
project:
  type: default
  output-dir: _supplementary

title: "Supporting Information"

# Clear metadata inherited from _quarto.yml
authors: []
abstract: ""
keywords: []

crossref:
  fig-title: "Figure S"
  tbl-title: "Table S"
  eq-title: "Equation S"

format:
  docx:
    reference-doc: template.docx
    csl: american-chemical-society.csl

bibliography: references.bib
```

**Key rules:**
- Profile file must be at project root, named `_quarto-{name}.yml`
- Render with `quarto render --profile si`
- Always set `project: type: default` (not `manuscript`) to avoid the article-only constraint
- Always clear `authors`, `abstract`, `keywords` (to override inherited main-manuscript metadata)
- `crossref` config goes in the profile (not the QMD) — both `index.qmd` and `si.qmd` are pure markdown

### Step 3: S-prefix numbering

| Element | YAML config | Caption display | Implementation |
|---------|-------------|-----------------|----------------|
| Figure | `fig-title: "Figure S"` | Figure S1 | Quarto native |
| Table | `tbl-title: "Table S"` | Table S1 | Quarto native |
| Equation | `eq-title: "Equation S"` | Equation S1 | YAML + post-process |

### Step 4: Cross-references — critical DOCX limitation

**Quarto's DOCX writer does not propagate `fig-title`/`tbl-title` into cross-reference text.** `@fig-extra` always renders as "Figure 1" in DOCX regardless of `crossref` config. This is a DOCX format limitation, not a bug.

| Reference type | How to write | Example |
|----------------|-------------|---------|
| Within SI | `@fig-xxx` (normal Quarto ref) | `@fig-extra` → "Figure S1" (correct within SI) |
| Main → SI | Manual markdown link | `[Supplementary Figure S1](#fig-extra)` |
| SI → Main | Manual markdown link | `[see Methods in main text](#sec-methods)` |

For the main manuscript (`index.qmd`), write SI references as:

```markdown
Supplementary Figure S1 shows the experimental data (see [Supplementary Figure S1](#fig-extra)).
```

This produces clean readable text in DOCX while maintaining a clickable link in HTML/PDF.

### Step 5: Equation numbering — post-processing required

`eq-title: "Equation S"` changes the *label text* (e.g., "Equation 1" → "Equation S1") but does **not** change the equation number itself `(1)` → `(S1)`. In DOCX, equation numbers are stored in OOXML `<m:t>` elements under the math namespace, outside Pandoc's AST reach.

**Solution**: Post-process the rendered DOCX with a Python script using `lxml`. A reusable template is bundled at `assets/scripts/fix-si-numbering.py` in this skill. Copy it into the project:

```bash
cp _extensions/quarto-manuscript-workflow/assets/scripts/fix-si-numbering.py scripts/
# Or directly from the skill source:
# cp /path/to/skill/assets/scripts/fix-si-numbering.py scripts/
```

The script handles two fixes:

```python
# fix-si-numbering.py key logic (full script at assets/scripts/fix-si-numbering.py):

# 1. Caption numbering: inject "S " into SEQ field codes
#    "SEQ Figure \\* ARABIC" → "SEQ Figure S \\* ARABIC" → Figure S1
for instr in doc.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instrText"):
    if " SEQ Figure " in instr.text:
        instr.text = instr.text.replace(" SEQ Figure ", " SEQ Figure S ")
    # similar for " SEQ Table "

# 2. Equation numbers: inject "S" into OMath <m:t> elements
#    "(1)" → "(S1)"
for t in doc.iter("{http://schemas.openxmlformats.org/officeDocument/2006/math}t"):
    if t.text and t.text.strip().startswith("(") and t.text.strip().endswith(")"):
        num = t.text.strip()[1:-1]
        if num.isdigit():
            t.text = t.text.replace(f"({num})", f"(S{num})")
```

**Caption NBSP handling**: When `fig-title: "Figure S"` is used, Quarto may insert a non-breaking space between the title prefix and the auto-number. The script above handles this by injecting "S " between "SEQ Figure" and the sequence number in the DOCX field codes.

### Step 6: One-command render wrapper

Bundle the render + post-process into `scripts/render-si.sh`. A template is at `assets/scripts/render-si.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
quarto render --profile si
python scripts/fix-si-numbering.py _supplementary/si.docx
echo "Done: _supplementary/si.docx"
```

Copy it from the skill assets:

```bash
cp _extensions/quarto-manuscript-workflow/assets/scripts/render-si.sh scripts/
chmod +x scripts/render-si.sh
```

### File structure after SI setup

```
project/
├── _quarto.yml            # Main manuscript config (project.type: manuscript)
├── _quarto-si.yml         # SI profile (project.type: default)
├── index.qmd              # Pure markdown, no frontmatter
├── si.qmd                 # Pure markdown, no frontmatter
├── scripts/
│   ├── abstract.lua       # Pandoc Lua filter (moves YAML abstract→body)
│   ├── fix-si-numbering.py # DOCX post-processor (equation S prefix + caption NBSP)
│   └── render-si.sh       # One-command SI render
├── template.docx
├── american-chemical-society.csl
├── references.bib
└── figures/
```

### SI best practices

- **Keep QMDs clean**: Both `index.qmd` and `si.qmd` should be pure markdown. All config in YAML files.
- **Profile naming**: `_quarto-si.yml` is conventional. Use `_quarto-supplementary.yml` if preferred.
- **References**: SI can share `references.bib` or have its own. If sharing, only cited entries appear.
- **Figures**: Put SI-specific figures in `figures/` alongside main figures. Filenames don't need SI prefix — labels handle that.
- **Equation post-processing is DOCX-only**: For PDF output, LaTeX handles `\tag{S1}` natively in the equation environment.
- **Lua filters cannot fix this**: Pandoc Lua filters operate on the AST, which does not contain DOCX field codes or OMath elements. DOCX-specific issues require OOXML-level post-processing.

## Iteration Loop

Researcher request → agent edit → `quarto render` → deliver new .docx:

- "Replace Figure 2 with a new image" → replace file, update caption → render
- "Move Methods after Results" → reorder sections → render
- "Add Smith 2023 citation" → find DOI → add bib entry → insert cite → render

## Render QA Checklist

Run before final delivery:

- [ ] Every `[@key]` has matching entry in `references.bib`
- [ ] Every `@fig-`, `@tbl-`, `@eq-`, `@sec-` label is unique
- [ ] No `TODO` / `FIXME` / `XXX` placeholders remain (unless acknowledged)
- [ ] `freeze` set correctly (`false` for editing, `true` for final)
- [ ] All figure paths resolve to existing files
- [ ] **If SI exists**: `_quarto-si.yml` `project.type` is `default` (not `manuscript`)
- [ ] **If SI exists**: `scripts/render-si.sh` renders without error
- [ ] **If SI exists**: Equation numbers in SI show `(S1)` not `(1)` (run post-process)

## Submission Readiness

- [ ] File naming matches journal requirements
- [ ] Figure resolution ≥300 DPI
- [ ] Word/page count within journal limits
- [ ] SI rendered as independent file via profile (`quarto render --profile si`)
- [ ] SI equation numbers show "S" prefix (`(S1)` not `(1)`)
- [ ] Cross-references between main and SI use plain text (not `@fig-` which renders as "Figure 1" in DOCX)
- [ ] Required sections present (data availability, author contributions, etc.)
- [ ] CSL matches target journal (verify citation format in .docx)

## Journal Template Index

All 22 CSL files in `journal-templates/` use `cite-method: citeproc` and target language `lang: en`. Exceptions:

| Field | Exception |
|-------|-----------|
| `cite-method: natbib` | ACS, ES&T |
| Non-English `lang:` | (none yet. Set explicitly when adding a non-English journal) |
