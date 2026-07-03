import pandas as pd
from pathlib import Path
from datetime import datetime

from python_etl.utils.logger import setup_logger
from python_etl.cleaning.cleaning_rules import CLEANING_RULES
from python_etl.cleaning.cleaning_utils import (
    standardize_column_names,
    trim_text_columns,
    remove_exact_duplicates,
    enforce_integer_columns,
    enforce_float_columns,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "raw"
CLEANED_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "cleaned"
CLEANING_REPORT_PATH = PROJECT_ROOT / "python_etl" / "data" / "cleaning"

logger = setup_logger("cleaning_pipeline.log")


def clean_table(file_path: Path) -> dict:
    table_name = file_path.stem

    logger.info(f"Starting cleaning for {table_name}")

    df = pd.read_csv(file_path)
    original_rows = len(df)
    original_columns = len(df.columns)

    df = standardize_column_names(df)
    df = trim_text_columns(df)

    df, duplicate_rows_removed = remove_exact_duplicates(df)

    rules = CLEANING_RULES.get(table_name, {})

    df = enforce_integer_columns(
        df,
        rules.get("integer_columns", []),
    )

    df = enforce_float_columns(
        df,
        rules.get("float_columns", []),
    )

    CLEANED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    output_file = CLEANED_DATA_PATH / f"{table_name}_cleaned.csv"
    df.to_csv(output_file, index=False)

    logger.info(f"Completed cleaning for {table_name}")

    return {
        "table_name": table_name,
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "original_columns": original_columns,
        "cleaned_columns": len(df.columns),
        "duplicate_rows_removed": duplicate_rows_removed,
        "output_file": str(output_file),
        "run_timestamp": datetime.now(),
    }


def main():
    logger.info("Starting cleaning pipeline")

    try:
        CLEANING_REPORT_PATH.mkdir(parents=True, exist_ok=True)

        cleaning_summary = []

        csv_files = list(RAW_DATA_PATH.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(f"No CSV files found for cleaning in {RAW_DATA_PATH}")

        for file_path in csv_files:
            summary = clean_table(file_path)
            cleaning_summary.append(summary)

        summary_df = pd.DataFrame(cleaning_summary)

        summary_df.to_csv(
            CLEANING_REPORT_PATH / "cleaning_summary.csv",
            index=False,
        )

        logger.info("Cleaning pipeline completed successfully")

        print("Cleaning completed successfully")
    except Exception:
        logger.exception("Cleaning pipeline failed")
        raise


if __name__ == "__main__":
    main()
