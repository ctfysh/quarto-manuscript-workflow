#!/usr/bin/env python3
"""
fix-si-numbering.py — Post-process SI .docx to inject "S" prefix into
equation numbers.

The Quarto crossref config (fig-title, tbl-title, eq-title) handles label
display text natively. However, equation numbers stored as OMML in DOCX
still show as "(1)" instead of "(S1)" — Pandoc's DOCX writer emits the
raw OMath elements and the crossref config cannot reach into them.

This script patches the rendered DOCX at the OOXML level by trying each
registered equation-numbering pattern. Patterns are ordered by likelihood;
the first one that matches wins.

Usage:
    python fix-si-numbering.py path/to/si.docx

Dependencies: stdlib only (xml.etree.ElementTree, zipfile)

Adding a new pattern:
    When Pandoc changes the OMML output structure (caught by
    assets/tests/test-render.sh), add a new fix function and register it
    in the PATTERNS list. The fix function receives (doc, ns_m) and
    returns (fixed_count, error_message_or_None).
"""

import sys
import os
import shutil
import tempfile
import zipfile
import io
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NS_MATH = "http://schemas.openxmlformats.org/officeDocument/2006/math"

# ---------------------------------------------------------------------------
# Built-in patterns
# ---------------------------------------------------------------------------


def _fix_split(doc, ns_m):
    """Equation number split across three <m:r> runs (Pandoc ≥3.x).

        <m:r><m:rPr><m:sty m:val="p" /></m:rPr><m:t>(</m:t></m:r>
        <m:r><m:t>1</m:t></m:r>     ← prepend "S"
        <m:r><m:rPr><m:sty m:val="p" /></m:rPr><m:t>)</m:t></m:r>

    The namespace prefix varies (m:, ns5:, …) but the URI is
    http://schemas.openxmlformats.org/officeDocument/2006/math.

    Note: This assumes the three equation-number runs ((, digits, )) are
    consecutive siblings in OMML. If Pandoc inserts intermediate formatting
    runs, extend with additional patterns in the PATTERNS list.
    """
    count = 0
    for omath in doc.iter(f"{{{ns_m}}}oMath"):
        runs = list(omath.iter(f"{{{ns_m}}}r"))
        for i, run in enumerate(runs):
            t = run.find(f"{{{ns_m}}}t")
            if t is None or not t.text:
                continue
            text = t.text.strip()
            if not text.isdigit():
                continue

            prev_t = (runs[i - 1].find(f"{{{ns_m}}}t") if i > 0 else None)
            next_t = (runs[i + 1].find(f"{{{ns_m}}}t") if i < len(runs) - 1 else None)

            prev_ok = prev_t is not None and prev_t.text and prev_t.text.strip() == "("
            next_ok = next_t is not None and next_t.text and next_t.text.strip() == ")"

            if prev_ok and next_ok:
                t.text = f"S{text}"
                count += 1
    return count, None if count > 0 else "split: no digit between ( and ) found"


# ---------------------------------------------------------------------------
# Registry — add new patterns here when Pandoc changes
# ---------------------------------------------------------------------------

PATTERNS = [
    ("split (Pandoc ≥3.x)", _fix_split),
]

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def fix_docx(path):
    """Read .docx (ZIP archive), patch document.xml, write back in-place."""
    temp_path = tempfile.mktemp(suffix=".docx")
    modified = False
    ns_m = NS_MATH

    with zipfile.ZipFile(path, "r") as zin:
        with zipfile.ZipFile(temp_path, "w") as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)

                if item.filename == "word/document.xml":
                    doc = ET.fromstring(data)
                    print(f"Processing: {path}")

                    # Check if there are any equations at all
                    omath_count = len(list(doc.iter(f"{{{ns_m}}}oMath")))
                    if omath_count == 0:
                        print("  No equations found — nothing to fix.")
                        zout.writestr(item, data)
                        continue

                    # Try each registered pattern
                    fixed = False
                    for name, fix_fn in PATTERNS:
                        c, err = fix_fn(doc, ns_m)
                        if c > 0:
                            print(f"  ✓ Matched pattern: {name}")
                            print(f"  Fixed {c} equation number(s)")
                            fixed = True
                            break
                        else:
                            print(f"  ✗ Skipped pattern: {name} — {err}")

                    if not fixed:
                        print()
                        print("  ERROR: No known equation numbering pattern matched.")
                        print("  Pandoc may have changed the OMML output structure.")
                        print("  To fix:")
                        print(f"    1. Run: bash {SCRIPT_DIR}/../tests/test-render.sh")
                        print("    2. Open assets/scripts/fix-si-numbering.py")
                        print("    3. Add a new fix function + register in PATTERNS")
                        print()
                        sys.exit(1)

                    buf = io.BytesIO()
                    ET.ElementTree(doc).write(
                        buf, encoding="UTF-8", xml_declaration=True
                    )
                    data = buf.getvalue()
                    modified = True

                zout.writestr(item, data)

    if modified:
        shutil.move(temp_path, os.path.abspath(path))
        print(f"✓ Saved: {path}")
    else:
        os.unlink(temp_path)
        print(f"  No changes needed: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix-si-numbering.py path/to/si.docx", file=sys.stderr)
        sys.exit(1)
    fix_docx(sys.argv[1])
