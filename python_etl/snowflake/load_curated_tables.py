from pathlib import Path

from config.settings import CURATED_DATA_PATH
from python_etl.snowflake.connection import get_snowflake_connection
from python_etl.utils.logger import setup_logger


logger = setup_logger("snowflake_pipeline.log")


TABLE_LOAD_CONFIG = {
    "dim_products.csv": "DIM_PRODUCTS",
    "dim_users.csv": "DIM_USERS",
    "dim_orders.csv": "DIM_ORDERS",
    "fact_order_items.csv": "FACT_ORDER_ITEMS",
}


def execute_sql(cursor, sql: str) -> None:
    logger.info(sql)
    cursor.execute(sql)


def truncate_table(cursor, table_name: str) -> None:
    execute_sql(cursor, f"TRUNCATE TABLE INSTACART_ANALYTICS.ANALYTICS.{table_name}")


def put_file_to_stage(cursor, file_path: Path) -> None:
    put_sql = f"""
        PUT file://{file_path}
        @INSTACART_ANALYTICS.ANALYTICS.CURATED_INTERNAL_STAGE
        AUTO_COMPRESS=TRUE
        OVERWRITE=TRUE
    """
    execute_sql(cursor, put_sql)


def copy_into_table(cursor, staged_file_name: str, table_name: str) -> None:
    copy_sql = f"""
        COPY INTO INSTACART_ANALYTICS.ANALYTICS.{table_name}
        FROM @INSTACART_ANALYTICS.ANALYTICS.CURATED_INTERNAL_STAGE/{staged_file_name}.gz
        FILE_FORMAT = (FORMAT_NAME = INSTACART_ANALYTICS.ANALYTICS.CSV_FILE_FORMAT)
        ON_ERROR = 'ABORT_STATEMENT'
    """
    execute_sql(cursor, copy_sql)


def validate_row_count(cursor, table_name: str) -> int:
    cursor.execute(f"SELECT COUNT(*) FROM INSTACART_ANALYTICS.ANALYTICS.{table_name}")
    return cursor.fetchone()[0]


def load_curated_tables() -> None:
    conn = None
    cursor = None

    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()

        execute_sql(cursor, "USE DATABASE INSTACART_ANALYTICS")
        execute_sql(cursor, "USE SCHEMA ANALYTICS")

        for file_name, table_name in TABLE_LOAD_CONFIG.items():
            file_path = CURATED_DATA_PATH / file_name

            if not file_path.exists():
                raise FileNotFoundError(f"Curated file not found: {file_path}")

            logger.info(f"Loading {file_name} into {table_name}")

            truncate_table(cursor, table_name)
            put_file_to_stage(cursor, file_path)
            copy_into_table(cursor, file_name, table_name)

            row_count = validate_row_count(cursor, table_name)
            logger.info(f"{table_name} loaded successfully with {row_count} rows")

        print("Curated tables loaded into Snowflake successfully")

    except Exception:
        logger.exception("Snowflake curated table load failed")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_curated_tables()