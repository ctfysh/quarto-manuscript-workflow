# Scenario C: Word Draft, From .docx to Journal-Ready .qmd

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

Agent generates the full `index.qmd` (format configuration goes in `_quarto.yml`):

```markdown
---
title: "Microplastic Distribution in Yangtze River Sediments"
author:
  - name: Wei Zhang
    affiliation: Nanjing University
    corresponding: true
abstract: |
  <!-- TODO: extract or write abstract -->
bibliography: references.bib
---

## Introduction {#sec-intro}

Microplastic pollution in freshwater systems has emerged as a major
environmental concern [@smith2020]. Unlike marine environments, the
distribution and fate of microplastics in river sediments remain poorly
characterized [@zhang2021]. Previous studies have documented microplastic
abundance in several major Chinese rivers, yet the Yangtze River—the longest
river in Asia—remains underrepresented in the literature. Understanding the
spatial distribution, polymer composition, and potential sources of
microplastics in Yangtze sediments is critical for assessing the ecological
risks to freshwater biota and informing targeted pollution control strategies.

## Methods {#sec-methods}

### Study Area {#sec-study-area}

Sediment samples were collected from 15 sites spanning approximately 1,200 km
along the middle and lower reaches of the Yangtze River, from Yichang to
Shanghai. At each site, triplicate surface sediment samples (0–5 cm depth)
were obtained using a Van Veen grab sampler during the dry season
(November–December 2022). Sampling locations were selected to represent
diverse land-use contexts, including urban, agricultural, and industrial
areas, to capture a comprehensive picture of microplastic pollution across
the river basin.

### Laboratory Analysis {#sec-lab}

Microplastics were extracted from sediment using density separation with a
sodium chloride solution (1.2 g cm⁻³), followed by wet peroxide oxidation to
remove natural organic matter. Particles were visually identified and sorted
under a stereomicroscope, then polymer characterization was performed using
Fourier-transform infrared spectroscopy (FTIR) in attenuated total reflectance
(ATR) mode. Each particle was categorized by shape (fiber, fragment, film,
sphere), color, and polymer type.

## Results {#sec-results}

Microplastic concentrations ranged from 120 to 850 particles per kg of dry
sediment (Fig. 1).

![Sampling sites and microplastic concentrations](figures/fig1-map.png){#fig-map}

![Polymer composition across sites](figures/fig3-polymer-distribution.png){#fig-polymers}

Polyethylene (PE) and polypropylene (PP) were the dominant polymer types,
accounting for 42% and 28% of total particles, respectively, suggesting that
packaging and agricultural films are major sources. Fibers constituted the
most common shape across all sites (mean 54%), followed by fragments (31%)
and films (11%). No significant correlation was found between microplastic
abundance and sediment grain size, indicating that factors such as
hydrodynamic conditions and proximity to urban centers play a more important
role in microplastic deposition.

## Discussion {#sec-discussion}

The concentrations observed in this study are comparable to those reported
in the Pearl River [@wang2022] and the Danube River [@kumar2019], suggesting
that microplastic contamination in large river systems follows broadly
similar accumulation patterns driven by urbanization and industrial activity.

## Conclusion {#sec-conclusion}

This study provides a comprehensive assessment of microplastic contamination
in Yangtze River sediments, revealing widespread pollution with concentrations
ranging from 120 to 850 particles per kg of dry sediment. Polyethylene and
polypropylene dominated the polymer profile, implicating packaging and
agricultural sources as primary contributors. These findings establish a
critical baseline for future monitoring efforts and underscore the need for
standardized analytical protocols to enable meaningful comparisons across
freshwater ecosystems globally.

## References {#sec-references}

::: {#refs}
:::
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
    csl: environmental-science-and-technology.csl
  pdf:
    csl: environmental-science-and-technology.csl
    cite-method: natbib               # ES&T exception
execute:
  freeze: false
bibliography: references.bib
filters:
  - abstract.lua
  - authors-block
```

Then runs `quarto add kapsner/authors-block` to install the extension, creating `_extensions/kapsner/authors-block/`.

```
✅ figures/ directory exists with 5 extracted images
✅ references.bib with 3 entries (1 TODO for Wang 2022)
```

With the extension installed and the project configured, the agent renders the manuscript:

```bash
quarto render
```

Output: formatted `.docx` with ES&T citation style, all figures placed, ready for submission.
