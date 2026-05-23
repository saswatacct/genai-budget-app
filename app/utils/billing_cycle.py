from datetime import datetime


def get_billing_cycle():

    return datetime.now().strftime(
        "%Y-%m"
    )