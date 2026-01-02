from src.loader import load_data
from src.cleaner import fill_missing_values, remove_duplicates
from src.reporter import generate_report


def main() -> None:
    df = load_data("data.csv")

    df_clean = fill_missing_values(df)
    df_clean = remove_duplicates(df_clean)

    report = generate_report(df, df_clean)

    print(report)


if __name__ == "__main__":
    main()
