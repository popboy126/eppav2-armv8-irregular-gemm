from pathlib import Path

from common.performance import plot_performance_set


ROOT = Path(__file__).resolve().parents[2]
ALGORITHMS = (
    "eppa_v3.25_t1",
    "eppa_v3.25_np2fp_t1",
    "eppa_v3.25_fp2fpl2p_t1",
    "eppa_v3.25_fpl2p2fp_t1",
)
NAMES = {
    "eppa_v3.25_t1": "Full",
    "eppa_v3.25_np2fp_t1": r"w/o $np$",
    "eppa_v3.25_fp2fpl2p_t1": r"w/o $fp$",
    "eppa_v3.25_fpl2p2fp_t1": r"w/o $fp\_l2p$",
}


def main() -> None:
    plot_performance_set(
        ROOT / "processed_data/single_thread/cache_contention",
        ROOT / "outputs",
        {
            "ft2000": "evaluation_cache_contention_ablation_ft2000_performance.pdf",
            "kp920": "evaluation_cache_contention_ablation_kp920_performance.pdf",
            "graviton2": "evaluation_cache_contention_ablation_graviton2_performance.pdf",
        },
        algorithms=ALGORITHMS,
        names=NAMES,
        baseline="eppa_v3.25_t1",
        bar_ylabel="Norm. perf.",
    )


if __name__ == "__main__":
    main()
