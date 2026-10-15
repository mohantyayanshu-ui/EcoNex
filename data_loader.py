
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "emission_factors.csv"

REQUIRED_COLUMNS = [
    "category",
    "item",
    "activity_unit",
    "emission_factor",
    "emission_unit",
    "gas_basis",
    "source",
    "status",
]


def load_emission_factors():
    """Load emission factors and validate the CSV structure."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Emission factors CSV not found: {DATA_FILE}"
        )

    data = pd.read_csv(DATA_FILE, keep_default_na=False)

    missing = [column for column in REQUIRED_COLUMNS
               if column not in data.columns]

    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    for column in ["category", "item"]:
        data[column] = data[column].astype(str).str.strip()

        if (data[column] == "").any():
            raise ValueError(
                f"CSV contains an empty value in '{column}'."
            )

    if data.duplicated(["category", "item"]).any():
        raise ValueError("Duplicate category/item entries found.")

    data["emission_factor"] = pd.to_numeric(
        data["emission_factor"].replace("", pd.NA),
        errors="coerce",
    )

    allowed_statuses = {
        "verified",
        "provisional",
        "historical_estimate",
        "pending_verification",
    }

    data["status"] = data["status"].astype(str).str.strip().str.lower()

    invalid_statuses = sorted(
        set(data["status"]) - allowed_statuses
    )

    if invalid_statuses:
        raise ValueError(
            f"Unknown factor statuses: {invalid_statuses}"
        )

    valid_factors = data["emission_factor"].dropna()

    if (valid_factors < 0).any():
        raise ValueError("Emission factors cannot be negative.")

    if not valid_factors.map(lambda value: value < float("inf")).all():
        raise ValueError("Emission factors must be finite numbers.")

    return data


def get_factor_record(category, item):
    """Return the record for one category/item pair."""

    data = load_emission_factors()

    category = str(category).strip()
    item = str(item).strip()

    matches = data[
        (data["category"] == category)
        & (data["item"] == item)
    ]

    if matches.empty:
        raise ValueError(f"Unknown item: {category}/{item}")

    record = matches.iloc[0].to_dict()
    factor = record["emission_factor"]

    if pd.isna(factor) or factor < 0:
        raise ValueError(
            f"Factor for {category}/{item} is missing or invalid."
        )

    record["emission_factor"] = float(factor)
    return record


if __name__ == "__main__":
    data = load_emission_factors()

    print("Emission factors loaded successfully.")
    print(f"CSV location: {DATA_FILE}")
    print(f"Total entries: {len(data)}")
    print("\nFactor status counts:")
    print(data["status"].value_counts().to_string())

    print("\nCSV structure verified successfully!")