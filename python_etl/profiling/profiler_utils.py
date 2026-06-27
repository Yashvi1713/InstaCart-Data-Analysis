import pandas as pd
from pathlib import Path

# csv_path = Path("python_etl/data/raw/orders.csv")
# df = pd.read_csv(csv_path)

def generate_column_profile(df, file_name):
    profile_data = []
    total_rows = len(df)

    for column in df.columns:
        null_count = df[column].isnull().sum()
        duplicate_count = df[column].duplicated().sum()
        unique_count = df[column].nunique()
        dtype = str(df[column].dtype)
        null_percentage = round((null_count/total_rows) * 100, 2)
        sample_values = df[column].dropna().astype(str).unique()[:5]

        profile_data.append({
            "file_name" : file_name,
            "column_name" : column,
            "data_type" : dtype,
            "row_count" : total_rows,
            "null_count" : null_count,
            "null_percentage" : null_percentage,
            "duplicate_count" : duplicate_count,
            "unqiue_count" :  unique_count,
            "samples_values" : ",".join(sample_values)
        })

    profile_df = pd.DataFrame(profile_data)
    
    return profile_df

def generate_dataset_summary(df, file_name):

    summary = {
        "file_name" : file_name,
        "row_count" : len(df),
        "column_count" : len(df.columns),
        "duplicate_rows" : df.duplicated().sum(),
        "memory_usage_mb" : round(df.memory_usage(deep = True).sum() / (1024*1024),2)
    }

    return pd.DataFrame([summary])

def save_profile_reports(column_profile_df, summary_df, output_path, base_file_name):
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    column_profile_df.to_csv(output_path/f"{base_file_name}_column_profile.csv", index=False)
    summary_df.to_csv(output_path/f"{base_file_name}_summary_profile.csv", index=False)
    