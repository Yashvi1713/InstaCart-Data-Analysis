import pandas as pd
from pathlib import Path
from datetime import datetime

from python_etl.utils.logger import setup_logger


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "cleaned"
CURATED_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "curated"

logger = setup_logger("transformation_pipeline.log")


def build_fact_order_items() -> pd.DataFrame:
    logger.info("Starting fact_order_items transformation")

    prior_path = CLEANED_DATA_PATH / "order_products__prior_cleaned.csv"
    train_path = CLEANED_DATA_PATH / "order_products__train_cleaned.csv"
    orders_path = CLEANED_DATA_PATH / "orders_cleaned.csv"

    prior_df = pd.read_csv(prior_path)
    train_df = pd.read_csv(train_path)
    orders_df = pd.read_csv(orders_path)

    logger.info("Cleaned input files loaded successfully")

    prior_df["source_file"] = "prior"
    train_df["source_file"] = "train"

    order_products_df = pd.concat(
        [prior_df, train_df],
        ignore_index=True
    )

    logger.info(f"Combined order products rows: {len(order_products_df)}")

    fact_df = order_products_df.merge(
        orders_df[
            [
                "order_id",
                "user_id",
                "eval_set",
                "order_number",
                "order_dow",
                "order_hour_of_day",
                "days_since_prior_order",
            ]
        ],
        on="order_id",
        how="left"
    )

    fact_df = fact_df[
        [
            "order_id",
            "user_id",
            "product_id",
            "add_to_cart_order",
            "reordered",
            "order_number",
            "order_dow",
            "order_hour_of_day",
            "days_since_prior_order",
            "eval_set",
            "source_file",
        ]
    ]

    fact_df["transformed_at"] = datetime.now()

    logger.info(f"fact_order_items created with {len(fact_df)} rows")

    return fact_df


def save_fact_order_items(fact_df: pd.DataFrame) -> None:
    CURATED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    output_path = CURATED_DATA_PATH / "fact_order_items.csv"

    fact_df.to_csv(output_path, index=False)

    logger.info(f"fact_order_items saved to {output_path}")


def main():
    try:
        fact_df = build_fact_order_items()
        save_fact_order_items(fact_df)

        print("fact_order_items transformation completed successfully")

    except Exception:
        logger.exception("fact_order_items transformation failed")
        raise


if __name__ == "__main__":
    main()