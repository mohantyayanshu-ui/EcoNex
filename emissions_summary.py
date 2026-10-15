
from carbon_calculator import calculate_emissions

DAYS_PER_MONTH = 30

# Units that explicitly specify their time period.
PERIOD_BY_UNIT = {
    "kWh/month": "month",
    "kWh/day": "day",
    "meal/day": "day",
    "item/month": "month",
}


def calculate_category_totals(activities):
    """
    Each activity must contain:
        category, item, amount, activity_unit, period

    period must be 'day' or 'month'.

    Emissions are grouped separately by CO2 and CO2e.
    Invalid activities and missing factors are recorded in pending.
    """

    category_totals = {}
    pending = []

    for activity in activities:
        category = activity.get("category")
        item = activity.get("item")
        amount = activity.get("amount")
        activity_unit = activity.get("activity_unit")
        period = activity.get("period")

        # Validate required category and item.
        if not category or not item:
            pending.append({
                "category": category or "unknown",
                "item": item or "unknown",
                "reason": "Category and item are required.",
            })
            continue

        # Validate the reporting period.
        if period not in ("day", "month"):
            pending.append({
                "category": category,
                "item": item,
                "reason": (
                    "Period must be explicitly 'day' or 'month'."
                ),
            })
            continue

        # Check whether the activity unit requires a specific period.
        expected_period = PERIOD_BY_UNIT.get(activity_unit)

        if expected_period and period != expected_period:
            pending.append({
                "category": category,
                "item": item,
                "reason": (
                    f"Activity unit '{activity_unit}' requires "
                    f"period '{expected_period}', not '{period}'."
                ),
            })
            continue

        # Calculate emissions and catch invalid or unavailable factors.
        try:
            result = calculate_emissions(
                category,
                item,
                amount,
                activity_unit=activity_unit,
            )
        except (ValueError, TypeError, KeyError) as error:
            pending.append({
                "category": category,
                "item": item,
                "reason": str(error),
            })
            continue

        emissions = result["emissions"]
        basis = result["gas_basis"]

        # Keep CO2 and CO2e totals separate.
        category_totals.setdefault(basis, {})
        category_totals[basis].setdefault(
            category,
            {"daily": 0.0, "monthly": 0.0},
        )

        if period == "day":
            category_totals[basis][category]["daily"] += emissions
            category_totals[basis][category]["monthly"] += (
                emissions * DAYS_PER_MONTH
            )
        else:
            category_totals[basis][category]["monthly"] += emissions
            category_totals[basis][category]["daily"] += (
                emissions / DAYS_PER_MONTH
            )

    return category_totals, pending


if __name__ == "__main__":
    sample_activities = [
        {
            "category": "transport",
            "item": "car",
            "amount": 10,
            "activity_unit": "vehicle_km",
            "period": "day",
        },
        {
            "category": "transport",
            "item": "motorcycle",
            "amount": 20,
            "activity_unit": "vehicle_km",
            "period": "day",
        },
        {
            "category": "transport",
            "item": "train",
            "amount": 10,
            "activity_unit": "passenger_km",
            "period": "day",
        },
        {
            "category": "food",
            "item": "vegetarian",
            "amount": 2,
            "activity_unit": "meal/day",
            "period": "day",
        },
        {
            "category": "electricity",
            "item": "electricity",
            "amount": 150,
            "activity_unit": "kWh/month",
            "period": "month",
        },
        # Deliberately invalid example to test period validation.
        {
            "category": "electricity",
            "item": "electricity",
            "amount": 150,
            "activity_unit": "kWh/month",
            "period": "day",
        },
    ]

    totals, pending = calculate_category_totals(sample_activities)

    print("Calculated totals by gas basis:")

    for basis, categories in totals.items():
        print(f"\n{basis}:")

        for category, values in categories.items():
            print(
                f"  {category}: "
                f"daily average = {values['daily']:.3f}, "
                f"monthly = {values['monthly']:.3f}"
            )

    print("\nActivities awaiting factors or needing attention:")

    if not pending:
        print("None")
    else:
        for activity in pending:
            print(
                f"{activity['category']}/{activity['item']}: "
                f"{activity['reason']}"
            )
