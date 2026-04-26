import json
import sys
import traceback
from pathlib import Path

NOTEBOOK = Path("wisig_SODA_RFF_Final_parallel_variants.ipynb")


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    g = {
        "__name__": "__main__",
        "__file__": str(NOTEBOOK.resolve()),
        "RUN_PARALLEL_VARIANTS_SMOKE": True,
        "EXECUTION_MODE": "smoke",
    }
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        code = "".join(cell.get("source", []))
        if not code.strip():
            continue
        print(f"\n===== EXEC CELL {i} =====")
        exec(compile(code, f"{NOTEBOOK.name}:cell_{i}", "exec"), g)
    print("\nPARALLEL SODA VARIANTS NOTEBOOK EXECUTION COMPLETE")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
