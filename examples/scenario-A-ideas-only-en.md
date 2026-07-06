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
├── template.docx            # copied from skill assets
├── nature.csl               # copied from skill journal-templates/
├── abstract.lua             # copied from skill assets
└── .gitignore               # _manuscript/, _freeze/
```

After Step 3, the directory also contains `_extensions/kapsner/authors-block/` (created by `quarto add`).

`index.qmd` is assembled with TODO blocks for every missing section:

```markdown
---
title: "Microplastic Pollution in Freshwater Ecosystems: Sources, Fate, and Ecological Impacts"
author: "<!-- TODO: add author info -->"
date: today
bibliography: references.bib
format:
  docx:
    reference-doc: template.docx
    csl: nature.csl
---

<!-- TODO: Abstract — 150–250 words summarizing scope, key findings, conclusions -->

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

## References {#sec-references}

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
execute:
  freeze: false
bibliography: references.bib
filters:
  - abstract.lua
  - authors-block
```

Then runs `quarto add kapsner/authors-block` to install extension.

---

## Step 4: Pre-flight Check

- ✅ `.gitignore` exists with `_manuscript/` and `_freeze/`
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
