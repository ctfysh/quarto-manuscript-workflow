# Scenario F: Adding Supporting Information to an Existing Project

**Researcher:** *"I have a manuscript drafted and also have supplementary materials with extra methods and figures. Can you set up a Supporting Information file?"*

The researcher has a working Quarto manuscript project (such as an output from Scenario A–D). They now need SI.

---

## Initial State

```
project/
├── _quarto.yml              # Main manuscript config (project.type: manuscript)
├── index.qmd                # YAML frontmatter: title, authors, abstract, keywords, filters (authors-block)
├── references.bib
├── template.docx
├── american-chemical-society.csl
├── scripts/
│   └── abstract.lua
├── figures/                 # Contains fig-main.png, fig-setup.png
└── .gitignore
```

`_quarto.yml`:

```yaml
project:
  type: manuscript
manuscript:
  article: index.qmd
lang: en
cite-method: natbib
format:
  docx:
    reference-doc: template.docx
    csl: american-chemical-society.csl
    filters:
      - scripts/abstract.lua
execute:
  freeze: false
bibliography: references.bib
```

`index.qmd` frontmatter:

```markdown
---
title: "Microplastic Characterization in Urban Waterways"
author:
  - name: Alex Chen
    affiliation: City University
    corresponding: true
    email: alex.chen@cityu.edu
  - name: Beth Lee
    affiliation: City University
filters:
  - authors-block
abstract: |
  This study characterizes microplastic pollution in urban waterways.
keywords:
  - microplastics
  - urban waterways
  - polymer characterization
bibliography: references.bib
---
```

The main text already references SI items:

```markdown
## Methods {#sec-methods}

Sample collection followed established protocols (see Supplementary Figure S1
for the sampling site map). Detailed extraction procedures are described in the
[Supplementary Methods](#sec-supp-methods). Polymer identification parameters
are listed in Supplementary Table S1.

## Results

...
```

---

## Step 1: Create `si.qmd`

Pure markdown, zero frontmatter. All configuration goes in the SI project config.

````markdown
# Supporting Information

## Supplementary Methods {#sec-supp-methods}

Samples were collected using a stainless steel grab sampler at 12 sites along
the urban waterway. Each sample was sieved through a 5 mm mesh to remove large
debris, then digested in 30% H₂O₂ at 65 °C for 48 h.

