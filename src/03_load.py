"""Step 3: build the star schema and load the cleaned data into the database."""
import pandas as pd
from sqlalchemy import create_engine, text
from config import CLEAN_FILE, DATABASE_URL

df = pd.read_csv(CLEAN_FILE, parse_dates=["date"])
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    for stmt in open("sql/schema.sql").read().split(";"):
        if stmt.strip():
            conn.execute(text(stmt))

dim_area = pd.DataFrame({"area_name": sorted(df["area"].dropna().unique())})
dim_area.insert(0, "area_id", range(1, len(dim_area) + 1))

prop_cols = ["property_type", "property_sub_type", "reg_type"]
dim_prop = df[prop_cols].drop_duplicates().reset_index(drop=True)
dim_prop.insert(0, "property_id", range(1, len(dim_prop) + 1))

d = pd.DataFrame({"full_date": sorted(df["date"].dt.normalize().unique())})
d["date_id"] = d["full_date"].dt.strftime("%Y%m%d").astype(int)
d["year"] = d["full_date"].dt.year
d["quarter"] = d["full_date"].dt.quarter
d["month"] = d["full_date"].dt.month

fact = (df.merge(dim_area, left_on="area", right_on="area_name")
          .merge(dim_prop, on=prop_cols, how="left")
          .assign(date_id=lambda x: x["date"].dt.strftime("%Y%m%d").astype(int)))
fact = fact.rename(columns={"project": "project_name", "value": "value_aed"})[
    ["transaction_id", "date_id", "area_id", "property_id", "project_name", "rooms",
     "value_aed", "area_sqm", "price_per_sqm", "is_bulk"]]

dim_area.to_sql("dim_area", engine, if_exists="append", index=False)
dim_prop.to_sql("dim_property", engine, if_exists="append", index=False)
d[["date_id", "full_date", "year", "quarter", "month"]].to_sql("dim_date", engine, if_exists="append", index=False)
fact.to_sql("fact_transactions", engine, if_exists="append", index=False, chunksize=10000)
print(f"Loaded {len(fact):,} fact rows, {len(dim_area)} areas, {len(dim_prop)} property types, {len(d)} dates.")
