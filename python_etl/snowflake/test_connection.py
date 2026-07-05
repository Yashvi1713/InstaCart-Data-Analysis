from python_etl.snowflake.connection import get_snowflake_connection


def main():

    conn = None
    cursor = None

    try:

        conn = get_snowflake_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                CURRENT_ACCOUNT(),
                CURRENT_USER(),
                CURRENT_ROLE(),
                CURRENT_WAREHOUSE(),
                CURRENT_DATABASE(),
                CURRENT_SCHEMA(),
                CURRENT_VERSION();
            """
        )

        result = cursor.fetchone()

        print("\n========== Snowflake Connection ==========\n")

        print(f"Account      : {result[0]}")
        print(f"User         : {result[1]}")
        print(f"Role         : {result[2]}")
        print(f"Warehouse    : {result[3]}")
        print(f"Database     : {result[4]}")
        print(f"Schema       : {result[5]}")
        print(f"Version      : {result[6]}")

        print("\nConnection Successful\n")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    main()