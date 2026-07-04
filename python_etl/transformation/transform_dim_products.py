import pandas as pd
from datetime import datetime

from config.settings import CLEANED_DATA_PATH, CLEANED_FILES, CURATED_DATA_PATH, CURATED_FILES
from python_etl.utils.logger import setup_logger


logger = setup_logger("transformation_pipeline.log")


def build_dim_products() -> pd.DataFrame:
    logger.info("Starting dim_products transformation")

    products_df = pd.read_csv(CLEANED_DATA_PATH / CLEANED_FILES["products"])
    aisles_df = pd.read_csv(CLEANED_DATA_PATH / CLEANED_FILES["aisles"])
    departments_df = pd.read_csv(CLEANED_DATA_PATH / CLEANED_FILES["departments"])

    dim_products_df = products_df.merge(
        aisles_df,
        on="aisle_id",
        how="left",
    ).merge(
        departments_df,
        on="department_id",
        how="left",
    )

    dim_products_df = dim_products_df[
        [
            "product_id",
            "product_name",
            "aisle_id",
            "aisle",
            "department_id",
            "department",
        ]
    ]

    dim_products_df["transformed_at"] = datetime.now()

    logger.info(f"dim_products created with {len(dim_products_df)} rows")

    return dim_products_df


def save_dim_products(dim_products_df: pd.DataFrame) -> None:
    CURATED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    output_path = CURATED_DATA_PATH / CURATED_FILES["dim_products"]

    dim_products_df.to_csv(output_path, index=False)

    logger.info(f"dim_products saved to {output_path}")


def main():
    try:
        dim_products_df = build_dim_products()
        save_dim_products(dim_products_df)

        print("dim_products transformation completed successfully")

    except Exception:
        logger.exception("dim_products transformation failed")
        raise


if __name__ == "__main__":
    main()
