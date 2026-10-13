
from carbon_calculator import calculate_emissions


DAYS_PER_MONTH = 30


def calculate_category_totals(activities):
    """
    Each activity must contain category, item, and amount.
    Amount must match the unit expected by its emission factor.

    Results are separated by gas basis so CO2 is never
    incorrectly combined with CO2e.
    """

    category_totals = {}
    pending = []

    for activity in activities:
        category = activity["category"]
        item = activity["item"]
        amount = activity["amount"]

        try:
            result = calculate_emissions(category, item, amount)
        except ValueError as error:
            pending.append({
                "category": category,
                "item": item,
                "reason": str(error),
            })
            continue

        basis = result["gas_basis"]
        key = (basis, category)

        category_totals[key] = (
            category_totals.get(key, 0) + result["emissions"]
        )

    totals_by_basis = {}

    for (basis, category), amount in category_totals.items():
        totals_by_basis.setdefault(basis, {})
        totals_by_basis[basis][category] = amount

    return totals_by_basis, pending


if __name__ == "__main__":
    sample_activities = [
        {"category": "transport", "item": "car", "amount": 10},
        {"category": "transport", "item": "motorcycle", "amount": 20},
        {"category": "transport", "item": "train", "amount": 10},
        {"category": "food", "item": "vegetarian", "amount": 2},
    ]

    totals, pending = calculate_category_totals(sample_activities)

    print("Calculated totals by gas basis:")
    for basis, categories in totals.items():
        print(f"{basis}: {categories}")

    print("\nActivities awaiting verified factors:")
    for activity in pending:
        print(
            f"{activity['category']}/{activity['item']}: "
            f"{activity['reason']}"
        )