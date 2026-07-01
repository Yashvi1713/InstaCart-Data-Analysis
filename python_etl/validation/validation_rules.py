VALIDATION_RULES = {
    "orders": [
        {"rule_name": "order_id_not_null", "column": "order_id", "type": "not_null"},
        {"rule_name": "order_id_unique", "column": "order_id", "type": "unique"},
        {"rule_name": "order_id_positive", "column": "order_id", "type": "positive"},

        {"rule_name": "user_id_not_null", "column": "user_id", "type": "not_null"},
        {"rule_name": "user_id_positive", "column": "user_id", "type": "positive"},

        {"rule_name": "order_number_not_null", "column": "order_number", "type": "not_null"},
        {"rule_name": "order_number_positive", "column": "order_number", "type": "positive"},

        {"rule_name": "order_dow_between_0_6", "column": "order_dow", "type": "between", "min": 0, "max": 6},
        {"rule_name": "order_hour_between_0_23", "column": "order_hour_of_day", "type": "between", "min": 0, "max": 23},

        {"rule_name": "eval_set_allowed_values", "column": "eval_set", "type": "allowed_values", "values": ["prior", "train", "test"]},

        {
            "rule_name": "days_since_prior_order_null_only_for_first_order",
            "column": "days_since_prior_order",
            "type": "conditional_null",
            "condition_column": "order_number",
            "allowed_condition_value": 1,
        },
        {
            "rule_name": "days_since_prior_order_non_negative",
            "column": "days_since_prior_order",
            "type": "min_value_when_not_null",
            "min": 0,
        },
    ],

    "products": [
        {"rule_name": "product_id_not_null", "column": "product_id", "type": "not_null"},
        {"rule_name": "product_id_unique", "column": "product_id", "type": "unique"},
        {"rule_name": "product_id_positive", "column": "product_id", "type": "positive"},
        {"rule_name": "product_name_not_blank", "column": "product_name", "type": "not_blank"},
        {"rule_name": "aisle_id_not_null", "column": "aisle_id", "type": "not_null"},
        {"rule_name": "aisle_id_positive", "column": "aisle_id", "type": "positive"},
        {"rule_name": "department_id_not_null", "column": "department_id", "type": "not_null"},
        {"rule_name": "department_id_positive", "column": "department_id", "type": "positive"},
    ],

    "aisles": [
        {"rule_name": "aisle_id_not_null", "column": "aisle_id", "type": "not_null"},
        {"rule_name": "aisle_id_unique", "column": "aisle_id", "type": "unique"},
        {"rule_name": "aisle_id_positive", "column": "aisle_id", "type": "positive"},
        {"rule_name": "aisle_not_blank", "column": "aisle", "type": "not_blank"},
    ],

    "departments": [
        {"rule_name": "department_id_not_null", "column": "department_id", "type": "not_null"},
        {"rule_name": "department_id_unique", "column": "department_id", "type": "unique"},
        {"rule_name": "department_id_positive", "column": "department_id", "type": "positive"},
        {"rule_name": "department_not_blank", "column": "department", "type": "not_blank"},
    ],

    "order_products__prior": [
        {"rule_name": "order_id_not_null", "column": "order_id", "type": "not_null"},
        {"rule_name": "order_id_positive", "column": "order_id", "type": "positive"},
        {"rule_name": "product_id_not_null", "column": "product_id", "type": "not_null"},
        {"rule_name": "product_id_positive", "column": "product_id", "type": "positive"},
        {"rule_name": "order_product_composite_unique", "columns": ["order_id", "product_id"], "type": "composite_unique"},
        {"rule_name": "add_to_cart_order_not_null", "column": "add_to_cart_order", "type": "not_null"},
        {"rule_name": "add_to_cart_order_positive", "column": "add_to_cart_order", "type": "positive"},
        {"rule_name": "reordered_allowed_values", "column": "reordered", "type": "allowed_values", "values": [0, 1]},
    ],

    "order_products__train": [
        {"rule_name": "order_id_not_null", "column": "order_id", "type": "not_null"},
        {"rule_name": "order_id_positive", "column": "order_id", "type": "positive"},
        {"rule_name": "product_id_not_null", "column": "product_id", "type": "not_null"},
        {"rule_name": "product_id_positive", "column": "product_id", "type": "positive"},
        {"rule_name": "order_product_composite_unique", "columns": ["order_id", "product_id"], "type": "composite_unique"},
        {"rule_name": "add_to_cart_order_not_null", "column": "add_to_cart_order", "type": "not_null"},
        {"rule_name": "add_to_cart_order_positive", "column": "add_to_cart_order", "type": "positive"},
        {"rule_name": "reordered_allowed_values", "column": "reordered", "type": "allowed_values", "values": [0, 1]},
    ],
}


REQUIRED_TABLES = list(VALIDATION_RULES.keys())


REFERENTIAL_INTEGRITY_RULES = [
    {
        "rule_name": "products_aisle_id_exists_in_aisles",
        "child_table": "products",
        "child_column": "aisle_id",
        "parent_table": "aisles",
        "parent_column": "aisle_id",
    },
    {
        "rule_name": "products_department_id_exists_in_departments",
        "child_table": "products",
        "child_column": "department_id",
        "parent_table": "departments",
        "parent_column": "department_id",
    },
    {
        "rule_name": "prior_product_id_exists_in_products",
        "child_table": "order_products__prior",
        "child_column": "product_id",
        "parent_table": "products",
        "parent_column": "product_id",
    },
    {
        "rule_name": "train_product_id_exists_in_products",
        "child_table": "order_products__train",
        "child_column": "product_id",
        "parent_table": "products",
        "parent_column": "product_id",
    },
    {
        "rule_name": "prior_order_id_exists_in_prior_orders",
        "child_table": "order_products__prior",
        "child_column": "order_id",
        "parent_table": "orders",
        "parent_column": "order_id",
        "parent_filter_column": "eval_set",
        "parent_filter_value": "prior",
    },
    {
        "rule_name": "train_order_id_exists_in_train_orders",
        "child_table": "order_products__train",
        "child_column": "order_id",
        "parent_table": "orders",
        "parent_column": "order_id",
        "parent_filter_column": "eval_set",
        "parent_filter_value": "train",
    },
]
