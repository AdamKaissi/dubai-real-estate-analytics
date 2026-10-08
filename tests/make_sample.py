"""Generates a small FAKE file only to check that the pipeline runs end to end.
Never use this data in the write-up. Real findings must come from the real DLD file."""
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 4000
areas = ["Marina", "JVC", "Business Bay", "Downtown", "Palm", "Hills"]
df = pd.DataFrame({
    "transaction_id": [f"T{i}" for i in range(n)],
    "instance_date": pd.to_datetime("2020-01-01") + pd.to_timedelta(rng.integers(0, 2000, n), unit="D"),
    "trans_group_en": rng.choice(["Sales", "Mortgages", "Gifts"], n, p=[.8, .15, .05]),
    "procedure_name_en": "Sell",
    "area_name_en": rng.choice(areas, n),
    "property_type_en": "Unit",
    "property_sub_type_en": rng.choice(["Flat", "Villa"], n),
    "reg_type_en": rng.choice(["Existing Properties", "Off-Plan Properties"], n),
    "project_name_en": "P",
    "rooms_en": rng.choice(["1 B/R", "2 B/R", "3 B/R"], n),
    "procedure_area": rng.uniform(40, 300, n),
})
df["actual_worth"] = df["procedure_area"] * rng.lognormal(9, 0.3, n) / 3
df["instance_date"] = df["instance_date"].dt.strftime("%d-%m-%Y")
df.to_csv("data/raw/dld_transactions.csv", index=False)
print("Wrote fake sample to data/raw/dld_transactions.csv")
