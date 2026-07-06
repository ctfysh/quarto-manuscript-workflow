---
name: quarto-manuscript-workflow
description: "Use when a researcher needs to produce a formatted academic manuscript — they have fragments (notes, PPT, Word, Markdown) rather than a complete draft, need journal-style formatting, or want to systematically organize existing materials for submission."
---

# Quarto Manuscript Workflow

## Overview

This skill guides the AI agent as a **translation layer** between the researcher and Quarto. The researcher provides materials; the agent assembles them into a proper Quarto manuscript project, applies journal templates, iterates on revisions, and delivers a formatted .docx. The researcher **never** writes .qmd syntax or runs commands.

## Core Concepts (for the AI agent)

- **Quarto manuscript project:** `quarto create project --type manuscript` — single source (`index.qmd`) produces DOCX/PDF/HTML
- **.qmd structure:** Markdown + YAML frontmatter (`---`) + cross-references (`@fig-`, `@sec-`, etc.)
- **Journal template library:** `assets/template.docx` + 22 `*.csl` files in `journal-templates/`. The agent dynamically generates `_quarto-journal.yml` per session — no per-journal config files on disk.
- **Output pipeline:** `.qmd` → `quarto render` → `_manuscript/index.docx`

## Prerequisites

- **Quarto ≥1.3** — `quarto --version`
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

Agent strategy — puzzle assembly:

1. **Classify** each fragment → Introduction / Methods / Results / Discussion / Unknown
2. **Infer** IMRaD placement from context, mark uncertain with `<!-- FUZZY -->`
3. **Assemble** into .qmd in IMRaD order
4. **Coverage report**: ✅ Intro ✅ Methods ❌ Results ⚠️ Discussion ❌ Abstract — present all gaps at once, batch questions

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

- **Always renderable** — Never wait. Every gap → TODO block.
- **Batch questions** — One structured gap report, not individual Q&A.
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
5. **Mark uncertain** translations with `<!-- LANG-CHECK: original text -->` — do not silently guess
6. **Figure captions and table headers**: always normalize to target language

Applies to Scenario B (fragments → assembly), Scenario C (Word/Markdown → .qmd), and Scenario D (complete manuscript with mixed-language content). Scenario A (ideas only) and E (existing project) produce content in the target language from the start.

## Template Application

Researcher only says which journal — agent handles everything:

1. **Look up** the journal → identify CSL file, `cite-method`, and target language
2. **Note language**: all current journals are English (`lang: en`); if adding a non-English journal the language must be set explicitly
3. **Copy** `assets/template.docx` + the matching `*.csl` to project root
4. **If CSL not bundled**: download from [CSL style repository](https://github.com/citation-style-language/styles) or [Zotero style search](https://www.zotero.org/styles)
5. **Generate config** depending on context:

   **New project** — write complete `_quarto.yml` and install extensions:
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
       filters:
         - abstract.lua
         - authors-block
     pdf:
       csl: <journal>.csl
       cite-method: citeproc       # or natbib
   execute:
     freeze: false                 # toggle to true for final render
   bibliography: references.bib
   ```
   Then run `quarto add kapsner/authors-block` to install the third-party author affiliation extension.
   Create `figures/` directory (empty, for figures to be added).

   **Switching journals** — write `_quarto-journal.yml` with only format overrides:
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
7. **Pre-flight check** before render:
   - ✅ `.gitignore` exists with `_manuscript/` and `_freeze/`
   - ✅ `freeze:` matches phase (`false` during editing, `true` for final)
   - ✅ `lang:` matches journal language (all current journals → `en`)
   - ✅ `cite-method` matches journal (default `citeproc`; ACS/ES&T → `natbib`)
   - ✅ CSL + reference-doc are from the same journal
   - ✅ Manuscript body language matches `lang:` — auto-fix detected mismatches, mark uncertain segments with `<!-- LANG-CHECK -->`

### Customization entry points

- **Paper size**: `format.pdf.papersize: a4` (or `letter`)
- **Main font**: `format.pdf.mainfont: Times New Roman`
- **Margins**: `format.pdf.geometry: margin=1in`
- **Line spacing**: Set in `template.docx` (for DOCX) or via LaTeX package (for PDF)

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

## Submission Readiness

- [ ] File naming matches journal requirements
- [ ] Figure resolution ≥300 DPI
- [ ] Word/page count within journal limits
- [ ] Supplementary materials separate from main file
- [ ] Required sections present (data availability, author contributions, etc.)
- [ ] CSL matches target journal (verify citation format in .docx)

## Journal Template Index

All 22 CSL files in `journal-templates/` use `cite-method: citeproc` and target language `lang: en`. Exceptions:

| Field | Exception |
|-------|-----------|
| `cite-method: natbib` | ACS, ES&T |
| Non-English `lang:` | (none yet — set explicitly when adding a non-English journal) |
