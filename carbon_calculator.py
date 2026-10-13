
import math
from numbers import Real

from data_loader import get_factor_record


def calculate_emissions(category, item, activity_amount):
    """Return emissions and their documented gas basis."""

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
    emissions = activity_amount * record["emission_factor"]

    return {
        "category": category,
        "item": item,
        "emissions": emissions,
        "gas_basis": record["gas_basis"],
        "emission_unit": record["emission_unit"],
        "source": record["source"],
    }


if __name__ == "__main__":
    try:
        result = calculate_emissions("transport", "car", 10)
        print(
            f"Estimated emissions: {result['emissions']:.2f} "
            f"{result['emission_unit']}"
        )
        print(f"Gas basis: {result['gas_basis']}")

    except (ValueError, TypeError) as error:
        print(f"Cannot calculate: {error}")