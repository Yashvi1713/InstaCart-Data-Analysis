import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def trim_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    return df


def remove_exact_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before_count = len(df)
    df = df.drop_duplicates()
    after_count = len(df)

    removed_count = before_count - after_count

    return df, removed_count


def enforce_integer_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    return df


def enforce_float_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df
