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
- **authors-block extension** for author affiliations. Install with `quarto add kapsner/authors-block`.
- **Python 3** (stdlib) for SI DOCX post-processing (uses `xml.etree.ElementTree` — no extra packages), only if SI is needed.

## Workflow (adaptive)

Agent auto-selects flow based on what the researcher provides:

### Adaptive scenarios

| Input | Strategy |
|-------|----------|
| **Ideas only** | 2-question interview (title? journal?) → scaffold with TODOs → render |
| **Fragments** (notes, PPT, emails) | Classify → IMRaD assemble (`<!-- FUZZY -->`) → coverage report → render |
| **Word/Markdown draft** | Parse styles → extract figures/citations → generate bib from DOIs → IMRaD check → render |
| **Complete manuscript** | Identify journal → apply template → render |
| **Existing project** | Verify config → check cross-refs → re-render |
| **SI setup** | Add SI to existing project → create si.qmd, _quarto-si.yml, render wrapper → render |
| **Revision request** | Read reviewer comments → edit manuscript → pre-flight → render → deliver with change log |

### Scenario classification logic

Use this decision tree to classify the input:

```
1. Does the researcher mention reviewer comments / revision / "大修" / "小修"?
   → YES → Scenario G (Revision)
   → NO ↓

2. Is there an existing Quarto project (index.qmd + _quarto.yml on disk)?
   → YES → Scenario E (Existing project)
   → NO ↓

3. Does the researcher have a complete Word/Markdown draft (≥80% sections present)?
   → YES → Scenario C (Word/Markdown draft)
   → NO ↓

4. Does the researcher have a final manuscript that just needs formatting?
   → YES → Scenario D (Complete manuscript)
   → NO ↓

5. Does the researcher want Supporting Information added?
   → YES → Scenario F (SI setup)
   → NO ↓

6. Does the researcher have scattered materials (notes, PPT, emails, partial text)?
   → YES → Scenario B (Fragments)
   → NO → Scenario A (Ideas only)
```

All variants: missing content → `<!-- TODO -->` block, never block on gaps. Batch all questions into one structured gap report.

🔴 **CHECKPOINT**: After detecting scenario, present classification to researcher and confirm before proceeding. Example: "I detect this is a **fragments** scenario (B). I'll assemble your notes into IMRaD structure with ES&T template. Correct?"

Example walkthroughs for all variants are in [`examples/`](examples/).

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

## Anti-patterns (do NOT do)

| # | Don't | Why | Do instead |
|---|-------|-----|-----------|
| 1 | **Block on missing content** | Researcher may not have all material ready | Insert `<!-- TODO: ... -->` and continue — never wait |
| 2 | **Ask questions one at a time** | Annoying, slows workflow | Batch all gaps into one structured report |
| 3 | **Guess uncertain translations** | Silent errors corrupt manuscript | Mark with `<!-- LANG-CHECK: original -->` |
| 4 | **Put metadata in `_quarto.yml`** | Leaks into SI rendering | Metadata goes in `index.qmd` frontmatter only |
| 5 | **Use `@fig-` cross-refs between main↔SI** | DOCX doesn't propagate S-prefix | Use plain text links: `[Supplementary Figure S1](#fig-extra)` |
| 6 | **Run `quarto render` on SI with `project.type: manuscript`** | OMML bug — equation numbers break | Use `scripts/render-si.sh` (standalone project in `_supplementary/`) |
| 7 | **Skip pre-flight checklist** | Silent config mismatches cause render failures | Always run checklist before `quarto render` |
| 8 | **Hardcode journal-specific settings in `_quarto.yml`** | Breaks when switching journals | Use `_quarto-journal.yml` overlay for journal-specific overrides |

---

## Language normalization

Before template application, normalize prose to match target journal's language:

1. **Detect** language per block; translate non-matching blocks. Preserve: citation keys, DOIs, URLs, code, equations, labels.
2. **Keep** `<!-- TODO -->` / `<!-- FUZZY -->` markers in English.
3. **Mark uncertain** translations with `<!-- LANG-CHECK: original -->`. Do not silently guess.
4. **Figure captions + table headers**: always normalize to target language.

Applies to scenarios producing new content (B/C). Scenarios A/D/E work with existing content in target language.

## Template Application

Researcher only says which journal. Agent handles everything:

🔴 **CHECKPOINT**: Confirm target journal before applying template. Example: "Target journal: **ES&T** (cite-method: natbib, lang: en). Applying template now."

