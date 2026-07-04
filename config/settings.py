import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if load_dotenv:
    load_dotenv(PROJECT_ROOT / ".env")


# --------------------------------------------------
# Data paths
# --------------------------------------------------

DATA_DIR = PROJECT_ROOT / "python_etl" / "data"

RAW_DATA_PATH = DATA_DIR / "raw"
PROFILING_DATA_PATH = DATA_DIR / "profiling"
VALIDATION_DATA_PATH = DATA_DIR / "validation"
CLEANING_DATA_PATH = DATA_DIR / "cleaning"
CLEANED_DATA_PATH = DATA_DIR / "cleaned"
CURATED_DATA_PATH = DATA_DIR / "curated"

LOG_DIR = PROJECT_ROOT / "logs"


# --------------------------------------------------
# Source files
# --------------------------------------------------

RAW_FILES = {
    "orders": "orders.csv",
    "products": "products.csv",
    "aisles": "aisles.csv",
    "departments": "departments.csv",
    "order_products__prior": "order_products__prior.csv",
    "order_products__train": "order_products__train.csv",
}


# --------------------------------------------------
# Cleaned output files
# --------------------------------------------------

CLEANED_FILES = {
    "orders": "orders_cleaned.csv",
    "products": "products_cleaned.csv",
    "aisles": "aisles_cleaned.csv",
    "departments": "departments_cleaned.csv",
    "order_products__prior": "order_products__prior_cleaned.csv",
    "order_products__train": "order_products__train_cleaned.csv",
}


# --------------------------------------------------
# Curated output files
# --------------------------------------------------

CURATED_FILES = {
    "fact_order_items": "fact_order_items.csv",
    "dim_products": "dim_products.csv",
    "dim_users": "dim_users.csv",
    "dim_orders": "dim_orders.csv",
}


# --------------------------------------------------
# Snowflake configuration
# --------------------------------------------------

SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}


def validate_snowflake_config() -> None:
    missing_values = [
        key for key, value in SNOWFLAKE_CONFIG.items()
        if not value
    ]

    if missing_values:
        raise EnvironmentError(
            f"Missing Snowflake environment variables: {missing_values}"
        )
