# Scenario D: Complete Manuscript — Just Format It

**Researcher:** *"Here's my final draft. Please format it for submission to Water Research and send me the .docx."*

Researcher provides: `final-draft.md` (a complete Markdown manuscript)

---

## Step 1: Read and Validate

Agent reads the Markdown file — all sections are present, no TODOs, no gaps:

```
✅ Title: "Occurrence and Removal of Microplastics in Drinking Water Treatment Plants"
✅ Authors: 6 authors with affiliations
✅ Abstract: ~200 words
✅ Introduction: ~800 words
✅ Methods: ~1200 words (sampling, extraction, FTIR analysis)
✅ Results: ~1500 words with 4 figures
✅ Discussion: ~1000 words
✅ Conclusion: ~300 words
✅ References: 42 entries
✅ Figures: 4 embedded references
✅ Supplementary: referenced in text
```

**Agent:** *"Your manuscript looks complete. I'll apply the Water Research template and render it."*

No interview, no TODO blocks, no gap analysis. Skip straight to template.

---

## Step 2: Apply Template

Agent copies `water-research.csl` and `template.docx`, generates `_quarto.yml`:

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
    filters:
      - abstract.lua
execute:
  freeze: true               # final render — freeze
bibliography: references.bib
```

No `authors-block` extension needed if the manuscript already has proper author formatting.

---

## Step 3: Pre-flight Check

- ✅ `.gitignore` set up
- ✅ `freeze: true` (final render)
- ✅ `lang: en` matches
- ✅ `cite-method: citeproc` (Water Research)
- ✅ Body language fully English, no mixed-language content
- ✅ All 4 figure paths resolve to existing files
- ✅ All `[@key]` have matching entries in references
- ✅ No TODO/FIXME/XXX placeholders
- ✅ Figure resolution checked (≥300 DPI)

---

## Step 4: Render

```bash
quarto render
```

---

## Delivery

**Agent:** *"Done. Your manuscript is formatted for Water Research."*

Delivers: `_manuscript/index.docx`

Switching journals later is one command:

**Researcher:** *"Actually, let's submit to Journal of Hazardous Materials instead."*

**Agent:** *"Switching template..."*
1. Copies `journal-of-hazardous-materials.csl` (or downloads if not bundled)
2. Writes `_quarto-journal.yml` with only format overrides
3. Runs pre-flight check
4. Re-renders

New delivery in under a minute.
