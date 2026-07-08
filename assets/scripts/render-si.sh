#!/usr/bin/env bash
# render-si.sh — One-command SI render: profile render + post-processing
set -euo pipefail

quarto render --profile si

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python "${SCRIPT_DIR}/fix-si-numbering.py" _supplementary/si.docx

echo "Done: _supplementary/si.docx"
