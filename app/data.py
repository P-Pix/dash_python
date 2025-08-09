import pandas as pd
import requests
from functools import lru_cache
from pathlib import Path
import os

# We will combine energy consumption & CO2 emissions from Our World In Data
ENERGY_URL = "https://github.com/owid/energy-data/raw/master/owid-energy-data.csv"
EMISSIONS_URL = "https://github.com/owid/co2-data/raw/master/owid-co2-data.csv"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOCAL_ENERGY = DATA_DIR / "owid-energy-data.csv"
LOCAL_EMISSIONS = DATA_DIR / "owid-co2-data.csv"
LOCAL_TIDY = DATA_DIR / "tidy_energy_co2.csv"

YEAR_MIN = 1965
YEAR_MAX = 2023


def _download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)


def ensure_local_files(force: bool = False):
    """Télécharge les fichiers bruts si absents (ou si force=True)."""
    if force or not LOCAL_ENERGY.exists():
        _download(ENERGY_URL, LOCAL_ENERGY)
    if force or not LOCAL_EMISSIONS.exists():
        _download(EMISSIONS_URL, LOCAL_EMISSIONS)


def _build_tidy(force: bool = False) -> pd.DataFrame:
    """Construit le tidy dataset et le sauvegarde en cache CSV."""
    ensure_local_files(force=force)
    if LOCAL_TIDY.exists() and not force:
        return pd.read_csv(LOCAL_TIDY)

    energy = pd.read_csv(LOCAL_ENERGY, usecols=[
        "iso_code", "country", "year", "primary_energy_consumption", "population"
    ])
    emissions = pd.read_csv(LOCAL_EMISSIONS, usecols=[
        "iso_code", "country", "year", "co2", "co2_per_capita"
    ])

    df = pd.merge(energy, emissions, on=["iso_code", "country", "year"], how="outer")

    records = []
    for _, row in df.iterrows():
        if YEAR_MIN <= row.year <= YEAR_MAX:
            if pd.notna(row.primary_energy_consumption):
                records.append({
                    "iso_code": row.iso_code,
                    "country": row.country,
                    "year": row.year,
                    "indicator": "Primary Energy Consumption (TWh)",
                    "value": row.primary_energy_consumption,
                    "population": row.population
                })
            if pd.notna(row.co2):
                records.append({
                    "iso_code": row.iso_code,
                    "country": row.country,
                    "year": row.year,
                    "indicator": "CO2 Emissions (Mt)",
                    "value": row.co2,
                    "population": row.population
                })
            if pd.notna(row.co2_per_capita):
                records.append({
                    "iso_code": row.iso_code,
                    "country": row.country,
                    "year": row.year,
                    "indicator": "CO2 Emissions per Capita (t)",
                    "value": row.co2_per_capita,
                    "population": row.population
                })

    tidy = pd.DataFrame.from_records(records)
    tidy.to_csv(LOCAL_TIDY, index=False)
    return tidy


@lru_cache(maxsize=1)
def get_dataset(force: bool = False):
    return _build_tidy(force=force)


def list_indicators(df=None):
    if df is None:
        df = get_dataset()
    return sorted(df["indicator"].unique())
