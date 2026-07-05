import snowflake.connector

from config.settings import SNOWFLAKE_CONFIG, validate_snowflake_config
from python_etl.utils.logger import setup_logger

logger = setup_logger("snowflake_pipeline.log")


def get_snowflake_connection():
    """
    Create and return a Snowflake connection using environment variables.
    """

    validate_snowflake_config()

    try:
        connection = snowflake.connector.connect(
            **SNOWFLAKE_CONFIG,
        )

        logger.info("Connected to Snowflake successfully")
        return connection

    except Exception:
        logger.exception("Failed to connect to Snowflake")
        raise
