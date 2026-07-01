import pandas as pd
from datetime import datetime


def build_validation_result(
    table_name,
    rule_name,
    column_name,
    validation_type,
    total_records,
    failed_records,
):
    passed_records = total_records - failed_records
    failure_percentage = round((failed_records / total_records) * 100, 2) if total_records else 0

    return {
        "table_name": table_name,
        "rule_name": rule_name,
        "column_name": column_name,
        "validation_type": validation_type,
        "total_records": total_records,
        "failed_records": failed_records,
        "passed_records": passed_records,
        "failure_percentage": failure_percentage,
        "status": "PASS" if failed_records == 0 else "FAIL",
        "run_timestamp": datetime.now(),
    }


def get_failed_sample(df, mask, max_records=5):
    failed_df = df[mask].head(max_records)
    if failed_df.empty:
        return ""
    return failed_df.to_dict(orient="records")


def check_not_null(df, column):
    return df[column].isnull()


def check_unique(df, column):
    return df[column].duplicated(keep=False)


def check_positive(df, column):
    return df[column] <= 0


def check_between(df, column, min_value, max_value):
    return ~df[column].between(min_value, max_value)


def check_allowed_values(df, column, allowed_values):
    return ~df[column].isin(allowed_values)


def check_not_blank(df, column):
    return df[column].isnull() | (df[column].astype(str).str.strip() == "")


def check_composite_unique(df, columns):
    return df.duplicated(subset=columns, keep=False)


def check_conditional_null(df, nullable_column, condition_column, allowed_condition_value):
    return df[nullable_column].isnull() & (df[condition_column] != allowed_condition_value)


def check_min_value_when_not_null(df, column, min_value):
    return df[column].notnull() & (df[column] < min_value)


def check_referential_integrity(child_df, child_column, parent_df, parent_column):
    return ~child_df[child_column].isin(parent_df[parent_column])
