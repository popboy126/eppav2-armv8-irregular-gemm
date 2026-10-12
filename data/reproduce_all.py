from importlib import import_module


MODULES = (
    "figures.fig_ir_gemm_performance_reduction_and_mem_stall.plot",
    "figures.fig_evaluation_cache_model_validation.plot",
    "figures.fig_evaluation_cache_contention_performance.plot",
    "figures.fig_evaluation_cache_contention_ablation.plot",
    "figures.fig_evaluation_rnd_dataset_performance.plot",
    "figures.fig_evaluation_cache_contention_perf_events.plot",
    "figures.fig_evaluation_multiplatform_multithread_native_scaling.plot",
    "figures.fig_evaluate_app_performance.plot",
    "figures.fig_evaluation_rpi_end2end_performance.plot",
    "tables.table_evaluation_cache_model_validation.generate",
)


def main() -> None:
    for module_name in MODULES:
        import_module(module_name).main()


if __name__ == "__main__":
    main()
