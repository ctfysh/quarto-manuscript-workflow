# Scenario A: Ideas Only, From Topic to Scaffold

**Researcher:** *"I want to write a review on microplastics in aquatic ecosystems for Nature."*

---

## Step 1: Structured Interview (2 questions)

**Agent:** "Sure. Two questions:

1. **Title?** A working title is fine, it can change later.
2. **Sections?** Standard IMRaD, or do you have a specific outline in mind?"

**Researcher:** *"Title: 'Microplastic Pollution in Freshwater Ecosystems: Sources, Fate, and Ecological Impacts'. Standard IMRaD is fine."*

---

## Step 2: Scaffold Project

Agent creates the project directory with initial structure:

```
microplastics-review/
├── _quarto.yml              # project config + Nature template
├── index.qmd                # article source with TODO blocks
├── references.bib           # empty, bib entries to be added
├── figures/                 # empty, figures to be added
├── scripts/
│   └── abstract.lua         # copied from skill assets
├── template.docx            # copied from skill assets
├── nature.csl               # copied from skill journal-templates/
└── .gitignore               # _manuscript/, _freeze/, _supplementary/
```

After Step 3, the directory also contains `_extensions/kapsner/authors-block/` (created by `quarto add`).

`index.qmd` is assembled with TODO blocks for every missing section:

```markdown
---
title: "Microplastic Pollution in Freshwater Ecosystems: Sources, Fate, and Ecological Impacts"
author:
  - name: "First Author"  # TODO: replace with actual author info
    affiliation: "University"
    corresponding: true
  - name: "Second Author"  # TODO: replace with actual author info
    affiliation: "University"
date: today
abstract: |
  <!-- TODO: Abstract — 150–250 words summarizing scope, key findings, conclusions -->
filters:
  - authors-block                # author affiliations extension
bibliography: references.bib
---

## Introduction {#sec-intro}

<!-- TODO: Introduction (~500 words)
  - Background on plastic production and environmental release
  - Definitions: primary vs secondary microplastics
  - Known ecological impacts in marine systems
  - Gap: freshwater ecosystems understudied compared to marine
  - Thesis: this review synthesizes current knowledge on freshwater microplastics -->

## Methods {#sec-methods}

<!-- TODO: Methods (~300 words)
  - Literature search strategy (databases, keywords, inclusion/exclusion criteria)
  - Study selection process (PRISMA flow diagram @fig-prisma)
  - Data extraction approach -->

## Results {#sec-results}

<!-- TODO: Results section (~1000 words)
  - Occurrence and distribution across freshwater systems
  - Sources and pathways
  - Ecological effects on freshwater organisms
  - Tables summarizing key studies (@tbl-studies) -->

## Discussion {#sec-discussion}

<!-- TODO: Discussion (~600 words)
  - Synthesis of main findings
  - Comparison with marine microplastic literature
  - Knowledge gaps and future research directions
  - Methodological challenges -->

## Conclusion {#sec-conclusion}

<!-- TODO: Conclusion (~200 words)
  - Summary of key findings
  - Implications for policy and management
  - Urgent research needs -->

# References

<!-- TODO: add references -->
```

---

## Step 3: Apply Nature Template

Agent generates `_quarto.yml`:

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
      - scripts/abstract.lua          # moves abstract from YAML to manuscript body
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

Then:
- Runs `quarto add kapsner/authors-block` to install extension
- Adds `filters: [authors-block]` to `index.qmd` frontmatter (not in `_quarto.yml`, to keep the filter scoped to the article, not the project config)

---

## Step 4: Pre-flight Check

- ✅ `.gitignore` exists with `_manuscript/`, `_freeze/`, and `_supplementary/`
- ✅ `freeze: false` (editing phase)
- ✅ `lang: en` matches Nature (English journal)
- ✅ `cite-method: citeproc` (Nature, not in exception list)
- ✅ CSL and reference-doc consistent
- ✅ Body language matches `lang: en` (TODO blocks are English)

---

## Step 5: Render

```bash
quarto render
```

Output: `_manuscript/index.docx` with Nature citation formatting, Nature-appropriate typography, and TODO blocks visible as HTML comments in the rendered document.

---

## Delivery

Agent presents the `.docx` and a coverage report:

```
✅ Project scaffolded with Nature template
✅ Ready for editing at microplastics-review/index.qmd

📋 Gaps to fill:
  🔴 Title authors   → missing
  🟡 Abstract        → TODO in index.qmd
  🟡 Introduction    → TODO in index.qmd
  🟡 Methods         → TODO in index.qmd
  🟡 Results         → TODO in index.qmd
  🟡 Discussion      → TODO in index.qmd
  🟡 Conclusion      → TODO in index.qmd
  🟡 References      → TODO in references.bib
  🟡 Figures         → place in figures/
```

Researcher can now fill in the TODOs and ask the agent to re-render at any time.
