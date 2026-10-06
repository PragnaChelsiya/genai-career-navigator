import pandas as pd

df = pd.read_parquet("data/train-00000-of-00001.parquet")

print("Dataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())