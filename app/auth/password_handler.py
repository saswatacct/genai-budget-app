from passlib.hash import bcrypt


def hash_password(password: str):

    password = password[:72]

    return bcrypt.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    plain_password = plain_password[:72]

    return bcrypt.verify(
        plain_password,
        hashed_password
    )