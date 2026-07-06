# Scenario C: Word Draft — From .docx to Journal-Ready .qmd

**Researcher:** *"Here's my manuscript draft in Word. I need it formatted for Environmental Science & Technology."*

Researcher provides: `manuscript-draft.docx`

---

## Step 1: Parse Word Styles

Agent opens the `.docx` and maps Word styles to `.qmd` structure:

```
Word style            →  .qmd element
──────────────────────────────────────
Title                 →  YAML title:
Authors block         →  YAML authors:
Heading 1 "Introduction"    →  ## Introduction {#sec-intro}
Heading 1 "Methods"         →  ## Methods {#sec-methods}
Heading 2 "Study Area"      →  ### Study Area {#sec-study-area}
Heading 2 "Laboratory Analysis" → ### Laboratory Analysis {#sec-lab}
Heading 1 "Results"         →  ## Results {#sec-results}
Heading 1 "Discussion"      →  ## Discussion {#sec-discussion}
Heading 1 "Conclusion"      →  ## Conclusion {#sec-conclusion}
Normal (body text)   →  paragraph text
Inline image         →  ![](figures/fig1.png){#fig-map}
```

---

## Step 2: Extract Figures

Agent finds 5 embedded images in the Word file, extracts them:

```
figures/
├── fig1-map.png
├── fig2-concentrations.png
├── fig3-polymer-distribution.png
├── fig4-sediment-profile.png
└── fig5-comparison.png
```

Each image gets a `@fig-` label mapped from the Word caption.

---

## Step 3: Identify Citations

Agent scans for inline citations in the text:

| In-text | Action |
|---------|--------|
| `(Smith et al., 2020)` | Search DOI → add to `references.bib` |
| `(Zhang & Li, 2021)` | Search DOI → add to `references.bib` |
| `(Kumar et al., 2019)` | Search DOI → add to `references.bib` |
| `(Wang, 2022)` | DOI not found → mark `<!-- TODO: find DOI for Wang 2022 -->` |

Citations are converted to `[@smith2020]`, `[@zhang2021]`, etc.

---

## Step 4: Build .qmd

Agent generates the full `index.qmd`:

```markdown
---
title: "Microplastic Distribution in Yangtze River Sediments"
author:
  - name: Wei Zhang
    affiliation: Nanjing University
abstract: |
  <!-- TODO: extract or write abstract -->
format:
  docx:
    reference-doc: template.docx
    csl: environmental-science-and-technology.csl
bibliography: references.bib
lang: en
---

## Introduction {#sec-intro}

Microplastic pollution in freshwater systems has emerged as a major
environmental concern [@smith2020]. Unlike marine environments, the
distribution and fate of microplastics in river sediments remain poorly
characterized [@zhang2021]...

...body text continues...

## Methods {#sec-methods}

### Study Area {#sec-study-area}

Sediment samples were collected from 15 sites along the Yangtze River...

### Laboratory Analysis {#sec-lab}

Samples were processed using density separation and FTIR spectroscopy...

## Results {#sec-results}

Microplastic concentrations ranged from 120 to 850 particles per kg of dry
sediment (Fig. 1).

![Sampling sites and microplastic concentrations](figures/fig1-map.png){#fig-map}

![Polymer composition across sites](figures/fig3-polymer-distribution.png){#fig-polymers}

## Discussion {#sec-discussion}

The concentrations observed in this study are comparable to those reported
in the Pearl River [@wang2022 <!-- TODO: verify DOI -->]...

## Conclusion {#sec-conclusion}

...

## References {#sec-references}
```

---

## Step 5: IMRaD Check

Agent flags what's missing:

```
✅ Introduction  — present
✅ Methods       — present (Study Area + Lab Analysis complete)
✅ Results       — present (3 figures referenced)
✅ Discussion    — present
✅ Conclusion    — present but brief (~80 words)
❌ Abstract      — missing, marked as TODO
```

---

## Step 6: Apply ES&T Template + Render

```
✅ _quarto.yml generated with ES&T config
✅ cite-method: natbib (ES&T exception)
✅ abstract.lua filter configured
✅ authors-block extension installed
✅ figures/ directory exists with 5 extracted images
✅ references.bib with 3 entries (1 TODO for Wang 2022)
```

```bash
quarto render
```

Output: formatted `.docx` with ES&T citation style, all figures placed, ready for submission.
