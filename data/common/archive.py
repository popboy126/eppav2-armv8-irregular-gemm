from __future__ import annotations

import json
import statistics
import tarfile
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd


def detail_records(archive_path: Path) -> Iterable[dict]:
    with tarfile.open(archive_path, "r:*") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            if stream is None:
                continue
            for raw_line in stream:
                line = raw_line.decode("utf-8", errors="replace")
                if line.startswith("Detail - "):
                    yield json.loads(line[9:])


def _scaled_performance(
    values: list[float], shape: tuple[int, int, int], configs: dict
) -> list[float]:
    m, k, n = shape
    padded_m = int(configs.get("M_padding", m))
    padded_k = int(configs.get("K_padding", k))
    padded_n = int(configs.get("N_padding", n))
    scale = (m * k * n) / (padded_m * padded_k * padded_n)
    return [float(value) * scale for value in values]


def performance_frame(archive_path: Path) -> pd.DataFrame:
    algorithms: list[str] = []
    rows: dict[tuple[int, int, int], dict[str, float | int | str]] = {}
    for record in detail_records(archive_path):
        shape = (int(record["m"]), int(record["k"]), int(record["n"]))
        m, k, n = shape
        row = rows.setdefault(
            shape,
            {"MxKxN": f"{m}x{k}x{n}", "m": m, "k": k, "n": n},
        )
        for algorithm, result in record.items():
            if not isinstance(result, dict) or "performance" not in result:
                continue
            if algorithm not in algorithms:
                algorithms.append(algorithm)
            values = _scaled_performance(
                result["performance"], shape, result.get("configs", {})
            )
            row[algorithm] = statistics.median(values)
    frame = pd.DataFrame(rows.values())
    return frame.reindex(columns=["MxKxN", "m", "k", "n", *algorithms])


def end2end_summary(archive_path: Path, providers: Sequence[str]) -> pd.DataFrame:
    per_sample: dict[str, dict[str, float]] = {}
    with tarfile.open(archive_path, "r:*") as archive:
        for provider in providers:
            stream = archive.extractfile(f"openblas_{provider}/result.json")
            if stream is None:
                raise FileNotFoundError(
                    f"missing openblas_{provider} result in {archive_path}"
                )
            data = json.loads(stream.read().decode("utf-8"))
            groups: dict[str, list[float]] = {}
            for record in data["latency"]["samples"]:
                groups.setdefault(record["sample_id"], []).append(record["latency_ms"])
            per_sample[provider] = {
                sample_id: statistics.median(values)
                for sample_id, values in groups.items()
            }
    sample_ids = sorted(per_sample[providers[0]].keys())
    for provider in providers:
        if sorted(per_sample[provider].keys()) != sample_ids:
            raise RuntimeError(f"sample ids differ for {provider}")
    rows = []
    for provider in providers:
        rows.append(
            {
                "provider": provider,
                "mean_latency_ms": statistics.mean(
                    per_sample[provider][sid] for sid in sample_ids
                ),
                "mean_speedup": statistics.mean(
                    per_sample[provider][sid] / per_sample["eppav2"][sid]
                    for sid in sample_ids
                ),
            }
        )
    return pd.DataFrame(rows, columns=["provider", "mean_latency_ms", "mean_speedup"])


def _counter_mean(record: dict, event: str) -> float:
    values: list[float] = []
    for group in ("performance", "group-performance"):
        for sample in record.get(group, []):
            if event not in sample:
                continue
            value = sample[event]
            if isinstance(value, list):
                if value:
                    values.append(sum(float(item) for item in value) / len(value))
            elif isinstance(value, (int, float)):
                values.append(float(value))
    return pd.Series(values).mean() if values else -1.0


def pmu_mean_frame(archive_path: Path, events: list[str]) -> pd.DataFrame:
    rows = []
    for record in detail_records(archive_path):
        row = {
            "m": int(record["m"]),
            "k": int(record["k"]),
            "n": int(record["n"]),
            "bin_label": record["bin_label"],
        }
        row.update({event: _counter_mean(record, event) for event in events})
        rows.append(row)
    return pd.DataFrame(rows)
