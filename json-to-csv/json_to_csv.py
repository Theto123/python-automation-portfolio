import json
import csv
import os
import logging
import pandas as pd
from datetime import datetime
from collections.abc import MutableMapping

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def flatten_json(y, parent_key='', sep='_'):
    """Flattens nested JSON objects"""
    items = {}
    for k, v in y.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, MutableMapping):
            items.update(flatten_json(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def convert_json_to_csv(json_file, csv_file, flatten=True, field_order=None):
    """Converts a single JSON file to CSV with optional flattening and custom field order"""
    try:
        with open(json_file, "r", encoding="utf-8") as jf:
            data = json.load(jf)

        if flatten:
            data = [flatten_json(item) for item in data]

        if field_order:
            fieldnames = field_order + [k for k in data[0].keys() if k not in field_order]
        else:
            fieldnames = data[0].keys()

        with open(csv_file, "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"Converted {json_file} to {csv_file} ({len(data)} records)")

        excel_file = os.path.splitext(csv_file)[0] + ".xlsx"
        pd.DataFrame(data).to_excel(excel_file, index=False)
        logging.info(f"Also exported to Excel: {excel_file}")

    except Exception as e:
        logging.error(f"Failed to convert {json_file}: {e}")

def convert_folder(json_folder, output_folder):
    """Converts all JSON files in a folder to CSV/Excel"""
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(json_folder):
        if file.lower().endswith(".json"):
            input_path = os.path.join(json_folder, file)
            output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".csv")
            convert_json_to_csv(input_path, output_path)

if __name__ == "__main__":
    convert_folder("json_data", "csv_output")
