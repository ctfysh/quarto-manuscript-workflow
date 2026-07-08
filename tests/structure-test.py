#!/usr/bin/env python3
"""Structural integrity tests for quarto-manuscript-workflow."""
import yaml, sys, os, glob, re

errors = 0
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def err(msg):
    global errors
    print(f"  \u2718 {msg}")
    errors += 1

def ok(msg):
    print(f"  \u2713 {msg}")

# ── 1. Asset files exist ──────────────────────────────────────────
print("── Asset files ──")
required_assets = [
    "assets/_quarto-si.yml",
    "assets/_gitignore",
    "assets/template.docx",
    "assets/scripts/abstract.lua",
    "assets/scripts/fix-si-numbering.py",
    "assets/scripts/render-si.sh",
    "assets/tests/test-render.sh",
    "assets/tests/test-equation.qmd",
    "assets/tests/test-no-eq.qmd",
    "assets/tests/_quarto.yml",
    "assets/tests/.gitignore",
]
for p in required_assets:
    if os.path.exists(os.path.join(SKILL_DIR, p)):
        ok(p)
    else:
        err(f"Missing: {p}")

# ── 2. YAML parse checks ──────────────────────────────────────────
print("\n── YAML validity ──")
for p in ["assets/_quarto-si.yml", "assets/tests/_quarto.yml"]:
    fp = os.path.join(SKILL_DIR, p)
    try:
        with open(fp) as f:
            yaml.safe_load(f)
        ok(f"{p} parses")
    except yaml.YAMLError as e:
        err(f"{p}: {e}")

# _quarto-si.yml specifics
with open(os.path.join(SKILL_DIR, "assets/_quarto-si.yml")) as f:
    si = yaml.safe_load(f)
if si["project"]["type"] != "default":
    err("SI project.type != default")
else:
    ok("SI project.type = default")
csl = si.get("format", {}).get("docx", {}).get("csl", "")
if csl != "<journal>.csl":
    err(f"SI csl = {csl!r}, expected <journal>.csl")
else:
    ok("SI csl placeholder = <journal>.csl")

# ── 3. Script syntax ──────────────────────────────────────────────
print("\n── Script syntax ──")
import subprocess
scripts = {
    "assets/scripts/fix-si-numbering.py": ["python3", "-m", "py_compile"],
    "assets/scripts/render-si.sh": ["bash", "-n"],
    "assets/scripts/abstract.lua": ["luac", "-p"],
}
for s, cmd in scripts.items():
    fp = os.path.join(SKILL_DIR, s)
    r = subprocess.run(cmd + [fp], capture_output=True, text=True)
    if r.returncode == 0:
        ok(f"{s} syntax OK")
    else:
        err(f"{s}: {r.stderr.strip()}")

# ── 4. EN/ZH example pairs ────────────────────────────────────────
print("\n── EN/ZH example pairs ──")
en_files = sorted(glob.glob(os.path.join(SKILL_DIR, "examples/scenario-*-en.md")))
for f in en_files:
    base = re.sub(r"-en\.md$", "", f)
    zh = base + "-zh.md"
    name = os.path.basename(f)
    if not os.path.exists(zh):
        err(f"{name} missing ZH pair")
        continue
    ok(f"{name} + pair exists")

# ── 5. pdf: block presence in scenarios A-D EN ────────────────────
print("\n── pdf: blocks in generated _quarto.yml (A-D EN) ──")
for f in en_files:
    name = os.path.basename(f)
    m = re.search(r"scenario-([A-D])-", name)
    if not m:
        continue
    content = open(f).read()
    # Find ```yaml ... ``` blocks
    blocks = re.findall(r"```yaml\n(.*?)```", content, re.DOTALL)
    found_pdf = any("  pdf:" in b for b in blocks)
    if found_pdf:
        ok(f"{name}: has pdf: block")
    else:
        err(f"{name}: missing pdf: block")

# ── 6. No top-level cite-method in agent-generated yaml ───────────
#   Only check scenarios A-D where the agent generates the _quarto.yml.
#   Scenario F shows the user's EXISTING project config first (valid top-level cite-method),
#   then the agent-generated SI config in a separate block.
print("\n── No top-level cite-method in agent-generated yaml (A-D) ──")
for f in en_files + sorted(glob.glob(os.path.join(SKILL_DIR, "examples/scenario-*-zh.md"))):
    name = os.path.basename(f)
    if not re.search(r"scenario-[A-D]-", name):
        continue
    content = open(f).read()
    yaml_blocks = re.findall(r"```yaml\n(.*?)```", content, re.DOTALL)
    for blk in yaml_blocks:
        if re.search(r"^cite-method:", blk, re.MULTILINE):
            err(f"{name}: top-level cite-method in yaml block")

# ── 7. Internal markdown links resolve ────────────────────────────
print("\n── Internal link resolution ──")
doc_root = SKILL_DIR
for md_file in ["README.md", "SKILL.md"]:
    fp = os.path.join(doc_root, md_file)
    if not os.path.exists(fp):
        err(f"Missing: {md_file}")
        continue
    content = open(fp).read()
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
    for text, href in links:
        if href.startswith("http") or href.startswith("#"):
            continue
        # Resolve relative to md file directory
        target = os.path.normpath(os.path.join(os.path.dirname(fp), href))
        if not os.path.exists(target):
            # Allow instructional example paths that are not real files
            if href in ("figures/placeholder.png",):
                continue
            err(f"{md_file}: '{href}' -> not found")
    ok(f"{md_file}: all internal links resolve")

# ── Summary ───────────────────────────────────────────────────────
print(f"\n{'='*40}")
print(f"Results: {errors} error(s)" if errors else "Results: ALL PASSED")
sys.exit(errors)
