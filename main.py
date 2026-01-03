from src.loader import load_data
from src.cleaner import (
    load_config,
    handle_missing_values,
    handle_duplicates,
    handle_outliers,
    handle_scaling,
)
from src.profiler import extended_profile, print_profile_report


def main() -> None:
    df = load_data("data.csv")

    # 1) Load config
    config = load_config("config.yml")

    # 2) Profiling before cleaning
    profile_before = extended_profile(df)
    print_profile_report(profile_before)

    # 3) Apply preprocessing steps
    df_clean = handle_missing_values(df, config)
    df_clean = handle_duplicates(df_clean, config)
    df_clean = handle_outliers(df_clean, config)
    df_clean = handle_scaling(df_clean, config)

    print("=== Data After Preprocessing ===")
    print(df_clean.head())

    # Optional:
    print("=== profiling after cleaning ===")
    profile_after = extended_profile(df_clean)
    print_profile_report(profile_after)


if __name__ == "__main__":
    main()
