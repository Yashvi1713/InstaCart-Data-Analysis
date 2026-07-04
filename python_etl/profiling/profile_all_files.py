import pandas as pd

from config.settings import PROFILING_DATA_PATH, RAW_DATA_PATH, RAW_FILES
from python_etl.profiling.profiler_utils import (generate_column_profile, generate_dataset_summary, save_profile_reports)
from python_etl.utils.logger import setup_logger

logger = setup_logger()

def process_file(file_path):
    file_name = file_path.stem
    logger.info(f"Starting profiling for: {file_name}")

    try:
        df = pd.read_csv(file_path)
        logger.info(f"{file_name} loaded successfully")

        column_profile_df = generate_column_profile(df, file_name)

        summary_df = generate_dataset_summary(df, file_name)

        save_profile_reports(column_profile_df, summary_df, PROFILING_DATA_PATH, file_name) 

        logger.info(f"Profiling completed for: {file_name}")     

    except Exception as e:
        logger.error(f"Failed processing {file_name}: {str(e)}")

def main():
    raw_path = RAW_DATA_PATH

    if not raw_path.exists():
        logger.error("Raw data directory does not exist")
        print("ERROR: data/raw directory not found")
        return

    csv_files = [raw_path / file_name for file_name in RAW_FILES.values()]
    missing_files = [file_path for file_path in csv_files if not file_path.exists()]

    if missing_files:
        logger.error(f"Missing raw files for profiling: {missing_files}")
        print("ERROR: required raw files missing")
        return
    
    logger.info(f"{len(csv_files)} CSV files detected")

    for file_path in csv_files:
        process_file(file_path)
    
    logger.info("All files processed successfully")
    print("\nData profiling completed successfully")

if __name__ == "__main__":

    main()
