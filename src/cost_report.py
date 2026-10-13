
from datetime import date
from typing import Any

import boto3


def get_monthly_cost(
    start_date: str,
    end_date: str,
    ce_client: Any = None,
) -> dict:
    """Return AWS cost data for a date range.

    Cost Explorer treats end_date as exclusive.
    """
    if date.fromisoformat(start_date) >= date.fromisoformat(end_date):
        raise ValueError("end_date must be later than start_date")

    if ce_client is None:
        ce_client = boto3.client("ce", region_name="us-east-1")

    response = ce_client.get_cost_and_usage(
        TimePeriod={
            "Start": start_date,
            "End": end_date,
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    results = response.get("ResultsByTime", [])
    total_amount = 0.0
    unit = "USD"
    estimated = False

    for period in results:
        cost = period.get("Total", {}).get("UnblendedCost", {})
        total_amount += float(cost.get("Amount", "0"))
        unit = cost.get("Unit", unit)
        estimated = estimated or period.get("Estimated", False)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "amount": round(total_amount, 2),
        "unit": unit,
        "estimated": estimated,
        "data_available": bool(results),
    }


if __name__ == "__main__":
    report = get_monthly_cost("2026-09-01", "2026-10-01")
    print(report)
