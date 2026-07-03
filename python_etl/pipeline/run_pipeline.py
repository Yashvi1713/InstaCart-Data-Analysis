from python_etl.utils.logger import setup_logger

from python_etl.profiling.profile_all_files import main as run_profiling
from python_etl.validation.validate_all_files import main as run_validation
from python_etl.cleaning.clean_all_files import main as run_cleaning
from python_etl.transformation.transformation_pipeline import run_transformation_pipeline


logger = setup_logger("master_pipeline.log")


def run_master_pipeline():
    logger.info("Starting master ETL pipeline")

    try:
        logger.info("Step 1: Running profiling")
        run_profiling()

        logger.info("Step 2: Running validation")
        run_validation()

        logger.info("Step 3: Running cleaning")
        run_cleaning()

        logger.info("Step 4: Running transformation")
        run_transformation_pipeline()

        logger.info("Master ETL pipeline completed successfully")
        print("Master ETL pipeline completed successfully")

    except Exception:
        logger.exception("Master ETL pipeline failed")
        raise


if __name__ == "__main__":
    run_master_pipeline()