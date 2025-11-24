import json, csv

def convert(json_file, csv_file):
    with open(json_file) as jf:
        data = json.load(jf)
    with open(csv_file, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    convert("data.json", "output.csv")