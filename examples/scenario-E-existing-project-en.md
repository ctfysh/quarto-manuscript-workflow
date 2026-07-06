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
- No `filters:` section → agent adds `abstract.lua` filter
- No `lang:` set → agent adds `lang: en`

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
- *Added abstract.lua filter to _quarto.yml*
- *Added `lang: en` to _quarto.yml*
- *Found and added DOI for Liu 2022 to references.bib*

*⚠️ Issues you need to fix:*
- *`@eq-1`: equation label not found in document*
- *`figures/raw-data.png`: exists but never referenced in text*

*Here's your rendered .docx."*
