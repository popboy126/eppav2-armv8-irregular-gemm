from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from common.archive import end2end_summary, performance_frame, pmu_mean_frame
from common.metrics import cache_diagnostics, read_csv


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_data"
PROCESSED = ROOT / "processed_data"
PLATFORMS = {
    "FT2000+": "ft2000",
    "KunPeng920": "kp920",
    "Graviton2": "graviton2",
}


def write_frame(frame: pd.DataFrame, path: Path, float_format: str = "%.12g") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, float_format=float_format)


def prepare_motivation() -> None:
    archive = (
        RAW
        / "motivation/KunPeng920/"
        "eppa_v3_12_perf_event_libshalom_limit_test_m20_n64.tgz"
    )
    events = ["performance", "cpu-cycles", "mem_stall_l1miss", "mem_stall_l2miss"]
    frame = pmu_mean_frame(archive, events)
    frame = frame[
        frame["bin_label"].isin(
            ["libshalom", "openblas", "blis", "blasfeo", "libxsmm", "eppa_p"]
        )
    ]
    write_frame(
        frame,
        PROCESSED / "motivation/performance_degradation_kp920.csv",
        "%.17g",
    )


def prepare_single_thread() -> None:
    archives = {
        "random": "eppa_v3_25_with_all_t1_task2.tgz",
        "cache_contention": "eppa_v3_25_with_weakness_all_t1_task0.tgz",
    }
    expected = {"random": 8000, "cache_contention": 3000}
    for platform, slug in PLATFORMS.items():
        for dataset, archive_name in archives.items():
            frame = performance_frame(RAW / "single_thread" / platform / archive_name)
            if len(frame) != expected[dataset]:
                raise ValueError(f"{platform}/{dataset} has {len(frame)} rows")
            write_frame(frame, PROCESSED / "single_thread" / dataset / f"{slug}.csv")


def prepare_applications() -> None:
    archives = {
        "pystack": "eppa_v3_25_with_date_pystack_t1_task0.tgz",
        "gromacs": "eppa_v3_25_with_date_gromacs_t1_task0.tgz",
        "scanpy": "eppa_v3_25_with_taco_scanpy_t1_task0.tgz",
    }
    for platform in ("KunPeng920", "Graviton2"):
        slug = PLATFORMS[platform]
        for workload, archive_name in archives.items():
            frame = performance_frame(RAW / "application" / platform / archive_name)
            write_frame(
                frame,
                PROCESSED / "application" / workload / f"{slug}.csv",
                "%.17g",
            )


def prepare_multithread() -> None:
    algorithms = {
        "eppav2": ("eppa_v3.25_mp", "EPPAv2", "native_ld"),
        "armpl": ("armpl", "ARMPL", "native_runtime"),
        "openblas": ("openblas", "OpenBLAS", "native_runtime"),
        "blis": ("blis", "BLIS", "native_runtime"),
        "eigen": ("eigen", "Eigen", "native_runtime"),
        "cake": ("cake", "CAKE", "native_runtime"),
    }
    for platform in ("KunPeng920", "Graviton2"):
        strong_task = "task4" if platform == "KunPeng920" else "task0"
        weak_task = "task3" if platform == "KunPeng920" else "task0"
        frames = {}
        for scaling, task, stem in (
            ("strong", strong_task, "multithread_random"),
            ("weak", weak_task, "multithread_weak_scaling"),
        ):
            for threads in (1, 2, 4, 8, 16):
                archive = (
                    RAW
                    / "multithread"
                    / platform
                    / f"eppa_v3_25_{stem}_t{threads}_1x{threads}x1_{task}.tgz"
                )
                frame = performance_frame(archive)
                if len(frame) != 1500:
                    raise ValueError(f"{archive} has {len(frame)} rows")
                frames[(scaling, threads)] = frame
        rows = []
        for scaling in ("strong", "weak"):
            for algorithm_id, (column, name, execution_path) in algorithms.items():
                baseline_mean = frames[(scaling, 1)][column].mean()
                for threads in (1, 2, 4, 8, 16):
                    mean_gflops = frames[(scaling, threads)][column].mean()
                    speedup = mean_gflops / baseline_mean
                    rows.append(
                        {
                            "scaling_type": scaling,
                            "timing_scope": "native_call",
                            "execution_path": execution_path,
                            "algorithm_id": algorithm_id,
                            "algorithm_column": column,
                            "algorithm": name,
                            "threads": threads,
                            "shape_count": 1500,
                            "mean_gflops": mean_gflops,
                            "aggregate_speedup": speedup,
                            "aggregate_efficiency": speedup / threads,
                        }
                    )
        write_frame(
            pd.DataFrame(rows),
            PROCESSED / "multithread" / f"{PLATFORMS[platform]}.csv",
            "%.17g",
        )


def prepare_end2end() -> None:
    providers = ("tvm", "openblas", "armpl", "blis", "libshalom", "eppav2")
    variants = {
        "rpi_t2": "all_minilm_l6_v2_fp32_five_hybrid_armv8_t2_rpi_stsb_openblas.tgz",
        "rpi_t4": "all_minilm_l6_v2_fp32_five_hybrid_armv8_t4_rpi_stsb_openblas.tgz",
    }
    for slug, archive_name in variants.items():
        frame = end2end_summary(RAW / "end2end/RPI" / archive_name, providers)
        if len(frame) != len(providers):
            raise ValueError(f"{slug} has {len(frame)} rows")
        write_frame(
            frame,
            PROCESSED / "end2end" / f"{slug}.csv",
            "%.17g",
        )


def prepare_cache_model_summary() -> None:
    rows_path = PROCESSED / "cache_model/heldout_v3_rows.csv"
    rows = read_csv(
        rows_path,
        ["platform", "m", "k", "n", "algo", "cache", "actual", "predicted"],
    )
    write_frame(cache_diagnostics(rows), PROCESSED / "cache_model/diagnostics.csv")


def validate_perf_event_tables() -> None:
    read_csv(
        PROCESSED / "perf_events/mechanism_perf_event_summary.csv",
        [
            "shape_key",
            "kernel",
            "bin_label",
            "gflops",
            "l1d_cache_wr_per_kflop",
            "mem_stall_l2miss_per_kflop",
        ],
    )
    read_csv(
        PROCESSED / "perf_events/mechanism_perf_event_details.csv",
        ["m", "k", "n", "bin_label", "gflops", "shape_key"],
    )


def write_checksums() -> None:
    lines = []
    for directory in (RAW, PROCESSED):
        for path in sorted(item for item in directory.rglob("*") if item.is_file()):
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            lines.append(f"{digest.hexdigest()}  {path.relative_to(ROOT).as_posix()}")
    (ROOT / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="ascii")


def main() -> None:
    prepare_motivation()
    prepare_single_thread()
    prepare_applications()
    prepare_multithread()
    prepare_end2end()
    prepare_cache_model_summary()
    validate_perf_event_tables()
    write_checksums()


if __name__ == "__main__":
    main()
