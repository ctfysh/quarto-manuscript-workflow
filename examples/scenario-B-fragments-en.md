# Scenario B: Fragments, From Scattered Notes to Structured Draft

**Researcher:** *"I have meeting notes, some slides, and email discussions about my lake sediment microplastics study. Can you make a manuscript out of this?"*

Researcher hands over:
- 3 pages of lab meeting notes (hand-written, OCR'd)
- A PowerPoint with 12 slides (methods + results)
- Email thread with co-authors discussing interpretation

---

## Step 1: Classify Fragments

Agent reads each fragment and assigns IMRaD labels:

| Fragment | Source | IMRaD label | Confidence |
|----------|--------|-------------|------------|
| "We sampled 12 lakes across the Yangtze basin..." | Meeting notes | Methods | High |
| "Preliminary data: 45-320 particles/L detected" | Meeting notes | Results | High |
| Slide 3: Sampling site map | PPT | Methods | High |
| Slide 5-8: Polymer composition pie charts | PPT | Results | High |
| "The high proportion of fibers suggests..." | Meeting notes | Discussion | Medium |
| "Jian suggested we also look at sediment cores" | Email thread | Unknown | Low → `<!-- FUZZY -->` |
| "Maybe compare with Zhang 2022 data?" | Email thread | Discussion | Low → `<!-- FUZZY -->` |
| Slide 12: Future work timeline | PPT | Discussion | Medium |

---

## Step 2: Assemble into .qmd

Agent assembles fragments into IMRaD order, preserving uncertain fragments with markers:

```markdown
---
title: "Microplastic Pollution in Lake Sediments: A Case Study from the Yangtze Basin"
author:
  - name: First Author
    corresponding: true
    affiliations:
      - Department of Environmental Science, University of the Yangtze
  - name: Second Author
    affiliations:
      - State Key Laboratory of Lake Science and Environment, Chinese Academy of Sciences
  - name: Corresponding Author
    affiliations:
      - Department of Environmental Science, University of the Yangtze
abstract: |
  <!-- TODO: Write a 150–250 word abstract summarizing the study objectives,
  methods, key findings, and implications. -->
bibliography: references.bib
---

## Introduction {#sec-intro}

<!-- TODO: Introduction — no fragments found for this section, ~500 words needed -->

## Methods {#sec-methods}

We sampled 12 lakes across the Yangtze basin from March to August 2024.
Surface water samples were collected using a manta trawl (330 μm mesh)...

![Sampling sites across the Yangtze basin](figures/sampling-sites.png){#fig-sites}

...methods content continues...

## Results {#sec-results}

Preliminary data showed 45–320 particles per liter across all sampling sites.
The dominant polymer types were:

![Polymer composition by site](figures/polymer-composition.png){#fig-polymers}

Polyethylene (PE) and polypropylene (PP) accounted for >60% of total particles...

## Discussion {#sec-discussion}

The high proportion of fibers detected in all samples is consistent with
wastewater effluent as a major pathway (Browne et al., 2011).

<!-- FUZZY: 'Maybe compare with Zhang 2022 data?' — could also belong in Results.
   Agent placed here based on comparative context. -->

<!-- FUZZY: 'Jian suggested we also look at sediment cores' — unclear if this
   belongs in Methods (future sampling) or Discussion (limitation). -->

## Conclusion {#sec-conclusion}

<!-- TODO: Conclusion — no fragments found for this section, ~200 words needed -->
```

---

## Step 3: Language Normalization

All fragments are in English → no translation needed. But if fragments were in Chinese, agent would detect and translate each block, preserving technical terms and citations.

---

## Step 4: Coverage Report

```
📋 Coverage Report: Lake Sediment Microplastics Manuscript

  Section        | Status | Source
  ---------------|--------|-------------------
  ✅ Title        | filled | from context
  ❌ Abstract    | TODO   | no fragment found
  ❌ Introduction | TODO   | no fragment found
  ✅ Methods     | filled | meeting notes + slides
  ✅ Results     | filled | meeting notes + slides
  ⚠️ Discussion  | partial| 2 fragments + 2 FUZZY
  ❌ Conclusion  | TODO   | no fragment found
  ❌ References  | TODO   | no fragment found
  ❌ Figures     | TODO   | 2 slides extracted, need processing
```

Agent presents all gaps at once (batch questions, not one-at-a-time):

*"I've assembled the manuscript from your materials. Three sections are missing entirely (Abstract, Introduction, Conclusion). Two fragments are marked as `<!-- FUZZY -->`. Could you clarify where they go? Also, do you have DOI links for your references?"*

---

## Step 5: Apply Template + Render

Researcher responds with clarification, agent:
1. Applies ES&T template (the target journal)
2. Runs pre-flight checks
3. Renders

Output: a structured draft with content from fragments, TODO placeholders for gaps.

---

### Generated `_quarto.yml`

After applying the template, a `_quarto.yml` configuration file is generated alongside `index.qmd`:

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
    filters:
      - scripts/abstract.lua          # moves abstract from YAML to manuscript body
  pdf:
    reference-doc: template.docx
    csl: environmental-science-and-technology.csl
    filters:
      - scripts/abstract.lua
    cite-method: natbib

execute:
  freeze: false

bibliography: references.bib
```

> **Note:** The `authors-block` extension requires `quarto add kapsner/authors-block` to be run before the first render, and `filters: [authors-block]` must be added to `index.qmd` frontmatter (not in `_quarto.yml`, to avoid leaking into SI rendering). The `abstract.lua` filter is a custom Lua script that moves the abstract from YAML frontmatter into the manuscript body.
