#!/usr/bin/env bash
# test-render.sh — Render test QMD, run fix, verify equation numbers
#
# Usage:
#   bash assets/tests/test-render.sh
#
# When Pandoc changes the OMML output:
#   1. This test will fail (fix will error out)
#   2. Add a new pattern in assets/scripts/fix-si-numbering.py
#   3. Update this script's verification if needed
#
# Dependencies: quarto, python3

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_DIR="${SKILL_DIR}/assets/tests"
SCRIPT="${SKILL_DIR}/assets/scripts/fix-si-numbering.py"
OUTPUT_FILE="_test_output/test-equation.docx"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

cleanup() { rm -rf "${TEST_DIR}/_test_output"; }
trap cleanup EXIT

# ---- 1. Render ----
echo "============================================"
echo " quarto-manuscript-workflow — SI test suite"
echo "============================================"
echo ""

rm -rf "${TEST_DIR}/_test_output"

echo "[1/4] Rendering test-equation.qmd → DOCX ..."
cd "${TEST_DIR}"
quarto render test-equation.qmd 2>&1 | tail -2
echo ""

if [ ! -f "${OUTPUT_FILE}" ]; then
    echo -e "${RED}✘ FAIL${NC} Render produced no output."
    exit 1
fi

# ---- 2. Run fix ----
echo "[2/4] Running fix-si-numbering.py ..."
python3 "${SCRIPT}" "${OUTPUT_FILE}"
echo ""

# ---- 3. Verify in XML ----
echo "[3/4] Verifying equation numbers in XML ..."

python3 << 'PYEOF'
import zipfile, sys, re

path = "_test_output/test-equation.docx"
try:
    with zipfile.ZipFile(path, "r") as z:
        data = z.read("word/document.xml")
except Exception as e:
    print(f"  ERROR: Cannot read {path}: {e}")
    sys.exit(1)

text = data.decode("utf-8")

# Find oMathPara elements
paras = list(re.finditer(r'(<[^:]+:oMathPara[ >].*?</[^:]+:oMathPara>)', text, re.DOTALL))
if not paras:
    print("  ERROR: No oMathPara elements found")
    sys.exit(1)

print(f"  Found {len(paras)} equation(s)")

errors = 0
for idx, m in enumerate(paras, 1):
    eq = m.group(1)
    t_texts = re.findall(r'<[^:]+:t[^>]*>(.*?)</[^:]+:t>', eq)

    has_s = any(t.strip().startswith("S") and t.strip()[1:].isdigit() for t in t_texts)
    has_unfixed = any(
        t_texts[i].strip().isdigit()
        and not t_texts[i].strip().startswith("S")
        and i > 0 and t_texts[i-1].strip() == "("
        and i + 1 < len(t_texts) and t_texts[i+1].strip() == ")"
        for i in range(len(t_texts))
    )

    if has_s:
        print(f"  ✓ Equation {idx}: (S prefix present)")
    elif has_unfixed:
        print(f"  ✘ Equation {idx}: bare digit still present — fix missed it")
        errors += 1
    else:
        print(f"  ? Equation {idx}: unrecognized pattern. t_texts={t_texts}")
        errors += 1

sys.exit(errors)
PYEOF

VERIFY_EXIT=$?
echo ""

# ---- 4. Test no-equation case ----
echo "[4/4] Testing no-equation code path ..."
quarto render test-no-eq.qmd 2>&1 | tail -2
NOEQ_OUTPUT_FILE="_test_output/test-no-eq.docx"
python3 "${SCRIPT}" "${NOEQ_OUTPUT_FILE}" 2>&1 | grep -q "No equations found" && echo "  ✓ No-equation case handled correctly" || { echo "  ✘ No-equation case failed"; exit 1; }
echo ""

if [ $VERIFY_EXIT -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED (4 tests)${NC}"
    exit 0
else
    echo -e "${RED}✘ SOME CHECKS FAILED${NC}"
    exit 1
fi
