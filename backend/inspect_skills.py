import pandas as pd

# Load dataset
df = pd.read_parquet("data/train-00000-of-00001.parquet")

# Show some job titles
print("JOB TITLES:")
print(df["job_title"].head(20).to_string(index=False))

# Show skills for the first job
print("\nSKILLS FOR FIRST JOB:")
print(df["job_skill_set"].iloc[0])

# Count missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())