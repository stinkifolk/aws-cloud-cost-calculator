
def evaluate_spending(
    amount: float,
    threshold: float,
    unit: str = "USD",
) -> dict:
    """Evaluate reported spending against a configured threshold."""
    if amount < 0:
        raise ValueError("amount cannot be negative")

    if threshold <= 0:
        raise ValueError("threshold must be greater than zero")

    if amount >= threshold:
        return {
            "alert": True,
            "amount": round(amount, 2),
            "threshold": round(threshold, 2),
            "unit": unit,
            "message": (
                f"Spending alert: {amount:.2f} {unit} "
                f"has reached or exceeded the "
                f"{threshold:.2f} {unit} threshold."
            ),
        }

    return {
        "alert": False,
        "amount": round(amount, 2),
        "threshold": round(threshold, 2),
        "unit": unit,
        "message": (
            f"Spending is {amount:.2f} {unit}, "
            f"below the {threshold:.2f} {unit} threshold."
        ),
    }
