# Scenario D: Complete Manuscript, Just Format It

**Researcher:** *"Here's my final draft. Please format it for submission to Water Research and send me the .docx."*

Researcher provides: `final-draft.md` (a complete Markdown manuscript)

---

## Step 1: Read and Validate

Agent reads the Markdown file. All sections are present, with no TODOs or gaps:

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

The manuscript is complete, so the agent skips the interview and gap analysis and applies the template directly.

---

## Step 2: Apply Template

Agent copies `water-research.csl` and `template.docx`, generates `index.qmd` and `_quarto.yml`:

### Agent generates `index.qmd`:

```qmd
---
title: "Occurrence and Removal of Microplastics in Drinking Water Treatment Plants"
author:
  - name: Alice M. Chen
    corresponding: true
    affiliations:
      - Department of Environmental Engineering, University of Science and Technology
  - name: Bo Liu
    affiliations:
      - Department of Environmental Engineering, University of Science and Technology
  - name: Carolina S. Rodriguez
    affiliations:
      - Water Quality Research Laboratory, National Institute of Water Research
  - name: Daiki Tanaka
    affiliations:
      - Department of Environmental Engineering, University of Science and Technology
  - name: Elena V. Petrova
    affiliations:
      - Analytical Chemistry Division, Institute of Environmental Chemistry
  - name: Feng Wei
    affiliations:
      - Municipal Water Treatment Authority, City Water Supply Bureau
abstract: |
  Microplastics have emerged as contaminants of concern in freshwater systems, yet limited data exist on their occurrence and removal across full-scale drinking water treatment plants (DWTPs). Here we investigated the abundance, morphology, polymer composition, and size distribution of microplastics in raw and treated water from six DWTPs employing different treatment trains. Microplastic particles were detected in all raw water samples at concentrations ranging from 1,250 to 4,800 particles m^−3^. Conventional treatment processes (coagulation–flocculation, sedimentation, and sand filtration) achieved an average removal efficiency of 72.3%, while advanced treatment incorporating ozonation and granular activated carbon filtration increased removal to 94.7%. The predominant polymers identified by Fourier-transform infrared spectroscopy were polyethylene, polypropylene, and polystyrene, accounting for 78.6% of all particles. Fibers and fragments were the most common morphologies, and particles smaller than 100 μm constituted over 60% of the total count. These findings demonstrate that while conventional DWTPs substantially reduce microplastic loads, advanced processes are required to approach complete removal, highlighting the need for upgraded treatment infrastructure in regions reliant on surface water sources.
bibliography: references.bib
---

# Introduction

Microplastic pollution has become recognized as a pervasive environmental threat, with particles detected in marine, freshwater, and terrestrial ecosystems worldwide [@koelmans2019; @ivleva2023]. Concerns over potential human health risks associated with microplastic ingestion and inhalation have driven growing interest in understanding the occurrence of these particles in drinking water [@danopoulos2020; @cox2019]. Although numerous studies have documented microplastic contamination in surface waters and wastewater effluents [@eerkes2015], comparatively less attention has been paid to their fate within drinking water treatment plants (DWTPs) [@novotna2019].

The efficiency of conventional water treatment processes—coagulation, flocculation, sedimentation, and granular media filtration—in removing microplastic particles remains incompletely characterized. Reported removal efficiencies range from 50% to 90%, varying with particle size, polymer type, and process configuration [@wang2020; @pivokonsky2018]. Advanced treatment processes such as ozonation, activated carbon adsorption, and membrane filtration may enhance microplastic removal, but quantitative data from full-scale facilities are scarce [@poerio2023].

In this study, we conducted a comprehensive investigation of microplastic occurrence and removal across six full-scale DWTPs representing diverse treatment configurations. Our objectives were to (i) characterize microplastic abundance, morphology, polymer composition, and size distribution in both raw and treated water, (ii) quantify the removal efficiency of individual treatment processes, and (iii) identify operational parameters that influence removal performance.

# Methods

## Sample Collection

Grab samples of raw water and treated water were collected from six DWTPs located in three river basins during July–September 2024. At each plant, 50 L of raw water and 100 L of treated water were collected in triplicate using stainless steel containers pre-rinsed with ultrapure water. Samples were transported to the laboratory at 4 °C and processed within 24 h of collection.

## Microplastic Extraction and Identification

Water samples were sequentially filtered through 500 μm, 100 μm, and 20 μm stainless steel mesh sieves. Retained material was subjected to wet peroxide oxidation (30% H2O2 at 60 °C for 48 h) to remove organic matter, followed by density separation using a NaCl solution (1.2 g cm^−3^). The supernatant was filtered onto 0.45 μm polycarbonate membrane filters for analysis.

Particle identification and polymer characterization were performed using a Fourier-transform infrared (FTIR) microscope (Thermo Nicolet iN10 MX) operating in reflection mode. Spectra were acquired in the range of 4,000–650 cm^−1^ at 8 cm^−1^ resolution with 32 co-added scans. A spectral library search was conducted against a database of polymer reference spectra; matches with a hit quality index ≥ 0.70 were accepted.

## Quality Assurance and Quality Control

All laboratory procedures were conducted under a laminar flow hood to minimize airborne contamination. Cotton lab coats and nitrile gloves were worn at all times. Procedural blanks (ultrapure water processed identically to samples) were analyzed with every batch of ten samples. No microplastic particles were detected in any of the procedural blanks.

# Results

## Microplastic Abundance in Raw Water

Microplastic particles were detected in all raw water samples, with concentrations ranging from 1,250 to 4,800 particles m^−3^ across the six DWTPs (Figure 1). The highest concentrations were observed in plants drawing water from rivers receiving urban runoff and industrial discharges, whereas plants supplied by reservoir water exhibited significantly lower burdens (p < 0.01, one-way ANOVA).

## Removal Efficiency by Treatment Stage

Figure 2 presents microplastic concentrations at successive stages of treatment. Coagulation–flocculation and sedimentation removed 58.7 ± 9.3% of particles, primarily through enmeshment in settling flocs. Rapid sand filtration achieved an additional 31.6 ± 6.8% removal of particles that passed sedimentation. Overall, conventional treatment (coagulation, sedimentation, and sand filtration) attained an average removal of 72.3%.

Plants equipped with ozonation followed by granular activated carbon (GAC) filtration reached a mean removal efficiency of 94.7% (Figure 3). Ozonation alone contributed a 39.8% reduction, likely through surface oxidation altering particle buoyancy, while subsequent GAC filtration captured the majority of remaining particles.

## Particle Morphology and Polymer Composition

Fibers constituted 47.2% of all identified particles, followed by fragments (35.8%), films (10.3%), and spheres (6.7%) (Figure 4). Polymer composition determined by FTIR was dominated by polyethylene (36.1%), polypropylene (24.5%), and polystyrene (18.0%). Polyamide (9.2%), polyester (7.8%), and other polymers (4.4%) were also detected.

Particles smaller than 100 μm represented 63.4% of the total microplastic count, highlighting the importance of analytical methods capable of detecting micron-sized particles.

# Discussion

The microplastic concentrations in raw water observed here are consistent with previous studies of surface water sources [@koelmans2019; @eerkes2015]. The spatial variation across DWTPs underscores the influence of land use and hydrological context on microplastic loading to drinking water intakes.

The removal efficiency of conventional treatment (72.3%) aligns with the limited available literature [@wang2020; @pivokonsky2018] and confirms that standard coagulation–filtration processes can reduce but not eliminate microplastic contamination. The substantial improvement achieved by adding ozonation and GAC filtration suggests that oxidative and adsorptive mechanisms complement physical removal. These findings align with recent pilot-scale work [@poerio2023] and provide crucial field-scale validation.

The predominance of polyethylene and polypropylene reflects their high production volumes and widespread use in packaging, while the abundance of fibers suggests contributions from textile washing and atmospheric deposition [@ivleva2023]. The dominance of small particles (<100 μm) is of particular concern, as these are more likely to bypass remaining treatment barriers and may pose greater health risks if ingested [@danopoulos2020].

# Conclusion

This study demonstrates that microplastics are ubiquitous in raw water sources supplying DWTPs and that treatment processes vary considerably in removal efficacy. Conventional treatment removes approximately three-quarters of microplastic particles, but advanced processes including ozonation and GAC filtration are necessary to approach complete removal. These findings support the adoption of multi-barrier treatment strategies and provide a scientific basis for upgrading DWTPs in regions vulnerable to microplastic contamination.

# References

::: {#refs}
:::
```

### Agent generates `_quarto.yml`:

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
  pdf:                       # also configures PDF output
    csl: water-research.csl
execute:
  freeze: true               # final render — freeze
bibliography: references.bib
filters:
  - abstract.lua
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

The new delivery is produced in under a minute.
