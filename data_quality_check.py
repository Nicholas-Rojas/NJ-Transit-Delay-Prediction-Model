"""
data_quality_check.py
Profiles the NJ Transit + Amtrak rail-performance CSVs before any modeling.

Usage:
    1. Put the Kaggle CSVs into a ./data/ folder next to this file.
    2. Run:  python data_quality_check.py

Goal: confirm the data is clean ENOUGH to predict train delays -- not perfect.
"clean" is a relationship between the data and your goal, not a property of the file.
"""

import glob
import os
import sys
import pandas as pd

DATA_DIR = "data"


def load_files(data_dir):
    files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    if not files:
        sys.exit(f"No CSVs found in ./{data_dir}/ -- put the Kaggle files there first.")
    print(f"Found {len(files)} CSV files in ./{data_dir}/\n")
    return files


def check_schema(files):
    print("=" * 64)
    print("PHASE 1  Schema consistency across files")
    print("=" * 64)
    schemas = {}
    for f in files:
        cols = tuple(pd.read_csv(f, nrows=0).columns)
        schemas.setdefault(cols, []).append(os.path.basename(f))
    if len(schemas) == 1:
        print(f"All {len(files)} files share the same columns. Safe to concat.\n")
    else:
        print(f"WARNING: {len(schemas)} different column layouts found:")
        for cols, fnames in schemas.items():
            shown = fnames[:3]
            more = "..." if len(fnames) > 3 else ""
            print(f"\n  {len(fnames)} file(s): {shown}{more}")
            print(f"  columns: {list(cols)}")
        print("\n  -> Reconcile these before concatenating, or rows will misalign.\n")


def load_all(files):
    frames = []
    for f in files:
        try:
            frames.append(pd.read_csv(f))
        except Exception as e:
            print(f"  could not read {os.path.basename(f)}: {e}")
    return pd.concat(frames, ignore_index=True)


def structure(df):
    print("=" * 64)
    print("PHASE 1  Structure")
    print("=" * 64)
    print(f"Rows: {len(df):,}   Columns: {df.shape[1]}\n")
    print("Dtypes + non-null counts (are dates real datetimes? numbers numeric?):")
    df.info()
    print("\nRandom sample of 10 rows (sample, NOT .head() -- head hides mid-file junk):")
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(df.sample(min(10, len(df))))
    print()


def completeness(df):
    print("=" * 64)
    print("PHASE 2  Completeness (% missing per column)")
    print("=" * 64)
    miss = (df.isna().mean() * 100).sort_values(ascending=False).round(2)
    print(miss.to_string())
    print("\nJudgment call: a missing actual_time / delay is probably a CANCELLED")
    print("train (a real category), not corrupt data. Decide before you drop.\n")


def uniqueness(df):
    print("=" * 64)
    print("PHASE 2  Uniqueness (duplicates inflate data + leak into eval)")
    print("=" * 64)
    print(f"Fully duplicated rows: {df.duplicated().sum():,}")
    key = [c for c in ["date", "train_id", "to"] if c in df.columns]
    if len(key) >= 2:
        print(f"Duplicate trips by {key}: {df.duplicated(subset=key).sum():,}")
    print()


def consistency(df):
    print("=" * 64)
    print("PHASE 2  Consistency (scraped text splits one category into many)")
    print("=" * 64)
    for col in ["line", "status", "type"]:
        if col in df.columns:
            print(f"\n{col!r}:")
            print(df[col].value_counts(dropna=False).head(20).to_string())
    print()


def target(df):
    print("=" * 64)
    print("PHASE 3  Target column: delay  (interrogate this HARDEST)")
    print("=" * 64)
    delay_col = next((c for c in df.columns if "delay" in c.lower()), None)
    if not delay_col:
        print("No obvious delay column -- check the column names printed above.\n")
        return
    s = pd.to_numeric(df[delay_col], errors="coerce")
    print(f"Column: {delay_col!r}")
    print(s.describe().round(2).to_string())
    print(f"\nNegative (trains early -- legit or error?): {(s < 0).sum():,}")
    print(f"Over 180 min (possible sentinel/error codes): {(s > 180).sum():,}")
    print("\nErrors in a feature hurt a little; errors in the target are fatal.")
    print("Confirm the units (minutes) and how delay is defined.\n")


def coverage(df):
    print("=" * 64)
    print("PHASE 3  Time coverage (find the COVID tail + any gaps)")
    print("=" * 64)
    if "date" in df.columns:
        d = pd.to_datetime(df["date"], errors="coerce")
        print(f"Date range: {d.min()}  ->  {d.max()}")
        print("\nRows per month (Mar-May 2020 will look abnormal -- likely exclude):")
        print(d.dt.to_period("M").value_counts().sort_index().to_string())
    print()


def main():
    files = load_files(DATA_DIR)
    check_schema(files)
    df = load_all(files)
    structure(df)
    completeness(df)
    uniqueness(df)
    consistency(df)
    target(df)
    coverage(df)
    print("=" * 64)
    print("DONE. Now write 3-4 sentences on what you found (row count, schema,")
    print("what missingness means, dups, COVID handling, target reliability).")
    print("Paste that into the README -- it's the part that reads as 'real analyst.'")
    print("=" * 64)


if __name__ == "__main__":
    main()
