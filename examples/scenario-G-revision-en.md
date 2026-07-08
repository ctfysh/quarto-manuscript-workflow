# Scenario: Revision Request — From Reviewer Comments to Revised Manuscript

**Researcher:** *"I got minor revision from Water Research. The reviewers have three requests. Can you revise my manuscript and re-render it?"*

Researcher provides:
- The existing `index.qmd`, `_quarto.yml`, and project files
- The reviewer comments

---

## Step 1: Read Reviewer Comments

Agent reads the comments and maps each to an action:

| # | Comment | Action |
|---|---------|--------|
| 1 | "Figure 2 resolution is too low for publication (needs ≥300 DPI)" | Replace `fig2-concentrations.png` with high-res version |
| 2 | "The Discussion should acknowledge the limitation of sample size (n=6 plants)" | Add one paragraph to Discussion |
| 3 | "Please check that all citation keys match the reference list — I found [@smith2020] in the text but not in references.bib" | Add missing bib entry for Smith 2020 |

---

## Step 2: Apply Edits

Agent edits `index.qmd`:

```diff
 ## Discussion {#sec-discussion}
 
 The removal efficiency of conventional treatment (72.3%) aligns with the limited available literature...
 
+### Limitations
+
+We acknowledge that this study is based on samples from six DWTPs, which may not capture the full
+range of treatment configurations and source water conditions. Future studies with larger sample
+sizes across diverse geographic regions would strengthen the generalizability of these findings.
+Additionally, seasonal variability was not assessed, as sampling was conducted during a single
+summer period; year-round monitoring would provide a more complete picture of microplastic removal dynamics.
+
 ## Conclusion {#sec-conclusion}
```

Agent also:
- Replaces `figures/fig2-concentrations.png` with the high-resolution version provided by the researcher
- Adds `[@smith2020]` entry to `references.bib` (auto-lookup DOI from CrossRef)

---

## Step 3: Pre-flight Check

- [x] `.gitignore` covers `_manuscript/`, `_freeze/`, `_supplementary/`
- [x] `freeze: false` (editing phase — will toggle to `true` for final)
- [x] `lang: en` matches journal
- [x] CSL + reference-doc from same journal (Water Research)
- [x] Body language matches `lang: en`
- [x] Every `[@key]` has matching `references.bib` entry — **Smith 2020 added**
- [x] Every `@fig-`/`@tbl-`/`@eq-`/`@sec-` label is unique
- [x] No `TODO`/`FIXME`/`XXX` remain
- [x] All figure paths resolve — **fig2-concentrations.png replaced with 600 DPI version**
- [x] Figure resolution ≥300 DPI — **confirmed via python3 PIL**

---

## Step 4: Render

```bash
quarto render
```

---

## Step 5: Deliver with Change Log

**Agent:** *"All three reviewer comments have been addressed:*

| # | Change | Status |
|---|--------|--------|
| 1 | Replaced Figure 2 with 600 DPI version | ✅ Done |
| 2 | Added Limitations paragraph to Discussion | ✅ Done |
| 3 | Added Smith 2020 to references.bib | ✅ Done (DOI: 10.1016/j.watres.2020.115853) |

*Your revised manuscript is ready at `_manuscript/index.docx`. The `freeze:` flag is still `false` — set it to `true` before final submission to lock the computation. Let me know if you need to address additional reviewer comments."*
