from fastapi.security import HTTPBearer

from fastapi import (
    Request,
    HTTPException
)

from jose import jwt

import os


SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):

    async def __call__(
        self,
        request: Request
    ):

        credentials = await super().__call__(
            request
        )

        try:

            payload = jwt.decode(
                credentials.credentials,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return payload

        except Exception:

            raise HTTPException(
                status_code=403,
                detail="Invalid token"
            )