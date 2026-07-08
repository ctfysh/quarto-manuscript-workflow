#!/usr/bin/env bash
# render-si.sh — One-command SI render: standalone project + post-processing
#
# Why standalone instead of --profile si?
#   Quarto's profile mechanism (--profile si) merges _quarto-si.yml on top
#   of _quarto.yml. When the main project uses project.type: manuscript,
#   this merge prevents equations from rendering as OMML math objects in
#   the SI DOCX output — they appear as plain text with field codes instead.
#   A standalone subdirectory with its own _quarto.yml (project.type: default)
#   avoids this issue entirely.
#
# Usage:
#   Place at project/scripts/render-si.sh, then run from project root:
#     bash scripts/render-si.sh
#
# Expected project structure:
#   project/
#   ├── _quarto.yml                 # Main manuscript (project.type: manuscript)
#   ├── _quarto-si.yml              # → copied as _supplementary/_quarto.yml
#   ├── index.qmd                   # Main manuscript
#   ├── si.qmd                      # Pure markdown, no frontmatter
#   ├── american-chemical-society.csl
#   ├── template.docx
#   ├── references.bib
#   ├── scripts/
#   │   ├── abstract.lua
#   │   ├── fix-si-numbering.py
#   │   └── render-si.sh            # THIS FILE
#   └── _supplementary/             # created by this script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SI_DIR="${PROJECT_DIR}/_supplementary"

# ---- Step 1: Create standalone SI project ----
mkdir -p "${SI_DIR}"

# Check si.qmd exists
if [ ! -f "${PROJECT_DIR}/si.qmd" ]; then
    echo "ERROR: si.qmd not found in ${PROJECT_DIR}"
    echo "Create si.qmd before running render-si.sh"
    exit 1
fi

# Copy si.qmd (not symlink — avoids path resolution issues)
cp "${PROJECT_DIR}/si.qmd" "${SI_DIR}/"

# Copy/link shared assets into _supplementary/ so references resolve
for asset in template.docx references.bib; do
    if [ -f "${PROJECT_DIR}/${asset}" ]; then
        if ! ln -sf "${PROJECT_DIR}/${asset}" "${SI_DIR}/${asset}" 2>/dev/null; then
            cp "${PROJECT_DIR}/${asset}" "${SI_DIR}/"
        fi
    fi
done

# Copy/link any CSL files
for csl_file in "${PROJECT_DIR}/"*.csl; do
    if [ -f "${csl_file}" ]; then
        if ! ln -sf "${csl_file}" "${SI_DIR}/$(basename "${csl_file}")" 2>/dev/null; then
            cp "${csl_file}" "${SI_DIR}/"
        fi
    fi
done

# Copy/link abstract.lua if it exists
if [ -f "${PROJECT_DIR}/scripts/abstract.lua" ]; then
    mkdir -p "${SI_DIR}/scripts"
    if ! ln -sf "${PROJECT_DIR}/scripts/abstract.lua" "${SI_DIR}/scripts/abstract.lua" 2>/dev/null; then
        cp "${PROJECT_DIR}/scripts/abstract.lua" "${SI_DIR}/scripts/"
    fi
fi

# ---- Step 2: Create SI config ----
if [ -f "${PROJECT_DIR}/_quarto-si.yml" ]; then
    sed '/output-dir:/d' "${PROJECT_DIR}/_quarto-si.yml" > "${SI_DIR}/_quarto.yml"
    if ! grep -qE '\[@' "${SI_DIR}/si.qmd" 2>/dev/null; then
        sed -i '' '/^bibliography:/d; /csl:/d' "${SI_DIR}/_quarto.yml"
    fi
else
    echo "ERROR: _quarto-si.yml not found in ${PROJECT_DIR}"
    echo "Create it from the skill template before running render-si.sh"
    exit 1
fi

# ---- Step 3: Render ----
(cd "${SI_DIR}" && quarto render)

# ---- Step 4: Post-process ----
SI_DOCX="${SI_DIR}/si.docx"
if [ -f "${SI_DOCX}" ]; then
    python3 "${SCRIPT_DIR}/fix-si-numbering.py" "${SI_DOCX}"
    echo "Done: ${SI_DOCX}"
else
    echo "ERROR: SI output not found at ${SI_DOCX}"
    echo "Check _supplementary/ for rendered files."
    exit 1
fi
