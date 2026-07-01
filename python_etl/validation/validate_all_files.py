import pandas as pd
from pathlib import Path

from python_etl.utils.logger import setup_logger
from python_etl.validation.validation_rules import (
    VALIDATION_RULES,
    REFERENTIAL_INTEGRITY_RULES,
    REQUIRED_TABLES,
)
from python_etl.validation.validation_utils import (
    build_validation_result,
    get_failed_sample,
    check_not_null,
    check_unique,
    check_positive,
    check_between,
    check_allowed_values,
    check_not_blank,
    check_composite_unique,
    check_conditional_null,
    check_min_value_when_not_null,
    check_referential_integrity,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "python_etl" / "data" / "raw"
VALIDATION_OUTPUT_PATH = PROJECT_ROOT / "python_etl" / "data" / "validation"

SUMMARY_COLUMNS = [
    "table_name",
    "rule_name",
    "column_name",
    "validation_type",
    "total_records",
    "failed_records",
    "passed_records",
    "failure_percentage",
    "status",
    "run_timestamp",
]

FAILED_RECORD_COLUMNS = [
    "table_name",
    "rule_name",
    "column_name",
    "failed_record_sample",
    "run_timestamp",
]

logger = setup_logger("validation_pipeline.log")


def load_raw_files():
    tables = {}

    for table_name in REQUIRED_TABLES:
        csv_file = RAW_DATA_PATH / f"{table_name}.csv"
        if not csv_file.exists():
            raise FileNotFoundError(f"Required raw file not found: {csv_file}")

        logger.info(f"Loading {table_name}")
        tables[table_name] = pd.read_csv(csv_file)

    return tables


def apply_rule(df, rule):
    rule_type = rule["type"]

    if rule_type == "not_null":
        return check_not_null(df, rule["column"])

    if rule_type == "unique":
        return check_unique(df, rule["column"])

    if rule_type == "positive":
        return check_positive(df, rule["column"])

    if rule_type == "between":
        return check_between(df, rule["column"], rule["min"], rule["max"])

    if rule_type == "allowed_values":
        return check_allowed_values(df, rule["column"], rule["values"])

    if rule_type == "not_blank":
        return check_not_blank(df, rule["column"])

    if rule_type == "composite_unique":
        return check_composite_unique(df, rule["columns"])

    if rule_type == "conditional_null":
        return check_conditional_null(
            df,
            rule["column"],
            rule["condition_column"],
            rule["allowed_condition_value"],
        )

    if rule_type == "min_value_when_not_null":
        return check_min_value_when_not_null(df, rule["column"], rule["min"])

    raise ValueError(f"Unsupported validation rule type: {rule_type}")


def run_table_validations(tables):
    summary_results = []
    failed_records = []

    for table_name, rules in VALIDATION_RULES.items():
        if table_name not in tables:
            logger.warning(f"{table_name} not found in raw data")
            continue

        df = tables[table_name]
        total_records = len(df)

        for rule in rules:
            try:
                failure_mask = apply_rule(df, rule)
                failed_count = int(failure_mask.sum())

                column_name = rule.get("column", ",".join(rule.get("columns", [])))

                summary_results.append(
                    build_validation_result(
                        table_name=table_name,
                        rule_name=rule["rule_name"],
                        column_name=column_name,
                        validation_type=rule["type"],
                        total_records=total_records,
                        failed_records=failed_count,
                    )
                )

                if failed_count > 0:
                    failed_records.append({
                        "table_name": table_name,
                        "rule_name": rule["rule_name"],
                        "column_name": column_name,
                        "failed_record_sample": get_failed_sample(df, failure_mask),
                        "run_timestamp": pd.Timestamp.now(),
                    })

            except Exception:
                logger.exception(f"Validation failed for {table_name} - {rule['rule_name']}")
                raise

    return summary_results, failed_records


def run_referential_integrity_validations(tables):
    summary_results = []
    failed_records = []

    for rule in REFERENTIAL_INTEGRITY_RULES:
        try:
            child_table = rule["child_table"]
            parent_table = rule["parent_table"]

            child_df = tables[child_table]
            parent_df = tables[parent_table]

            if "parent_filter_column" in rule:
                parent_df = parent_df[
                    parent_df[rule["parent_filter_column"]]
                    == rule["parent_filter_value"]
                ]

            failure_mask = check_referential_integrity(
                child_df=child_df,
                child_column=rule["child_column"],
                parent_df=parent_df,
                parent_column=rule["parent_column"],
            )

            failed_count = int(failure_mask.sum())
            total_records = len(child_df)

            summary_results.append(
                build_validation_result(
                    table_name=child_table,
                    rule_name=rule["rule_name"],
                    column_name=rule["child_column"],
                    validation_type="referential_integrity",
                    total_records=total_records,
                    failed_records=failed_count,
                )
            )

            if failed_count > 0:
                failed_records.append({
                    "table_name": child_table,
                    "rule_name": rule["rule_name"],
                    "column_name": rule["child_column"],
                    "failed_record_sample": get_failed_sample(child_df, failure_mask),
                    "run_timestamp": pd.Timestamp.now(),
                })

        except Exception:
            logger.exception(f"Referential integrity validation failed: {rule['rule_name']}")
            raise

    return summary_results, failed_records


def save_validation_reports(summary_results, failed_records):
    VALIDATION_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    summary_df = pd.DataFrame(summary_results, columns=SUMMARY_COLUMNS)
    failed_df = pd.DataFrame(failed_records, columns=FAILED_RECORD_COLUMNS)

    summary_df.to_csv(
        VALIDATION_OUTPUT_PATH / "validation_summary.csv",
        index=False,
    )

    failed_df.to_csv(
        VALIDATION_OUTPUT_PATH / "validation_failed_records.csv",
        index=False,
    )

    logger.info("Validation reports saved successfully")


def main():
    logger.info("Starting validation pipeline")

    try:
        tables = load_raw_files()

        table_summary, table_failed = run_table_validations(tables)
        ref_summary, ref_failed = run_referential_integrity_validations(tables)

        all_summary = table_summary + ref_summary
        all_failed = table_failed + ref_failed

        save_validation_reports(all_summary, all_failed)

        failed_rule_count = sum(result["status"] == "FAIL" for result in all_summary)
        logger.info(
            "Validation pipeline completed successfully with %s rules and %s failed rules",
            len(all_summary),
            failed_rule_count,
        )
        print("Validation completed successfully")
    except Exception:
        logger.exception("Validation pipeline failed")
        raise


if __name__ == "__main__":
    main()
