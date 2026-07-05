from pathlib import Path

from config.settings import PROJECT_ROOT

from python_etl.snowflake.execute_sql import execute_sql_file
from python_etl.utils.logger import setup_logger


logger = setup_logger("snowflake_pipeline.log")


SQL_FOLDER = (
    PROJECT_ROOT
    / "python_etl"
    / "snowflake"
    / "sql"
)


def create_snowflake_objects():

    logger.info("Starting Snowflake object creation")

    sql_files = sorted(SQL_FOLDER.glob("*.sql"))

    if not sql_files:
        raise FileNotFoundError(
            f"No SQL files found in {SQL_FOLDER}"
        )

    for sql_file in sql_files:

        execute_sql_file(sql_file)

    logger.info("Snowflake object creation completed")


if __name__ == "__main__":

    create_snowflake_objects()