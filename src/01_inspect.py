"""Step 1: look at the raw file and check our column mapping before cleaning anything."""
import pandas as pd
from config import RAW_FILE, COLS

df = pd.read_csv(RAW_FILE, low_memory=False, nrows=200000)
print(f"Rows read (first 200k max): {len(df):,}")
print("\nColumns found in file:")
for c in df.columns:
    print(f"  - {c}")

missing = {k: v for k, v in COLS.items() if v not in df.columns}
if missing:
    print("\nMAPPING PROBLEM: these expected columns are not in the file:")
    for k, v in missing.items():
        print(f"  {k!r} -> {v!r}")
    print("Edit COLS in config.py to match the real column names above.")
else:
    print("\nAll mapped columns found. Sample values:")
    for k, v in COLS.items():
        print(f"  {k}: {df[v].dropna().unique()[:5].tolist()}")
