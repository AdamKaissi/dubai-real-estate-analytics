"""Step 4: which factors are associated with price per sqm? OLS on log price, robust SEs.
Coefficients on log price are approx. percentage effects. This is association, not causation:
there are no controls for view, floor, finish quality, developer, etc."""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from config import CLEAN_FILE, TOP_N_AREAS

df = pd.read_csv(CLEAN_FILE, parse_dates=["date"])
df = df[~df["is_bulk"]].copy()
top = df["area"].value_counts().head(TOP_N_AREAS).index
df["area_grp"] = np.where(df["area"].isin(top), df["area"], "Other")
df["log_psqm"] = np.log(df["price_per_sqm"])
df["year_c"] = df["year"].astype(str)

model = smf.ols("log_psqm ~ C(area_grp) + C(property_sub_type) + C(reg_type) + C(year_c)", data=df)
res = model.fit(cov_type="HC3")

with open("outputs/regression_summary.txt", "w") as f:
    f.write(str(res.summary()))
coef = pd.DataFrame({"coef": res.params, "pct_effect": (np.exp(res.params) - 1) * 100,
                     "p_value": res.pvalues}).round(4)
coef.to_csv("outputs/regression_coefficients.csv")
print(f"n = {int(res.nobs):,}   R-squared = {res.rsquared:.3f}")
print(coef.sort_values("pct_effect", ascending=False).head(15))
