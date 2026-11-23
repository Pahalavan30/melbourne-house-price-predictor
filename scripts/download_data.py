"""
Download the Melbourne Housing Snapshot (13,580 sales, 2016-2017).

Tries OpenML first (no login needed). If that fails, download melb_data.csv
manually from Kaggle and put it in data/raw/.

Run from the repo folder:  python scripts/download_data.py
"""
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
out = RAW / "melb_data.csv"

if out.exists():
    print(f"Already have {out.name}, skipping download.")
else:
    try:
        from sklearn.datasets import fetch_openml

        print("Downloading from OpenML...")
        df = fetch_openml(data_id=43447, as_frame=True).frame
        df.to_csv(out, index=False)
        print(f"Saved {out.name}")
    except Exception as e:  # network blocked, dataset moved, etc.
        raise SystemExit(
            f"OpenML download failed ({e}).\n"
            "Download melb_data.csv from "
            "https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot "
            f"and save it to {RAW}"
        )

df = pd.read_csv(out)
print("\nRows:", f"{len(df):,}", "| Columns:", df.shape[1])
print("Columns:", list(df.columns))
print("Price range:", f"${df['Price'].min():,.0f} to ${df['Price'].max():,.0f}")
