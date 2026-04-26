#!/usr/bin/env python
"""Thin stdlib notebook runner for wisig_SODA_RFF_figure_suite.ipynb."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _read_notebook(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _cell_source(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return str(src)


def execute_notebook_until_entry(notebook_path: Path, namespace: dict) -> dict:
    """Execute code cells from a notebook with the figure autorun cell suppressed."""
    nb = _read_notebook(notebook_path)
    namespace.setdefault("__name__", "__figure_suite_notebook__")
    namespace.setdefault("__file__", str(notebook_path.resolve()))
    namespace.setdefault("FIGURE_AUTORUN", False)
    for idx, cell in enumerate(nb.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = _cell_source(cell)
        if not source.strip():
            continue
        if "FIGURE_SUITE_AUTORUN_CELL" in source:
            continue
        code = compile(source, f"{notebook_path.name}:cell{idx}", "exec")
        exec(code, namespace)
    return namespace


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the WiSig SODA-RFF figure suite notebook.")
    parser.add_argument("--notebook", default="wisig_SODA_RFF_figure_suite.ipynb")
    parser.add_argument("--smoke", action="store_true", help="Run minimal smoke mode.")
    parser.add_argument("--full", action="store_true", help="Run full mode.")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--protocol", action="append", default=None, help="Protocol tag to include; can be repeated.")
    parser.add_argument("--max-splits", type=int, default=None)
    parser.add_argument("--max-folds", type=int, default=None)
    parser.add_argument("--max-epochs", type=int, default=None)
    parser.add_argument("--max-source-samples", type=int, default=None)
    parser.add_argument("--max-target-samples", type=int, default=None)
    args = parser.parse_args()

    if args.full and args.smoke:
        raise SystemExit("Choose either --smoke or --full, not both.")
    smoke = True if args.smoke or not args.full else False
    notebook_path = Path(args.notebook).resolve()
    if not notebook_path.exists():
        raise SystemExit(f"Notebook not found: {notebook_path}")

    ns = {
        "FIGURE_AUTORUN": False,
        "FIGURE_SMOKE": bool(smoke),
    }
    if args.run_name:
        ns["FIGURE_RUN_NAME"] = args.run_name
    if args.output_root:
        ns["FIGURE_OUTPUT_ROOT"] = args.output_root
    if args.protocol:
        ns["FIGURE_PROTOCOLS"] = args.protocol
    if args.max_splits is not None:
        ns["FIGURE_MAX_SPLITS"] = args.max_splits
    if args.max_folds is not None:
        ns["FIGURE_MAX_FOLDS"] = args.max_folds
    if args.max_epochs is not None:
        ns["FIGURE_MAX_EPOCHS"] = args.max_epochs
    if args.max_source_samples is not None:
        ns["FIGURE_MAX_SOURCE_SAMPLES"] = args.max_source_samples
    if args.max_target_samples is not None:
        ns["FIGURE_MAX_TARGET_SAMPLES"] = args.max_target_samples

    old_cwd = os.getcwd()
    os.chdir(notebook_path.parent)
    try:
        execute_notebook_until_entry(notebook_path, ns)
        if "run_figure_suite" not in ns:
            raise RuntimeError("run_figure_suite was not defined by the notebook.")
        result = ns["run_figure_suite"](smoke=smoke)
        if smoke:
            print("FIGURE SMOKE TEST PASSED")
        print("FIGURE_RUN_DIR=", result.get("run_dir"))
        print("FIGURE_CACHE_ROWS=", result.get("cache_rows"))
        return 0
    finally:
        os.chdir(old_cwd)


if __name__ == "__main__":
    raise SystemExit(main())
