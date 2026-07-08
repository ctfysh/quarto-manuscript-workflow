# Scenario E: Existing Quarto Project, QA and Fix

**Researcher:** *"I've been writing in Quarto directly. Can you check if everything is set up correctly and render it?"*

Researcher provides: an existing Quarto project directory.

---

## Step 1: Verify `_quarto.yml`

Agent reads the project config and checks:

```yaml
project:
  type: manuscript               # ✅ correct
manuscript:
  article: index.qmd             # ✅ file exists
format:
  docx:
    reference-doc: template.docx # ⚠️ referenced but not in project root
    csl: nature.csl              # ⚠️ referenced but not in project root
execute:
  freeze: false                  # ✅ editing phase
bibliography: references.bib     # ✅ file exists
```

**Issues found:**
- `template.docx` and `nature.csl` are referenced but don't exist in the project directory → agent copies them from the skill's assets
- No `filters:` section → agent copies `abstract.lua` to `scripts/abstract.lua` and adds `scripts/abstract.lua` filter
- No `lang:` set → agent adds `lang: en`

### Agent applies fixes:

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
format:
  docx:
    reference-doc: template.docx
    csl: nature.csl
    filters:
      - scripts/abstract.lua
lang: en
execute:
  freeze: false
bibliography: references.bib
```

No `authors-block` extension needed since the existing project already has proper author formatting.

## Researcher's `index.qmd`:

```markdown
---
title: "Microplastic Contamination in Freshwater Environments: A Comprehensive Assessment"
author:
  - name: "Wei Chen"
    affiliations: "Department of Environmental Science, East China University"
    corresponding: true
  - name: "Sarah Johnson"
    affiliations: "Institute of Water Research, University of California"
abstract: |
  Microplastic pollution has emerged as a pervasive environmental threat to freshwater ecosystems worldwide. Here we present a comprehensive assessment of microplastic contamination across 15 freshwater sites in eastern China, combining field sampling, spectroscopic characterization, and ecological risk modeling. Our results reveal widespread contamination with mean abundances of 1,850 ± 420 particles per cubic meter, predominantly consisting of polyethylene and polypropylene fibers. We identify significant correlations between microplastic abundance and upstream industrial activity, and estimate regional ecological risk indices ranging from moderate to high. These findings underscore the urgent need for standardized monitoring protocols and targeted mitigation strategies for freshwater microplastic pollution.
bibliography: references.bib
---

## Introduction

Microplastic pollution, defined as plastic particles smaller than 5 mm in diameter, has become one of the most pressing environmental challenges of the Anthropocene [@liu2022]. While initial research focused on marine environments, growing evidence suggests that freshwater systems may act as significant conduits for microplastic transport from terrestrial sources to oceanic sinks. Rivers, lakes, and reservoirs receive microplastic inputs from wastewater effluent, urban runoff, industrial discharge, and atmospheric deposition, yet comprehensive assessments of freshwater contamination remain limited compared to marine studies.

Spatial patterns of microplastic distribution are strongly influenced by proximity to urban and industrial areas @fig-sampling. However, standardized methodologies for sampling, extraction, and identification are still lacking, making cross-study comparisons challenging.

## Methods {#sec-methods}

### Sampling Protocol

Water samples were collected from 15 sites along the Yangtze River Delta region between March and June 2026. At each site, triplicate surface water samples (50 L each) were collected using a stainless-steel bucket and passed through a 300 μm stainless-steel sieve. Retained materials were rinsed into glass jars and transported to the laboratory at 4°C.

### Laboratory Analysis

Microplastic extraction followed a density separation protocol using a saturated NaCl solution (1.2 g/cm³), followed by filtration through 0.45 μm glass fiber filters. Particles were visually identified under a stereomicroscope and chemically characterized using Fourier-transform infrared spectroscopy (FTIR) in attenuated total reflectance mode.

### Statistical Analysis

Ecological risk assessment was performed using the Polymer Hazard Index (PHI) and the Potential Ecological Risk Index (PERI), following established methodologies. Correlation analyses between microplastic abundance and land-use variables were conducted using Spearman's rank correlation.

## Results

