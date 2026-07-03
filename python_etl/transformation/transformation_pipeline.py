from python_etl.utils.logger import setup_logger

from python_etl.transformation.transform_fact_order_items import (
    build_fact_order_items,
    save_fact_order_items,
)

from python_etl.transformation.transform_dim_products import (
    build_dim_products,
    save_dim_products,
)

from python_etl.transformation.transform_dim_users import (
    build_dim_users,
    save_dim_users,
)

from python_etl.transformation.transform_dim_orders import (
    build_dim_orders,
    save_dim_orders,
)


logger = setup_logger("transformation_pipeline.log")


def run_transformation_pipeline() -> None:
    logger.info("Starting full transformation pipeline")

    try:
        logger.info("Building fact_order_items")
        fact_order_items_df = build_fact_order_items()
        save_fact_order_items(fact_order_items_df)

        logger.info("Building dim_products")
        dim_products_df = build_dim_products()
        save_dim_products(dim_products_df)

        logger.info("Building dim_users")
        dim_users_df = build_dim_users()
        save_dim_users(dim_users_df)

        logger.info("Building dim_orders")
        dim_orders_df = build_dim_orders()
        save_dim_orders(dim_orders_df)

        logger.info("Full transformation pipeline completed successfully")
        print("Transformation pipeline completed successfully")

    except Exception:
        logger.exception("Transformation pipeline failed")
        raise


if __name__ == "__main__":
    run_transformation_pipeline()