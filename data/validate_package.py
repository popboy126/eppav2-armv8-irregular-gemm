from __future__ import annotations

import ast
import csv
import hashlib
import importlib.util
import re
import tokenize
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FORBIDDEN_TEXT = (
    "independent_" + "fpl2p",
    "eppa_v3_25_with_" + "p_l2p",
    "plot_" + "ablation_figure",
)
ABSOLUTE_PATH = re.compile(
    r"(?:[A-Za-z]:[\\/]|/data/" + "matrix_computation_research)"
)


def validate_python() -> None:
    failures = []
    for path in sorted(ROOT.rglob("*.py")):
        with tokenize.open(path) as stream:
            source = stream.read()
        tokens = tokenize.generate_tokens(iter(source.splitlines(keepends=True)).__next__)
        comments = [token for token in tokens if token.type == tokenize.COMMENT]
        if comments:
            failures.append(f"{path}: comments at {[token.start[0] for token in comments]}")
        tree = ast.parse(source, filename=str(path))
        used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name.split(".")[0]
                    if name not in used_names:
                        failures.append(f"{path}: unused import {name}")
            if isinstance(node, ast.ImportFrom) and node.module != "__future__":
                for alias in node.names:
                    name = alias.asname or alias.name
                    if name != "*" and name not in used_names:
                        failures.append(f"{path}: unused import {name}")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if ast.get_docstring(node, clean=False) is not None:
                    failures.append(f"{path}: docstring at line {getattr(node, 'lineno', 1)}")
        if ABSOLUTE_PATH.search(source):
            failures.append(f"{path}: absolute workstation path")
        for text in FORBIDDEN_TEXT:
            if text in source:
                failures.append(f"{path}: inactive token {text}")
    if failures:
        raise ValueError("\n".join(failures))


def validate_manifest() -> None:
    with (ROOT / "manifest.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 12:
        raise ValueError(f"manifest has {len(rows)} rows")
    for row in rows:
        source = ROOT / row["source_data"]
        if not source.exists():
            raise FileNotFoundError(source)
        entry_point = row["entry_point"]
        if entry_point and importlib.util.find_spec(entry_point) is None:
            raise ModuleNotFoundError(entry_point)
        for output in filter(None, row["outputs"].split(";")):
            output_path = ROOT / "outputs" / output
            if not output_path.is_file() or output_path.stat().st_size == 0:
                raise FileNotFoundError(output_path)


def validate_inventory() -> None:
    raw_files = [path for path in (ROOT / "raw_data").rglob("*") if path.is_file()]
    if len(raw_files) != 43:
        raise ValueError(f"raw_data has {len(raw_files)} files")
    inactive = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix in {".pyc", ".pkl", ".obj", ".exe"}
    ]
    if inactive:
        raise ValueError(f"inactive generated files: {inactive}")


def validate_checksums() -> None:
    checksum_path = ROOT / "checksums.sha256"
    entries = checksum_path.read_text(encoding="ascii").splitlines()
    expected_files = [
        path
        for directory in (ROOT / "raw_data", ROOT / "processed_data")
        for path in directory.rglob("*")
        if path.is_file()
    ]
    if len(entries) != len(expected_files):
        raise ValueError(
            f"checksum count {len(entries)} does not match file count {len(expected_files)}"
        )
    for entry in entries:
        expected, relative = entry.split("  ", 1)
        path = ROOT / relative
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected:
            raise ValueError(f"checksum mismatch: {relative}")


def main() -> None:
    validate_python()
    validate_manifest()
    validate_inventory()
    validate_checksums()
    print("package validation passed")


if __name__ == "__main__":
    main()
