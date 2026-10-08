"""Step 2: clean the raw DLD transactions. Every step logs rows removed so the
cleaning decisions can be documented (docs/cleaning_decisions.md)."""
import numpy as np
import pandas as pd
from config import RAW_FILE, CLEAN_FILE, COLS, START_DATE, RESIDENTIAL_SUBTYPES, INCLUDE_PROCEDURES

log = []
def step(name, df, before):
    log.append({"step": name, "rows_after": len(df), "rows_removed": before - len(df)})
    print(f"{name:55s} kept {len(df):>10,}  removed {before - len(df):>9,}")
    return df

raw = pd.read_csv(RAW_FILE, low_memory=False)
df = raw.rename(columns={v: k for k, v in COLS.items()})[list(COLS.keys())].copy()
log.append({"step": "raw rows loaded", "rows_after": len(df), "rows_removed": 0})
print(f"{'raw rows loaded':55s} {len(df):>10,}")

# 1. parse dates (your file uses ISO format, YYYY-MM-DD)
n = len(df)
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
df = step("drop unparseable dates", df.dropna(subset=["date"]), n)

# 2. analysis window
n = len(df)
df = step(f"keep dates >= {START_DATE}", df[df["date"] >= START_DATE], n)

# 3. sales only (exclude mortgages, gifts, etc.)
n = len(df)
df = step("keep sales transactions only",
          df[df["group"].astype(str).str.contains("sale", case=False, na=False)], n)

# 3b. keep only ordinary market-sale procedures (whitelist set in config.py)
print("\nSales procedures present:\n" + df["procedure"].value_counts().head(12).to_string() + "\n")
n = len(df)
keep = df["procedure"].astype(str).str.strip().str.lower().isin([p.lower() for p in INCLUDE_PROCEDURES])
df = step(f"keep procedures {INCLUDE_PROCEDURES}", df[keep], n)

# 3c. residential only (offices, shops, land, hotel rooms have different price dynamics)
print("Property sub types present:\n" + df["property_sub_type"].value_counts().head(10).to_string() + "\n")
n = len(df)
df = step(f"keep residential sub types {RESIDENTIAL_SUBTYPES}",
          df[df["property_sub_type"].isin(RESIDENTIAL_SUBTYPES)], n)

# 4. numeric value and area, must be positive
for c in ["value", "area_sqm"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
n = len(df)
df = step("drop missing/non-positive value or area",
          df[(df["value"] > 0) & (df["area_sqm"] > 0)], n)

# 5. recompute price per sqm ourselves rather than trusting the provided column
df["price_per_sqm"] = df["value"] / df["area_sqm"]

# 6. drop duplicate transaction ids
n = len(df)
df = step("drop duplicate transaction_id", df.drop_duplicates(subset="transaction_id"), n)

# 7. outliers: extreme price/sqm within each property sub type (|z| > 4 on log scale)
df["log_psqm"] = np.log(df["price_per_sqm"])
grp = df.groupby("property_sub_type")["log_psqm"]
z = (df["log_psqm"] - grp.transform("mean")) / grp.transform("std")
n = len(df)
df = step("drop extreme price/sqm outliers (|z|>4, by sub type)", df[z.abs() <= 4], n)

# 8. flag (do NOT drop) likely bulk/portfolio deals: many identical-value rows on one day in one area.
# HEURISTIC - validate it against the data before trusting it, and say so in the write-up.
key = ["date", "area", "value"]
df["is_bulk"] = df.groupby(key)["transaction_id"].transform("count") >= 10
print(f"{'flagged as likely bulk deals (kept, flagged)':55s} {int(df['is_bulk'].sum()):>10,}")

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df.drop(columns=["log_psqm"]).to_csv(CLEAN_FILE, index=False)
pd.DataFrame(log).to_csv("docs/cleaning_log.csv", index=False)
print(f"\nSaved {CLEAN_FILE} and docs/cleaning_log.csv")
