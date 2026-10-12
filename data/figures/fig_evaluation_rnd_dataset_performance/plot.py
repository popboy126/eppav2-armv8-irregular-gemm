from pathlib import Path

from common.performance import plot_performance_set


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    plot_performance_set(
        ROOT / "processed_data/single_thread/random",
        ROOT / "outputs",
        {
            "ft2000": "evaluation_ft2000_rnd_dataset_performance.pdf",
            "kp920": "evaluation_kp920_rnd_dataset_performance.pdf",
            "graviton2": "evaluation_graviton2_rnd_dataset_performance.pdf",
        },
    )


if __name__ == "__main__":
    main()
