import pandas as pd

def clean(input_file, output_file):
    df = pd.read_csv(input_file)
    df.drop_duplicates(inplace=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    clean("input.csv", "clean.csv")