A total of 8,325 suspected microplastic particles were identified across all sampling sites, with mean abundances of 1,850 ± 420 particles per cubic meter @fig-results. The highest concentrations were observed at Site YZ-07 (3,210 particles/m³), located approximately 2 km downstream from a major textile manufacturing zone, while the lowest were recorded at Site YZ-15 (420 particles/m³), a protected wetland area.

| Polymer Type | Abundance (%) | Mean Size (μm) | PHI Score |
|:---|---:|---:|---:|
| Polyethylene | 42.3 | 820 ± 310 | 11 |
| Polypropylene | 28.7 | 650 ± 280 | 4 |
| Polystyrene | 12.5 | 440 ± 190 | 30 |
| Polyester | 9.8 | 510 ± 220 | 425 |
| Other | 6.7 | 560 ± 250 | — |

: Polymer composition, size distribution, and hazard scores for microplastics detected across all sampling sites {#tbl-comparison}

The relationship between microplastic abundance and distance to industrial zones followed a logarithmic decay model (R² = 0.87, @eq-1). Ecological risk assessment using the PERI framework classified 6 of 15 sites as high-risk, with PHI values dominated by polyester fibers despite their relatively low abundance.

## Discussion

Our findings demonstrate that freshwater microplastic contamination in the Yangtze River Delta region is both pervasive and ecologically significant. The dominance of polyethylene and polypropylene fibers aligns with global production volumes and textile industry discharges prevalent in the region. The identification of polyester as the primary driver of ecological hazard scores, despite its lower abundance, highlights the importance of polymer-specific risk assessment.

The strong correlation between microplastic abundance and proximity to industrial zones underscores the role of point-source pollution in freshwater contamination. However, the widespread distribution of microplastics even at remote sites suggests significant atmospheric transport and diffuse pollution pathways that warrant further investigation.

## Conclusion

This study provides the first comprehensive assessment of microplastic contamination across the Yangtze River Delta freshwater system. Our results establish baseline contamination levels, identify key polymer-specific risk drivers, and demonstrate the utility of integrated risk assessment frameworks for freshwater microplastic pollution. Future work should focus on seasonal dynamics, biological uptake, and the development of standardized monitoring protocols to support regulatory action.

## References
```

---

## Step 2: Check Cross-References

Agent scans `index.qmd` for all `@` references and validates:

```
References in document:
  @fig-sampling    → ✅ figures/sampling-map.png exists
  @fig-results     → ✅ figures/results-overview.png exists
  @tbl-comparison  → ✅ pipe table found in Results section
  @sec-methods     → ✅ ## Methods section found
  @eq-1            → ❌ no equation labeled {#eq-1}
  @liu2022         → ❌ no entry in references.bib for liu2022
```

**Issues found:**
- `@eq-1` is broken: equation missing or label wrong
- `@liu2022` is missing from bibliography

Agent fixes what it can (adds bib entry from DOI search) and reports what needs manual attention.

---

## Step 3: Check Figures

```
figures/
├── sampling-map.png       → ✅ 600 DPI, referenced
├── results-overview.png   → ✅ 300 DPI, referenced
└── raw-data.png           → ⚠️ exists but not referenced in text
```

---

## Step 4: Language Check

Agent detects the manuscript body is fully in English → ✅ matches `lang: en`.

---

## Step 5: Pre-flight Check

- ✅ `.gitignore` exists
- ✅ `freeze: false` (editing phase)
- ✅ `lang: en` matches
- ✅ `cite-method: citeproc` (was unset → default applied)
- ✅ CSL and reference-doc now available
- ⚠️ `@eq-1` cross-reference broken → flagged for user
- ⚠️ `@liu2022` bibliography entry added via DOI lookup
- ⚠️ `raw-data.png` unreferenced → flagged

---

## Step 6: Render

```bash
quarto render
```

---

## Delivery

**Agent:** *"Your project is now set up correctly and rendered. Issues I fixed:*

- *Added missing template.docx and nature.csl to project root*
- *Created scripts/ directory and added scripts/abstract.lua filter to _quarto.yml*
- *Added `lang: en` to _quarto.yml*
- *Found and added DOI for Liu 2022 to references.bib*

*⚠️ Issues you need to fix:*
- *`@eq-1`: equation label not found in document*
- *`figures/raw-data.png`: exists but never referenced in text*

*Here's your rendered .docx."*