![Sampling site map showing 12 collection points along the urban waterway.](figures/fig-setup.png){#fig-s1}

| Parameter | Instrument | Detection limit |
|-----------|------------|-----------------|
| Particle size | Stereomicroscope | 50 μm |
| Polymer type | μ-FTIR | — |
| Mass | Microbalance | 0.1 mg |
: Instrument parameters for microplastic characterization. {#tbl-s1}

$$ C = \frac{N}{V} $$ {#eq-conc}

## References

::: {#refs}
:::
````

---

## Step 2: Create SI Project Config (`_quarto-si.yml`)

Write at project root. CSL must match the main manuscript's journal.

```yaml
project:
  type: default

title: "Supporting Information"

crossref:
  fig-title: "Figure S"
  tbl-title: "Table S"
  eq-title: "Equation S"

format:
  docx:
    reference-doc: template.docx
    csl: american-chemical-society.csl
    filters:
      - scripts/abstract.lua         # Shared with main — harmless when abstract is absent

bibliography: references.bib
```

**Note**: Metadata (authors, abstract, keywords) is in `index.qmd` frontmatter, not in `_quarto.yml`. This keeps `si.qmd` clean — it's pure markdown with no inherited metadata.

---

## Step 3: Copy Post-Processor Script

```bash
cp <skill-assets>/assets/scripts/fix-si-numbering.py scripts/
```

This script post-processes equation numbers (`(1)` → `(S1)`) and handles caption SEQ field codes (fallback for older Quarto versions). It uses stdlib only (`xml.etree.ElementTree`), no extra packages.

---

## Step 4: Create Render Wrapper (`scripts/render-si.sh`)

Bundle the render and post-processing into one command. The script creates a standalone project in `_supplementary/`, copies in shared assets, renders, and runs the equation-number fix:

```bash
#!/usr/bin/env bash
# render-si.sh — One-command SI render: standalone project + post-processing
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SI_DIR="${PROJECT_DIR}/_supplementary"

mkdir -p "${SI_DIR}"

cp "${PROJECT_DIR}/si.qmd" "${SI_DIR}/"
for asset in template.docx references.bib; do
    [ -f "${PROJECT_DIR}/${asset}" ] && cp "${PROJECT_DIR}/${asset}" "${SI_DIR}/"
done
for f in "${PROJECT_DIR}/"*.csl; do
    [ -f "${f}" ] && cp "${f}" "${SI_DIR}/"
done

sed '/output-dir:/d' "${PROJECT_DIR}/_quarto-si.yml" > "${SI_DIR}/_quarto.yml"
if ! grep -qE '\[@[A-Za-z]' "${SI_DIR}/si.qmd" 2>/dev/null; then
    sed -i '' '/^bibliography:/d; /^    csl:/d' "${SI_DIR}/_quarto.yml"
fi

cd "${SI_DIR}"
quarto render
python3 "${SCRIPT_DIR}/fix-si-numbering.py" si.docx
```

> **Why not `quarto render --profile si`?** When the main project uses `project.type: manuscript`, the profile merge prevents equations from rendering as OMML math objects in the SI DOCX. A standalone subdirectory avoids this issue entirely.

---

## Step 5: Verify Metadata Placement

Check that `_quarto.yml` does NOT contain `authors:`, `abstract:`, or `keywords:`. These must be in `index.qmd` frontmatter only:

```yaml
# ❌ Wrong — metadata in _quarto.yml pollutes the project root:
# _quarto.yml
author:
  - name: Alex Chen
...

# ✅ Correct — scoped to index.qmd, SI is pure markdown:
# index.qmd
---
author:
  - name: Alex Chen
...
---
```

---

## Step 6: Pre-flight Check

- ✅ `si.qmd` exists with SI content and cross-reference labels
- ✅ `_quarto-si.yml` has `project.type: default` (not `manuscript`)
- ✅ `_quarto-si.yml` has `crossref` with S-prefix titles
- ✅ `scripts/fix-si-numbering.py` copied and working
- ✅ `scripts/render-si.sh` created and executable
- ✅ `.gitignore` includes `_supplementary/`
- ✅ Metadata in `index.qmd` frontmatter, not `_quarto.yml`
- ✅ Cross-references between main and SI use plain text (e.g., "Supplementary Figure S1"), not `@fig-s1`
- ✅ Every plain-text SI ref in `index.qmd` has a matching `{#fig-...}` / `{#tbl-...}` label in `si.qmd`

---

## Step 7: Render Both Files

```bash
# Main manuscript
quarto render

# Supporting Information
bash scripts/render-si.sh
```

---

## Result

```
project/
├── _quarto.yml              # Main manuscript config
├── _quarto-si.yml           # SI profile
├── index.qmd                # YAML frontmatter + main text
├── si.qmd                   # Pure markdown SI content
├── scripts/
│   ├── abstract.lua
│   ├── fix-si-numbering.py  # Post-processor for equation S-prefix
│   └── render-si.sh         # One-command SI render
├── figures/
├── _manuscript/
│   └── index.docx           # Main manuscript (Figure 1, Table 1)
├── _supplementary/
│   └── si.docx              # SI (Figure S1, Table S1, Equation S1)
├── template.docx
├── american-chemical-society.csl
├── references.bib
└── .gitignore
```

**Agent:** *"SI is set up. Render with `quarto render` for the main manuscript and `bash scripts/render-si.sh` for the SI. The SI equation numbers are automatically post-processed to show `(S1)` format. Let me know if you need to add more figures or sections to the SI."*
