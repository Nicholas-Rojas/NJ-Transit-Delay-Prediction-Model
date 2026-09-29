import pandas as pd
import glob

# Just ONE monthly CSV for exploration — fast, and enough to see the shape.
sample = sorted(glob.glob('data/raw/*.csv'))[0]   # adjust path/pattern to yours
df = pd.read_csv(sample)

print("File:", sample)
print("Columns:", list(df.columns), "\n")

# 1. What 'type' values exist, and how is Amtrak labeled/spelled?
print("=== type value counts ===")
print(df['type'].value_counts(dropna=False), "\n")

amtrak = df[df['type'] != 'NJ Transit'].copy()   # everything you filtered out
print("Non-NJT rows:", len(amtrak), f"({len(amtrak)/len(df):.1%} of file)\n")

# 2. Which STATIONS do Amtrak trains actually appear at? (the join surface)
print("=== top Amtrak stations ===")
print(amtrak['from'].value_counts().head(15), "\n")

# 3. Is the messiness in naming? Peek at a few raw rows.
print("=== sample Amtrak rows ===")
print(amtrak[['train_id', 'type', 'line', 'from', 'scheduled_time']].head(10))