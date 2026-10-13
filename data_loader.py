
import pandas as pd

DATA_FILE = "data/emission_factors.csv"

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
    data = pd.read_csv(DATA_FILE)

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    if data.duplicated(["category", "item"]).any():
        raise ValueError("Duplicate category/item entries found.")

    return data


def get_factor_record(category, item):
    data = load_emission_factors()
    matches = data[
        (data["category"] == category) &
        (data["item"] == item)
    ]

    if matches.empty:
        raise ValueError(f"Unknown item: {category}/{item}")

    record = matches.iloc[0].to_dict()
    factor = pd.to_numeric(record["emission_factor"], errors="coerce")

    if pd.isna(factor) or factor < 0:
        raise ValueError(
            f"Factor for {category}/{item} is missing or invalid."
        )

    record["emission_factor"] = float(factor)
    return record


if __name__ == "__main__":
    data = load_emission_factors()
    print(data.to_string(index=False))
    print("\nCSV structure verified successfully!")