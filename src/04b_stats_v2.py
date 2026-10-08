"""Step 4b: improved model. Adds unit size and rooms as controls, clusters standard errors by
project (units in the same building are not independent), and re-fits without 'Delayed Sell'
as a sensitivity check. Association, not causation: no controls for view, floor, finish, developer."""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from config import CLEAN_FILE, TOP_N_AREAS

df = pd.read_csv(CLEAN_FILE, parse_dates=["date"])
df = df[~df["is_bulk"]].copy()
top = df["area"].value_counts().head(TOP_N_AREAS).index
df["area_grp"] = np.where(df["area"].isin(top), df["area"], "Other")
top_rooms = df["rooms"].fillna("Unknown").value_counts().head(8).index
df["rooms_grp"] = np.where(df["rooms"].fillna("Unknown").isin(top_rooms), df["rooms"].fillna("Unknown"), "Other")
df["project"] = df["project"].fillna("Unknown")
df["log_psqm"] = np.log(df["price_per_sqm"])
df["log_area"] = np.log(df["area_sqm"])
df["year_c"] = df["year"].astype(str)

FORMULA = ("log_psqm ~ C(area_grp) + C(property_sub_type) + C(reg_type) + C(year_c)"
           " + C(rooms_grp) + log_area")

def fit(data):
    codes = pd.factorize(data["project"])[0]
    return smf.ols(FORMULA, data=data).fit(cov_type="cluster", cov_kwds={"groups": codes})

print("Reference (baseline) level for each categorical variable:")
for col in ["area_grp", "property_sub_type", "reg_type", "year_c", "rooms_grp"]:
    print(f"  {col}: {sorted(df[col].unique())[0]}")

res = fit(df)
ci = res.conf_int()
out = pd.DataFrame({"coef": res.params, "pct_effect": (np.exp(res.params) - 1) * 100,
                    "ci_low_pct": (np.exp(ci[0]) - 1) * 100, "ci_high_pct": (np.exp(ci[1]) - 1) * 100,
                    "p_value": res.pvalues}).round(3)
out.to_csv("outputs/regression_v2_coefficients.csv")
open("outputs/regression_v2_summary.txt", "w").write(str(res.summary()))
print(f"\nMain model: n = {int(res.nobs):,}   R-squared = {res.rsquared:.3f}   clusters = {df['project'].nunique():,}")

sens = fit(df[df["procedure"] != "Delayed Sell"])
sens_out = pd.DataFrame({"pct_effect_with_delayed": out["pct_effect"],
                         "pct_effect_without_delayed": ((np.exp(sens.params) - 1) * 100).round(3)})
sens_out.to_csv("outputs/regression_v2_sensitivity.csv")
print(f"Sensitivity (no Delayed Sell): n = {int(sens.nobs):,}   R-squared = {sens.rsquared:.3f}")

keys = ["reg_type", "year_c", "property_sub_type", "log_area"]
show = sens_out[[any(k in i for k in keys) for i in sens_out.index]]
print("\nKey effects, % difference vs baseline (with 95% CI for the main model):")
print(out.loc[show.index, ["pct_effect", "ci_low_pct", "ci_high_pct"]].join(show["pct_effect_without_delayed"]).to_string())
print("\nTop 10 area effects:")
areas = out[out.index.str.contains("area_grp")].sort_values("pct_effect", ascending=False).head(10)
print(areas[["pct_effect", "ci_low_pct", "ci_high_pct"]].to_string())
