def calculate_metrics(
    total_limit,
    total_spent,
    days_passed
):

    remaining = (
        total_limit - total_spent
    )

    usage_percent = (
        total_spent / total_limit
    ) * 100

    avg_daily = (
        total_spent / max(days_passed, 1)
    )

    days_left = 30 - days_passed

    recommended_daily = (
        remaining / max(days_left, 1)
    )

    alert = None

    if usage_percent >= 80:

        alert = (
            "ALERT: 80% limit reached"
        )

    return {
        "remaining": round(
            remaining,
            2
        ),
        "usage_percent": round(
            usage_percent,
            2
        ),
        "avg_daily": round(
            avg_daily,
            2
        ),
        "recommended_daily": round(
            recommended_daily,
            2
        ),
        "alert": alert
    }