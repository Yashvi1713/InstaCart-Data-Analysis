import pandas as pd

from config.settings import CURATED_DATA_PATH, CURATED_FILES
from python_etl.snowflake.connection import get_snowflake_connection
from python_etl.utils.logger import setup_logger


logger = setup_logger("snowflake_quality_checks.log")


TABLE_CONFIG = {
    "DIM_PRODUCTS": {
        "file": CURATED_FILES["dim_products"],
        "primary_key": "PRODUCT_ID",
    },
    "DIM_USERS": {
        "file": CURATED_FILES["dim_users"],
        "primary_key": "USER_ID",
    },
    "DIM_ORDERS": {
        "file": CURATED_FILES["dim_orders"],
        "primary_key": "ORDER_ID",
    },
    "FACT_ORDER_ITEMS": {
        "file": CURATED_FILES["fact_order_items"],
        "primary_key": None,
    },
}


def get_snowflake_count(cursor, table_name: str) -> int:
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM INSTACART_ANALYTICS.ANALYTICS.{table_name}
    """)
    return cursor.fetchone()[0]


def get_csv_count(file_name: str) -> int:
    file_path = CURATED_DATA_PATH / file_name
    return len(pd.read_csv(file_path))


def check_row_counts(cursor) -> list[dict]:
    results = []

    for table_name, config in TABLE_CONFIG.items():
        csv_count = get_csv_count(config["file"])
        snowflake_count = get_snowflake_count(cursor, table_name)

        results.append({
            "check_name": "row_count_match",
            "table_name": table_name,
            "expected_value": csv_count,
            "actual_value": snowflake_count,
            "status": "PASS" if csv_count == snowflake_count else "FAIL",
        })

    return results


def check_primary_key_uniqueness(cursor) -> list[dict]:
    results = []

    for table_name, config in TABLE_CONFIG.items():
        pk = config["primary_key"]

        if not pk:
            continue

        cursor.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {pk}) AS duplicate_count
            FROM INSTACART_ANALYTICS.ANALYTICS.{table_name}
        """)

        duplicate_count = cursor.fetchone()[0]

        results.append({
            "check_name": "primary_key_uniqueness",
            "table_name": table_name,
            "expected_value": 0,
            "actual_value": duplicate_count,
            "status": "PASS" if duplicate_count == 0 else "FAIL",
        })

    return results


def check_fact_referential_integrity(cursor) -> list[dict]:
    checks = [
        {
            "check_name": "fact_product_id_exists_in_dim_products",
            "sql": """
                SELECT COUNT(*)
                FROM INSTACART_ANALYTICS.ANALYTICS.FACT_ORDER_ITEMS f
                LEFT JOIN INSTACART_ANALYTICS.ANALYTICS.DIM_PRODUCTS p
                    ON f.PRODUCT_ID = p.PRODUCT_ID
                WHERE p.PRODUCT_ID IS NULL
            """
        },
        {
            "check_name": "fact_order_id_exists_in_dim_orders",
            "sql": """
                SELECT COUNT(*)
                FROM INSTACART_ANALYTICS.ANALYTICS.FACT_ORDER_ITEMS f
                LEFT JOIN INSTACART_ANALYTICS.ANALYTICS.DIM_ORDERS o
                    ON f.ORDER_ID = o.ORDER_ID
                WHERE o.ORDER_ID IS NULL
            """
        },
        {
            "check_name": "fact_user_id_exists_in_dim_users",
            "sql": """
                SELECT COUNT(*)
                FROM INSTACART_ANALYTICS.ANALYTICS.FACT_ORDER_ITEMS f
                LEFT JOIN INSTACART_ANALYTICS.ANALYTICS.DIM_USERS u
                    ON f.USER_ID = u.USER_ID
                WHERE u.USER_ID IS NULL
            """
        },
    ]

    results = []

    for check in checks:
        cursor.execute(check["sql"])
        orphan_count = cursor.fetchone()[0]

        results.append({
            "check_name": check["check_name"],
            "table_name": "FACT_ORDER_ITEMS",
            "expected_value": 0,
            "actual_value": orphan_count,
            "status": "PASS" if orphan_count == 0 else "FAIL",
        })

    return results


def check_allowed_values(cursor) -> list[dict]:
    results = []

    cursor.execute("""
        SELECT COUNT(*)
        FROM INSTACART_ANALYTICS.ANALYTICS.FACT_ORDER_ITEMS
        WHERE REORDERED NOT IN (0, 1)
    """)

    invalid_reordered_count = cursor.fetchone()[0]

    results.append({
        "check_name": "reordered_allowed_values",
        "table_name": "FACT_ORDER_ITEMS",
        "expected_value": 0,
        "actual_value": invalid_reordered_count,
        "status": "PASS" if invalid_reordered_count == 0 else "FAIL",
    })

    return results


def run_quality_checks() -> pd.DataFrame:
    conn = None
    cursor = None

    try:
        logger.info("Starting Snowflake quality checks")

        conn = get_snowflake_connection()
        cursor = conn.cursor()

        all_results = []

        all_results.extend(check_row_counts(cursor))
        all_results.extend(check_primary_key_uniqueness(cursor))
        all_results.extend(check_fact_referential_integrity(cursor))
        all_results.extend(check_allowed_values(cursor))

        results_df = pd.DataFrame(all_results)

        output_path = CURATED_DATA_PATH.parent / "snowflake_quality"
        output_path.mkdir(parents=True, exist_ok=True)

        results_df.to_csv(
            output_path / "snowflake_quality_check_results.csv",
            index=False,
        )

        failed_checks = results_df[results_df["status"] == "FAIL"]

        if not failed_checks.empty:
            logger.error("Snowflake quality checks failed")
            print(failed_checks)
            raise ValueError("One or more Snowflake quality checks failed")

        logger.info("All Snowflake quality checks passed")
        print("All Snowflake quality checks passed")

        return results_df

    except Exception:
        logger.exception("Snowflake quality checks failed")
        raise

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    run_quality_checks()