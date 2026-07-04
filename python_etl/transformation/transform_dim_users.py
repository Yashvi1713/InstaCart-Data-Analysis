import pandas as pd
from datetime import datetime

from config.settings import CLEANED_DATA_PATH, CLEANED_FILES, CURATED_DATA_PATH, CURATED_FILES
from python_etl.utils.logger import setup_logger


logger = setup_logger("transformation_pipeline.log")


def build_dim_users() -> pd.DataFrame:
    logger.info("Starting dim_users transformation")

    orders_df = pd.read_csv(CLEANED_DATA_PATH / CLEANED_FILES["orders"])

    dim_users_df = (
        orders_df
        .groupby("user_id")
        .agg(
            total_orders=("order_id", "count"),
            first_order_number=("order_number", "min"),
            last_order_number=("order_number", "max"),
            avg_days_since_prior_order=("days_since_prior_order", "mean"),
            first_order_dow=("order_dow", "first"),
            most_common_order_hour=("order_hour_of_day", lambda x: x.mode().iloc[0]),
        )
        .reset_index()
    )

    dim_users_df["avg_days_since_prior_order"] = dim_users_df[
        "avg_days_since_prior_order"
    ].round(2)

    dim_users_df["transformed_at"] = datetime.now()

    logger.info(f"dim_users created with {len(dim_users_df)} rows")

    return dim_users_df


def save_dim_users(dim_users_df: pd.DataFrame) -> None:
    CURATED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    output_path = CURATED_DATA_PATH / CURATED_FILES["dim_users"]

    dim_users_df.to_csv(output_path, index=False)

    logger.info(f"dim_users saved to {output_path}")


def main():
    try:
        dim_users_df = build_dim_users()
        save_dim_users(dim_users_df)

        print("dim_users transformation completed successfully")

    except Exception:
        logger.exception("dim_users transformation failed")
        raise


if __name__ == "__main__":
    main()
