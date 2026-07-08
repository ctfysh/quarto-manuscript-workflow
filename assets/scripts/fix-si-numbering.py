#!/usr/bin/env python3
"""
fix-si-numbering.py — Post-process SI .docx to inject "S" prefix into
caption numbering and equation numbers.

Usage:
    python fix-si-numbering.py path/to/si.docx

Dependencies: lxml (pip install lxml)
"""

import sys
import os
import shutil
import tempfile
import zipfile
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def fix_caption_numbering(doc):
    """Inject 'S ' prefix into figure/table caption field codes.
    
    Quarto generates DOCX captions using SEQ fields like:
        SEQ Figure \\* ARABIC  →  Figure 1
    We inject 'S ' to produce:
        SEQ Figure S \\* ARABIC  →  Figure S1
    
    This handles any NBSP spacing between prefix and number.
    """
    ns = NS["w"]
    for instr in doc.iter(f"{{{ns}}}instrText"):
        if instr.text:
            if " SEQ Figure " in instr.text:
                instr.text = instr.text.replace(" SEQ Figure ", " SEQ Figure S ")
            if " SEQ Table " in instr.text:
                instr.text = instr.text.replace(" SEQ Table ", " SEQ Table S ")


def fix_equation_numbering(doc):
    """Inject 'S' into equation numbers stored in OMath <m:t> elements.
    
    Equation numbers like (1) are stored in OMath runs as:
        <m:t>(1)</m:t>
    We transform to:
        <m:t>(S1)</m:t>
    """
    ns_m = NS["m"]
    for t in doc.iter(f"{{{ns_m}}}t"):
        if t.text and t.text.strip():
            inner = t.text.strip()
            if inner.startswith("(") and inner.endswith(")"):
                num = inner[1:-1]
                if num.isdigit():
                    t.text = t.text.replace(f"({num})", f"(S{num})")


def fix_docx(path):
    """Read .docx (ZIP), patch document.xml, write back in-place."""
    with zipfile.ZipFile(path, "r") as zin:
        with zipfile.ZipFile(
            tempfile.mktemp(suffix=".docx"), "w"
        ) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    doc = etree.fromstring(data)
                    fix_caption_numbering(doc)
                    fix_equation_numbering(doc)
                    data = etree.tostring(
                        doc, xml_declaration=True, encoding="UTF-8", standalone=True
                    )
                zout.writestr(item, data)
    shutil.move(zout.name, os.path.abspath(path))
    print(f"Fixed captions in {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix-si-numbering.py path/to/si.docx", file=sys.stderr)
        sys.exit(1)
    fix_docx(sys.argv[1])
