
import math
from numbers import Real

from data_loader import get_factor_record


def calculate_emissions(category, item, activity_amount, activity_unit=None):
    """
    Calculate emissions using the CSV factor.

    activity_unit must match the factor's activity_unit.
    If omitted, the CSV unit is assumed for backward compatibility.
    """

    if (
        isinstance(activity_amount, bool)
        or not isinstance(activity_amount, Real)
    ):
        raise ValueError("Activity amount must be a valid number.")

    if not math.isfinite(activity_amount):
        raise ValueError("Activity amount must be finite.")

    if activity_amount < 0:
        raise ValueError("Activity amount cannot be negative.")

    record = get_factor_record(category, item)

    expected_unit = str(record.get("activity_unit", "")).strip()

    if not expected_unit:
        raise ValueError(
            f"Activity unit is missing for {category}/{item}."
        )

    if activity_unit is not None and activity_unit.strip() != expected_unit:
        raise ValueError(
            f"Wrong activity unit for {category}/{item}. "
            f"Expected '{expected_unit}', received '{activity_unit}'."
        )

    factor = record.get("emission_factor")

    if (
        isinstance(factor, bool)
        or not isinstance(factor, Real)
        or not math.isfinite(factor)
        or factor < 0
    ):
        raise ValueError(
            f"Factor for {category}/{item} is missing or invalid."
        )

    status = str(record.get("status", "")).strip().lower()

    allowed_statuses = {
        "verified",
        "provisional",
        "historical_estimate",
    }

    if status not in allowed_statuses:
        raise ValueError(
            f"Factor for {category}/{item} is not ready to use. "
            f"Current status: {status or 'missing'}."
        )

    emission_unit = str(record.get("emission_unit", "")).strip()
    gas_basis = str(record.get("gas_basis", "")).strip()
    source = str(record.get("source", "")).strip()

    if not emission_unit or not gas_basis or not source:
        raise ValueError(
            f"Factor metadata is incomplete for {category}/{item}."
        )

    if gas_basis not in ("CO2", "CO2e"):
        raise ValueError(
            f"Unsupported gas basis for {category}/{item}: {gas_basis}"
        )

    emissions = float(activity_amount) * float(factor)
    total_emissions_unit = emission_unit.split("/")[0].strip()

    return {
        "category": category,
        "item": item,
        "activity_amount": float(activity_amount),
        "activity_unit": expected_unit,
        "emission_factor": float(factor),
        "emission_factor_unit": emission_unit,
        "emissions": emissions,
        "total_emissions_unit": total_emissions_unit,
        "gas_basis": gas_basis,
        "source": source,
        "status": status,
    }


if __name__ == "__main__":
    print("Carbon Choices - Unit Validation Test\n")

    tests = [
        ("transport", "car", 10, "vehicle_km"),
        ("transport", "bus", 10, "passenger_km"),
        ("transport", "car", 10, "passenger_km"),  # Should fail
        ("electricity", "electricity", 150, "kWh/month"),
        ("transport", "train", 10, "passenger_km"),  # Factor missing
    ]

    for category, item, amount, unit in tests:
        try:
            result = calculate_emissions(
                category, item, amount, activity_unit=unit
            )
            print(
                f"PASS: {category}/{item}: "
                f"{result['emissions']:.3f} "
                f"{result['total_emissions_unit']} "
                f"(unit={result['activity_unit']}, "
                f"status={result['status']})"
            )
        except (ValueError, TypeError, KeyError) as error:
            print(f"BLOCKED: {category}/{item}: {error}")