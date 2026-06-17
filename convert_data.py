#!/usr/bin/env python3
"""
RARE.Qc Catalog Data Converter
================================
Converts the Excel workbook (List_of_resources_-_Platforms.xlsx) into
two JSON data files consumed by the web catalog:
  - data/platforms.json
  - data/resources.json

USAGE:
  python3 convert_data.py
  python3 convert_data.py path/to/YourExcelFile.xlsx

WHEN TO RUN:
  Run this script any time the Excel file is updated. No other changes needed.
"""

import sys
import json
import pathlib
import pandas as pd


# ─── CONFIG ──────────────────────────────────────────────────────────────────

DEFAULT_EXCEL = "List_of_resources_-_Platforms.xlsx"
OUTPUT_DIR    = pathlib.Path("data")

# Column renames for Sheet 1 – Technology Platforms
PLATFORMS_COL_MAP = {
    "Institution":                                            "institution",
    "Unit":                                                   "unit",
    "Department / Platform / Core Facility":                  "platform",
    "Type (Equipment / Service / Expertise / Data Resource)": "type",
    "Scientific Domain (e.g., Genomics, Imaging, Cell Biology)": "domain",
    "Description":                                            "description",
    "Contact Person":                                         "contact",
    "Email":                                                  "email",
    "Alternative email":                                      "alt_email",
    "Website / Booking Link":                                 "website",
    "Access Type/Cost Model":                                 "access",
    "Location (City)":                                        "city",
}

# Column renames for Sheet 2 – Resources
RESOURCES_COL_MAP = {
    "Institution":                                              "institution",
    "Unit":                                                     "unit",
    "Department / Platform / Core Facility":                    "platform",
    "Resource Name":                                            "resource_name",
    "Type (Equipment / Service / Expertise / Data Resource)":   "type",
    "Scientific Domain (e.g., Genomics, Imaging, Cell Biology)":"domain",
    "Description":                                              "description",
    "Application Area (e.g., Rare Disease, Neuro, Oncology)":  "application_area",
    "Access Type (Internal / External / Collaboration / Fee-for-Service)": "access_type",
    "Cost Model (Free / Cost-recovery / Service Fee)":          "cost_model",
    "Keywords":                                                 "keywords",
    "Contact Person":                                           "contact",
    "Email":                                                    "email",
    "Website / Booking Link":                                   "website",
    "Location (City, Site)":                                    "city",
    "Language of Service (English / French / Bilingual)":       "language",
    "Notes / Additional Information":                           "notes",
    "Last Updated (Date)":                                      "last_updated",
}


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def clean_val(val) -> str:
    """Return a clean string or empty string for NaN / None."""
    if val is None:
        return ""
    s = str(val).strip()
    return "" if s.lower() in ("nan", "none", "nat") else s


def df_to_records(df: pd.DataFrame, col_map: dict, required_keys=("institution", "platform")) -> list[dict]:
    """Rename columns, drop empty rows, return list of dicts."""
    df = df.rename(columns=col_map)
    keep = [v for v in col_map.values() if v in df.columns]
    df   = df[keep]

    records = []
    for _, row in df.iterrows():
        entry = {col: clean_val(row[col]) for col in keep}
        # Skip rows where all required keys are empty
        if not any(entry.get(k) for k in required_keys):
            continue
        records.append(entry)
    return records


# ─── SHEET READERS ───────────────────────────────────────────────────────────

def read_platforms(xl_path: str) -> list[dict]:
    """
    Sheet 1: Technology Platforms
    Row 0 → actual column names (Unnamed: N), Row 1 → real headers, data from Row 2.
    """
    df = pd.read_excel(xl_path, sheet_name="Technology Platforms", header=0)
    # First data row is the real header
    real_cols = df.iloc[0].tolist()
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = real_cols
    # Drop trailing NaN column
    df = df[[c for c in df.columns if str(c) != "nan"]]
    df = df.dropna(how="all")
    return df_to_records(df, PLATFORMS_COL_MAP, required_keys=("institution", "platform"))


def read_resources(xl_path: str) -> list[dict]:
    """
    Sheet 2: Resources
    Row 0 → title text, Row 1 → blank, Row 2 → real headers, data from Row 3.
    """
    df = pd.read_excel(xl_path, sheet_name="Resources", header=1)
    real_cols = df.iloc[0].tolist()
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = real_cols
    df = df.dropna(how="all")
    return df_to_records(
        df, RESOURCES_COL_MAP,
        required_keys=("institution", "resource_name", "description")
    )


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    xl_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXCEL

    if not pathlib.Path(xl_path).exists():
        print(f"ERROR: Excel file not found: {xl_path}")
        print("Usage: python3 convert_data.py [path/to/excel.xlsx]")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Reading: {xl_path}")

    platforms = read_platforms(xl_path)
    out_p = OUTPUT_DIR / "platforms.json"
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(platforms, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {len(platforms):>4} platforms  → {out_p}")

    resources = read_resources(xl_path)
    out_r = OUTPUT_DIR / "resources.json"
    with open(out_r, "w", encoding="utf-8") as f:
        json.dump(resources, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {len(resources):>4} resources  → {out_r}")

    print("\nDone. Drop the updated JSON files into your web app's /data/ folder.")


if __name__ == "__main__":
    main()
