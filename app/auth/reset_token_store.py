from datetime import (
    datetime,
    timedelta
)

import secrets


# ==========================
# Temporary Token Store
# ==========================
#
# For MVP / Single Instance
#
# Later production scale:
# Move to Redis
#
# ==========================

tokens = {}


def create_reset_token(
    email: str
):

    token = (
        secrets.token_urlsafe(
            32
        )
    )

    expiry = (

        datetime.now()

        +

        timedelta(
            minutes=5
        )

    )

    tokens[token] = {

        "email": email,

        "expiry": expiry

    }

    return token


def validate_token(
    token: str
):

    data = tokens.get(
        token
    )

    if not data:

        return None

    if (

        datetime.now()

        >

        data["expiry"]

    ):

        del tokens[token]

        return None

    return data["email"]


def remove_token(
    token: str
):

    tokens.pop(
        token,
        None
    )


def cleanup_expired_tokens():

    current_time = (
        datetime.now()
    )

    expired = [

        token

        for token,
        value

        in tokens.items()

        if value["expiry"]
        < current_time

    ]

    for token in expired:

        tokens.pop(
            token,
            None
        )