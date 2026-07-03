import pandas as pd
from pathlib import Path
from datetime import datetime

from python_etl.utils.logger import setup_logger


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "cleaned"
CURATED_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "curated"

logger = setup_logger("transformation_pipeline.log")


def get_order_time_bucket(hour: int) -> str:
    if 5 <= hour <= 11:
        return "Morning"
    elif 12 <= hour <= 16:
        return "Afternoon"
    elif 17 <= hour <= 21:
        return "Evening"
    return "Night"


def build_dim_orders() -> pd.DataFrame:
    logger.info("Starting dim_orders transformation")

    orders_df = pd.read_csv(CLEANED_DATA_PATH / "orders_cleaned.csv")

    dim_orders_df = orders_df.copy()

    dim_orders_df["is_first_order"] = dim_orders_df["order_number"] == 1

    dim_orders_df["order_time_bucket"] = dim_orders_df[
        "order_hour_of_day"
    ].apply(get_order_time_bucket)

    dim_orders_df = dim_orders_df[
        [
            "order_id",
            "user_id",
            "eval_set",
            "order_number",
            "order_dow",
            "order_hour_of_day",
            "days_since_prior_order",
            "is_first_order",
            "order_time_bucket",
        ]
    ]

    dim_orders_df["transformed_at"] = datetime.now()

    logger.info(f"dim_orders created with {len(dim_orders_df)} rows")

    return dim_orders_df


def save_dim_orders(dim_orders_df: pd.DataFrame) -> None:
    CURATED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    output_path = CURATED_DATA_PATH / "dim_orders.csv"

    dim_orders_df.to_csv(output_path, index=False)

    logger.info(f"dim_orders saved to {output_path}")


def main():
    try:
        dim_orders_df = build_dim_orders()
        save_dim_orders(dim_orders_df)

        print("dim_orders transformation completed successfully")

    except Exception:
        logger.exception("dim_orders transformation failed")
        raise


if __name__ == "__main__":
    main()