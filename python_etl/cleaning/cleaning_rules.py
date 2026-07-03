CLEANING_RULES = {
    "orders": {
        "integer_columns": [
            "order_id",
            "user_id",
            "order_number",
            "order_dow",
            "order_hour_of_day",
        ],
        "float_columns": [
            "days_since_prior_order",
        ],
    },

    "products": {
        "integer_columns": [
            "product_id",
            "aisle_id",
            "department_id",
        ],
        "float_columns": [],
    },

    "aisles": {
        "integer_columns": [
            "aisle_id",
        ],
        "float_columns": [],
    },

    "departments": {
        "integer_columns": [
            "department_id",
        ],
        "float_columns": [],
    },

    "order_products__prior": {
        "integer_columns": [
            "order_id",
            "product_id",
            "add_to_cart_order",
            "reordered",
        ],
        "float_columns": [],
    },

    "order_products__train": {
        "integer_columns": [
            "order_id",
            "product_id",
            "add_to_cart_order",
            "reordered",
        ],
        "float_columns": [],
    },
}