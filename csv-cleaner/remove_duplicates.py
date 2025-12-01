import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_csv(input_file, output_file, drop_duplicates=True, fill_na=None, type_casts=None, export_excel=False):
    """
    Cleans a CSV file with multiple options:
    - drop_duplicates: Remove duplicate rows
    - fill_na: Dictionary to fill missing values per column
    - type_casts: Dictionary to cast columns to specific types
    - export_excel: Save an Excel version of cleaned data
    """
    if not os.path.exists(input_file):
        logging.error(f"Input file {input_file} does not exist!")
        return

    df = pd.read_csv(input_file)
    logging.info(f"Loaded {len(df)} rows from {input_file}")

    if drop_duplicates:
        before = len(df)
        df.drop_duplicates(inplace=True)
        logging.info(f"Dropped {before - len(df)} duplicate rows")

    # Fill missing values
    if fill_na:
        for col, val in fill_na.items():
            if col in df.columns:
                df[col].fillna(val, inplace=True)
                logging.info(f"Filled missing values in '{col}' with '{val}'")

    if type_casts:
        for col, dtype in type_casts.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype, errors='ignore')
                logging.info(f"Casted column '{col}' to {dtype}")

    df.to_csv(output_file, index=False)
    logging.info(f"Cleaned CSV saved to {output_file}")

    if export_excel:
        excel_file = os.path.splitext(output_file)[0] + ".xlsx"
        df.to_excel(excel_file, index=False)
        logging.info(f"Excel version saved to {excel_file}")
        
    logging.info("Summary statistics:")
    logging.info(df.describe(include='all'))

if __name__ == "__main__":
    clean_csv(
        input_file="input.csv",
        output_file="clean.csv",
        fill_na={"Age": 0, "Name": "Unknown"},
        type_casts={"Age": "int"},
        export_excel=True
    )
