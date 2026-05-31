# Quarto Manuscript Workflow

A superpowers skill for **agent-mediated manuscript production**. Researchers provide materials (notes, Word drafts, Markdown files, figures); the AI agent assembles them into a formatted journal-ready manuscript. Researchers never write .qmd syntax or run commands.

## Quick Start

1. Invoke this skill
2. Provide your materials to the agent (notes, Word, Obsidian exports, figures)
3. Agent assembles, applies journal template, renders
4. Receive your .docx

## Included Journal Templates (22)

**Style-based:** ACS, APA, Nature, Elsevier (Harvard), Elsevier (Vancouver), Wiley, Springer, Taylor & Francis, IEEE, Chicago (CMOS), MLA

**Environmental/Ecology:** Water Research, Environmental Science & Technology (ES&T), Journal of Hydrology, Science of the Total Environment (STOTEN), Ecology (ESA), Global Change Biology, Geophysical Research Letters (GRL/AGU), Biogeosciences, Limnology and Oceanography (L&O), Journal of Environmental Management (JEMA), Journal of Cleaner Production (JCP)

## Adding a New Journal

1. Create `journal-templates/<name>/`
2. Add `_quarto-journal.yml` with format config
3. Add `<name>.csl` with citation style
4. Add `template.docx` with Word reference template

## Requirements

- Quarto ≥1.3
- LaTeX (for PDF output)
