import pandas as pd
from pathlib import Path

from python_etl.profiling.profiler_utils import (generate_column_profile, generate_dataset_summary, save_profile_reports)
from python_etl.utils.logger import setup_logger

RAW_DATA_PATH = Path("python_etl/data/raw")
PROFILE_OUTPUT_PATH = Path("python_etl/data/profiling")

logger = setup_logger()

def process_file(file_path):
    file_name = file_path.stem
    logger.info(f"Starting profiling for: {file_name}")

    try:
        df = pd.read_csv(file_path)
        logger.info(f"{file_name} loaded successfully")

        column_profile_df = generate_column_profile(df, file_name)

        summary_df = generate_dataset_summary(df, file_name)

        save_profile_reports(column_profile_df, summary_df, PROFILE_OUTPUT_PATH, file_name) 

        logger.info(f"Profiling completed for: {file_name}")     

    except Exception as e:
        logger.error(f"Failed processing {file_name}: {str(e)}")

def main():
    raw_path = Path(RAW_DATA_PATH)

    if not raw_path.exists():
        logger.error("Raw data directory does not exist")
        print("ERROR: data/raw directory not found")
        return

    csv_files = list(raw_path.glob("*.csv"))

    if not csv_files:
        logger.warning("No CSV files found")
        print("No CSV files found in data/raw")
        return
    
    logger.info(f"{len(csv_files)} CSV files detected")

    for file_path in csv_files:
        process_file(file_path)
    
    logger.info("All files processed successfully")
    print("\nData profiling completed successfully")

if __name__ == "__main__":

    main()


