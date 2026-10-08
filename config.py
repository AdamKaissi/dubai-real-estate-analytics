"""Central settings. Edit COLS after running src/01_inspect.py if names differ."""
import os

RAW_FILE = os.getenv("RAW_FILE", "data/raw/dld_transactions.csv")
CLEAN_FILE = "data/clean/transactions_clean.csv"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://analyst:analyst@localhost:5432/dubai_re")

# Left side = our internal name, right side = column name in the DLD file.
# These are best guesses based on the DLD open-data schema; 01_inspect.py checks them.
COLS = {
    "transaction_id": "transaction_id",
    "date": "instance_date",
    "group": "trans_group_en",
    "procedure": "procedure_name_en",
    "area": "area_name_en",
    "property_type": "property_type_en",
    "property_sub_type": "property_sub_type_en",
    "reg_type": "reg_type_en",
    "project": "project_name_en",
    "rooms": "rooms_en",
    "value": "actual_worth",
    "area_sqm": "procedure_area",
}

START_DATE = "2019-01-01"   # analysis window
TOP_N_AREAS = 25            # areas kept as their own category in the regression

# Residential market analysis: sub types kept for the main price-per-sqm analysis.
# Check the real values with: df["property_sub_type"].value_counts()
RESIDENTIAL_SUBTYPES = ["Flat", "Villa"]
# Sales procedures kept for the analysis (everything else is dropped). Chosen after comparing
# median price per sqm and off-plan/existing split by procedure. Other procedures are
# development-related registrations, payment plans, or lease-to-own, and are ~2% of rows.
INCLUDE_PROCEDURES = ["Sell - Pre registration", "Sell", "Delayed Sell"]
