
from emissions_summary import calculate_category_totals


def calculate_footprint(activities):
    """
    Calculate a user's carbon footprint from lifestyle activities.

    Each activity must contain:
        category: str
        item: str
        amount: number
        activity_unit: str
        period: 'day' or 'month'

    Returns daily/monthly totals and activities that need attention.
    """

    totals, pending = calculate_category_totals(activities)

    result = {
        "status": "success",
        "daily_totals": {},
        "monthly_totals": {},
        "pending_activities": pending,
    }

    for gas_basis, categories in totals.items():
        result["daily_totals"][gas_basis] = {}
        result["monthly_totals"][gas_basis] = {}

        for category, values in categories.items():
            result["daily_totals"][gas_basis][category] = round(
                values["daily"], 3
            )
            result["monthly_totals"][gas_basis][category] = round(
                values["monthly"], 3
            )

    return result


if __name__ == "__main__":
    # Sample data for testing only; not a real user's footprint.
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
            "category": "electricity",
            "item": "electricity",
            "amount": 150,
            "activity_unit": "kWh/month",
            "period": "month",
        },
        {
            "category": "transport",
            "item": "train",
            "amount": 10,
            "activity_unit": "passenger_km",
            "period": "day",
        },
    ]

    footprint = calculate_footprint(sample_activities)

    print("CARBON CHOICES - BACKEND TEST")
    print("=" * 35)
    print("\nDaily totals:")
    print(footprint["daily_totals"])

    print("\nMonthly totals:")
    print(footprint["monthly_totals"])

    print("\nPending activities:")
    for activity in footprint["pending_activities"]:
        print(
            f"- {activity['category']}/{activity['item']}: "
            f"{activity['reason']}"
        )
