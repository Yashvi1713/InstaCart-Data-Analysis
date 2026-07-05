from pathlib import Path

from python_etl.snowflake.connection import get_snowflake_connection
from python_etl.utils.logger import setup_logger


logger = setup_logger("snowflake_pipeline.log")


def execute_sql_file(sql_file: Path) -> None:
    """
    Execute all SQL statements contained in a SQL file.
    """

    logger.info(f"Executing SQL file: {sql_file.name}")

    connection = None
    cursor = None

    try:

        connection = get_snowflake_connection()
        cursor = connection.cursor()

        with open(sql_file, "r", encoding="utf-8") as file:
            sql_script = file.read()

        # Split on semicolon and execute each statement
        statements = [
            stmt.strip()
            for stmt in sql_script.split(";")
            if stmt.strip()
        ]

        for statement in statements:
            logger.info(statement)
            cursor.execute(statement)

        logger.info(f"{sql_file.name} executed successfully")

    except Exception:

        logger.exception(f"Execution failed for {sql_file.name}")
        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()