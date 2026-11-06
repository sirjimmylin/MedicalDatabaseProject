# ──────────────────────────────────────────────────────────────────────────────
# rebuild_notebook.py  –  clean absolute paths & rename the kernel / DB name
# ──────────────────────────────────────────────────────────────────────────────
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).parent.parent           # repo root
NOTEBOOK = ROOT / "src" / "SQLProject.ipynb"
BACKUP   = NOTEBOOK.with_suffix(".ipynb.bak")

# -------------------------------------------------------------------------
# 1️⃣  Make a backup
# -------------------------------------------------------------------------
shutil.copy2(NOTEBOOK, BACKUP)
print(f"✅ Backup created: {BACKUP}")

# -------------------------------------------------------------------------
# 2️⃣  Load notebook JSON
# -------------------------------------------------------------------------
nb = json.load(open(NOTEBOOK, "r", encoding="utf‑8"))

# -------------------------------------------------------------------------
# 3️⃣  Helper: replace absolute paths with a relative one
# -------------------------------------------------------------------------
def relativise_path(abs_path: str) -> str:
    """
    Convert an absolute path that lives under the repo root
    into a path relative to the notebook location (src/).
    Example:
        /Users/jimmylin/.../data/physicians.csv  →  ../data/physicians.csv
    """
    abs_path = pathlib.Path(abs_path).resolve()
    try:
        rel = abs_path.relative_to(ROOT)
        # notebook lives in src/, so go up one level
        return f"../{rel}"
    except ValueError:
        # Path is *outside* the repo – leave untouched (should not happen)
        return str(abs_path)


# -------------------------------------------------------------------------
# 4️⃣  Walk every cell and perform replacements
# -------------------------------------------------------------------------
for idx, cell in enumerate(nb["cells"]):
    src = "".join(cell.get("source", []))

    # ---- a) Remove old database name from any SQL string ----
    src = src.replace("data1050SQLProject", "medical_database")

    # ---- b) Replace absolute CSV paths with relative ones ----
    # Look for string literals that contain “…/data/<file>.csv”
    pattern = r'\"([^"]*?/data/[^"]+?\.csv)\"'
    matches = re.finditer(pattern, src)
    for m in matches:
        abs_path = m.group(1)
        rel_path = relativise_path(abs_path)
        src = src.replace(f'"{abs_path}"', f'"{rel_path}"')

    # ---- c) Write back the possibly‑modified source ----
    # Preserve original line‑breaks (the notebook stores a list of lines)
    cell["source"] = [line + "\n" for line in src.splitlines()]

    # ---- d) Optional: tidy up any empty markdown cells created by the
    #          replacement process (they can appear if we removed everything)
    if cell["cell_type"] == "markdown" and not any(l.strip() for l in cell["source"]):
        # keep a single blank line so the notebook stays valid
        cell["source"] = ["\n"]

# -------------------------------------------------------------------------
# 5️⃣  Update notebook metadata – change the displayed kernel name
# -------------------------------------------------------------------------
kernelspec = nb.get("metadata", {}).get("kernelspec", {})
if kernelspec:
    old_name = kernelspec.get("display_name", "")
    kernelspec["display_name"] = "medical_database"
    print(f"✅ Kernel display name changed: '{old_name}' → 'medical_database'")
else:
    print("⚠️ No kernelspec found – notebook may be using a default kernel.")

# -------------------------------------------------------------------------
# 6️⃣  Write the cleaned notebook back
# -------------------------------------------------------------------------
with open(NOTEBOOK, "w", encoding="utf‑8") as f:
    json.dump(nb, f, indent=1)
print(f"✅ Notebook updated: {NOTEBOOK}")

# -------------------------------------------------------------------------
# 7️⃣  Quick sanity‑check: list any lingering `data1050` strings
# -------------------------------------------------------------------------
leftovers = []
for i, cell in enumerate(nb["cells"]):
    txt = "".join(cell.get("source", []))
    if "data1050" in txt:
        leftovers.append((i, txt.strip()[:120]))
if leftovers:
    print("\n⚠️  Still found 'data1050' in the following cells (you may want to review):")
    for i, snippet in leftovers:
        print(f"  • Cell {i}: {snippet}")
else:
    print("\n✅ No stray 'data1050' strings remain.")