1. **Look up** the journal → identify CSL file, `cite-method`, and target language
2. **Note language**: all current journals are English (`lang: en`); if adding a non-English journal the language must be set explicitly
3. **Copy** `assets/template.docx` + the matching `*.csl` from `journal-templates/` + `assets/scripts/abstract.lua` to the project (`abstract.lua` → `scripts/abstract.lua`)
4. **Create** `scripts/` and `figures/` directories.
5. **If CSL not bundled**: download from [CSL style repository](https://github.com/citation-style-language/styles) or [Zotero style search](https://www.zotero.org/styles)
6. **Generate config** depending on context:

   **New project**. Write complete `_quarto.yml`:
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
          - scripts/abstract.lua
      pdf:
        reference-doc: template.docx
        csl: <journal>.csl
        filters:
          - scripts/abstract.lua
        cite-method: citeproc       # or natbib
    execute:
      freeze: false                 # toggle to true for final render
    bibliography: references.bib
    ```
   Then:
   - Ensure `quarto add kapsner/authors-block` has been run to install the third-party author affiliation extension.
   - Add `authors-block` to `index.qmd` frontmatter (not in `_quarto.yml` — metadata (authors, abstract, keywords) must live in `index.qmd` frontmatter to avoid leaking into SI rendering).
   Create `.gitignore` with `_manuscript/`, `_freeze/`, `_supplementary/`, `.DS_Store`, `__pycache__/`, `*.pyc`, `.omo/`.

   **Switching journals**. Write `_quarto-journal.yml` with only format overrides:
    ```yaml
    format:
      docx:
        csl: <journal>.csl
        filters:
          - scripts/abstract.lua
      pdf:
        csl: <journal>.csl
        filters:
          - scripts/abstract.lua
        cite-method: citeproc       # or natbib
    ```
    (Quarto merges `_quarto-journal.yml` into `_quarto.yml` automatically. `authors-block` must still be in `index.qmd` frontmatter.)

7. **Notify** researcher of template applied
8. **Optionally offer SI setup**: If the researcher mentions Supporting Information, see the [Supporting Information](#supporting-information-si) section.

### Customization entry points

- **Paper size**: `format.pdf.papersize: a4` (or `letter`)
- **Main font**: `format.pdf.mainfont: Times New Roman`
- **Margins**: `format.pdf.geometry: margin=1in`
- **Line spacing**: Set in `template.docx` (for DOCX) or via LaTeX package (for PDF)

## Supporting Information (SI)

Many journals require a separate Supporting Information (aka Supplementary Material) file alongside the main manuscript. Quarto's `project.type: manuscript` is designed for single-article output, so SI needs explicit handling.

### Architecture: dual-file independent render

```
index.qmd → quarto render                     → _manuscript/index.docx     (Figure 1, Table 1)
si.qmd    → _supplementary/ + quarto render   → _supplementary/si.docx     (Figure S1, Table S1)
```

Each file is rendered independently. The SI is rendered as a **standalone Quarto project** in the `_supplementary/` subdirectory, bypassing the `project.type: manuscript` constraint that prevents multi-article output.

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

### Step 2: Create the SI project config (`_quarto-si.yml`)

Quarto `project.type: manuscript` only renders the QMD referenced in `manuscript: article:`. Other QMDs in the project root are ignored. The solution: render `si.qmd` as a **standalone project** in `_supplementary/`, using `_quarto-si.yml` as the template.

Write `_quarto-si.yml` at project root. Match the CSL to the main manuscript's journal:

```yaml
project:
  type: default

title: "Supporting Information"

# Document metadata (title, authors, abstract, keywords) lives in
# index.qmd frontmatter, NOT in _quarto.yml. The SI project's
# _quarto.yml only needs crossref and format settings.

crossref:
  fig-title: "Figure S"
  tbl-title: "Table S"
  eq-title: "Equation S"

format:
  docx:
    reference-doc: template.docx
    csl: <journal>.csl               # Same CSL as main manuscript
    filters:
      - scripts/abstract.lua         # Shared with main — harmless when abstract is absent

bibliography: references.bib
```

The render script uses this file as a template, stripping `output-dir:` and conditionally omitting `bibliography`/`csl` when `si.qmd` contains no citations.

**Key rules:**
- `project: type: default` (not `manuscript`) — avoids the article-only constraint
- **Metadata goes in `index.qmd` frontmatter**, not in `_quarto.yml`
- `crossref` config goes in the project config (not the QMD) — both `index.qmd` and `si.qmd` are pure markdown

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

**Pre-flight**: verify every plain-text SI ref in `index.qmd` ("Supplementary Figure S1", "Supplementary Table S1") has a matching `{#fig-...}` / `{#tbl-...}` label in `si.qmd`. No automated check — agent must verify manually.

### Step 5: Equation numbering — post-processing required

`eq-title: "Equation S"` changes the *label text* (e.g., "Equation 1" → "Equation S1") but does **not** change the equation number itself `(1)` → `(S1)`. In DOCX, equation numbers are stored in OOXML `<m:t>` elements under the math namespace, outside Pandoc's AST reach.

**Solution**: Post-process the rendered DOCX with `assets/scripts/fix-si-numbering.py` (stdlib only — `xml.etree.ElementTree`, no extra packages). Copy to `scripts/`:

```bash
cp <skill-assets>/assets/scripts/fix-si-numbering.py scripts/
```

The script uses a pattern registry (`PATTERNS` list). New patterns are added as functions and registered when Pandoc's OMML output changes. The script tries each pattern and uses the first match.

### Step 6: One-command render wrapper

Bundle render + post-process into `scripts/render-si.sh`:

```bash
cp <skill-assets>/assets/scripts/render-si.sh scripts/
chmod +x scripts/render-si.sh
```

The script creates a standalone project in `_supplementary/` (avoids OMML bug from `--profile si` with `project.type: manuscript`), copies shared assets, renders, and runs the equation fix. See `assets/scripts/render-si.sh` for the full implementation. After setup, render the SI with: `bash scripts/render-si.sh`

### File structure after SI setup

```
project/
├── _quarto.yml            # Main manuscript config (project.type: manuscript)
├── _quarto-si.yml         # SI project config template (project.type: default)
├── index.qmd              # YAML frontmatter: title, authors, abstract, keywords, filters (authors-block)
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

- **`si.qmd`**: pure markdown. Metadata lives in `index.qmd` frontmatter only.
- **Config naming**: `_quarto-si.yml` is conventional. Use `_quarto-supplementary.yml` if preferred.
- **References**: Share `references.bib` with main, or use separate file. Only cited entries appear.
- **Figures**: Put SI figures in `figures/` alongside main figures. No prefix needed — labels handle S-prefix.
- **DOCX-only**: Equation post-processing is DOCX-only. For PDF, LaTeX handles `\tag{S1}` natively.
- **Test after upgrade**: `bash assets/tests/test-render.sh` (run from the skill repository root, not from the user project) to verify `fix-si-numbering.py` with current Pandoc.

## Render & Pre-flight

🔴 **CHECKPOINT**: Before running `quarto render`, present pre-flight summary to researcher. Example: "Pre-flight complete: ✅ CSL correct ✅ template.docx ready ✅ 3 TODOs remaining. Render now?"

```bash
quarto render                    # main manuscript
bash scripts/render-si.sh        # SI (if exists)
```

### Pre-flight checklist

- [ ] `.gitignore` covers `_manuscript/`, `_freeze/`, `_supplementary/`
- [ ] `freeze:` matches phase (`false` editing, `true` final)
- [ ] `lang:` matches journal (all current → `en`)
- [ ] `cite-method` matches journal (PDF only; default `citeproc`; ACS/ES&T → `natbib`). DOCX always uses `citeproc`.
- [ ] CSL + reference-doc from same journal
- [ ] Body language matches `lang:`; mark uncertain segments with `<!-- LANG-CHECK: original -->`
- [ ] Every `[@key]` has matching `references.bib` entry
- [ ] Every `@fig-`/`@tbl-`/`@eq-`/`@sec-` label is unique
- [ ] No `TODO`/`FIXME`/`XXX` remain (unless acknowledged)
- [ ] All figure paths resolve
- [ ] **If SI exists**: `_quarto-si.yml` `project.type` is `default`, `crossref` present
- [ ] **If SI exists**: `bash scripts/render-si.sh` runs without error
- [ ] **If SI exists**: equation numbers show `(S1)` not `(1)`
- [ ] **If SI exists**: cross-refs between main and SI use plain text, not `@fig-`
- [ ] **If SI exists**: every plain-text SI ref in `index.qmd` (e.g. "Supplementary Figure S1") has a matching label `{#fig-...}` in `si.qmd`

### Failure mode fallback

| Trigger condition | First-line fix | If still fails |
|---|---|---|
| `quarto render` exits non-zero | Read error output: missing CSL → copy from `journal-templates/`; missing `template.docx` → copy from `assets/`; Lua filter error → check `scripts/abstract.lua` path | Ask researcher to run `quarto check` and share output |
| CSL file not in `journal-templates/` | Download from [CSL repo](https://github.com/citation-style-language/styles) or [Zotero](https://www.zotero.org/styles); save to project root | Tell researcher: "CSL for {journal} not bundled. I downloaded {file}. Verify citation format in rendered .docx." |
| `fix-si-numbering.py` errors (Python/XML) | Verify Python 3 available (`python3 --version`); check script has no syntax errors | Fall back to manual equation renumbering in DOCX via Word Find/Replace |
| `render-si.sh` fails | Check `_quarto-si.yml` exists and `project.type: default`; ensure `si.qmd` is at project root | Render SI manually: `quarto render si.qmd --output-dir _supplementary` |
| `authors-block` extension missing | Run `quarto add kapsner/authors-block` | If network fails, add authors directly in `index.qmd` YAML without the extension |
| Cross-ref labels collide (`@fig-1` used twice) | Agent must verify labels are unique in pre-flight; rename duplicate with descriptive suffix | Re-render after fix — no silent skip |
| `freeze: true` blocks re-rendering | Set `freeze: false` in `_quarto.yml` | If researcher wants frozen state, run `quarto render --no-freeze` |

### Submission readiness

- [ ] File naming matches journal requirements
- [ ] Figure resolution ≥300 DPI
- [ ] Word/page count within journal limits
- [ ] Required sections present (data availability, author contributions, etc.)
- [ ] CSL matches target journal (verify citation format in .docx)

## Journal Template Index

20 of the 22 CSL files in `journal-templates/` use `cite-method: citeproc` and target language `lang: en`. Two exceptions require `cite-method: natbib`:

| Field | Exception |
|-------|-----------|
| `cite-method: natbib` | ACS, ES&T |
| Non-English `lang:` | (none yet. Set explicitly when adding a non-English journal) |
