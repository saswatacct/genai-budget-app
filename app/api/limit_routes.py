# from fastapi import (
#     APIRouter,
#     Depends
# )

# from pydantic import BaseModel

# from app.auth.auth_bearer import (
#     JWTBearer
# )

# from app.db.database import (
#     get_connection
# )

# from app.utils.billing_cycle import (
#     get_billing_cycle
# )

# router = APIRouter(
#     prefix="/limit"
# )


# class LimitSchema(BaseModel):

#     upi_limit: float

#     credit_limit: float

#     card_no: str

#     account_no: str

#     atm_enabled: bool

#     online_enabled: bool


# @router.post(
#     "/create",
#     dependencies=[Depends(JWTBearer())]
# )
# def create_limit(
#     payload: LimitSchema,
#     token=Depends(JWTBearer())
# ):

#     user_id = token["user_id"]

#     billing_cycle = get_billing_cycle()

#     conn = get_connection()

#     cursor = conn.cursor()

#     existing_limit = cursor.execute(
#         '''
#         SELECT *

#         FROM spending_limits

#         WHERE user_id = ?
#         AND billing_cycle = ?
#         ''',
#         (
#             user_id,
#             billing_cycle
#         )
#     ).fetchone()

#     if existing_limit:

#         cursor.execute(
#             '''
#             UPDATE spending_limits

#             SET
#                 upi_limit = ?,
#                 credit_limit = ?,
#                 card_no = ?,
#                 account_no = ?,
#                 atm_enabled = ?,
#                 online_enabled = ?

#             WHERE user_id = ?
#             AND billing_cycle = ?
#             ''',
#             (
#                 payload.upi_limit,
#                 payload.credit_limit,
#                 payload.card_no,
#                 payload.account_no,
#                 int(payload.atm_enabled),
#                 int(payload.online_enabled),
#                 user_id,
#                 billing_cycle
#             )
#         )

#     else:

#         cursor.execute(
#             '''
#             INSERT INTO spending_limits (

#                 user_id,

#                 upi_limit,

#                 credit_limit,

#                 card_no,

#                 account_no,

#                 atm_enabled,

#                 online_enabled,

#                 billing_cycle
#             )

#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             ''',
#             (
#                 user_id,
#                 payload.upi_limit,
#                 payload.credit_limit,
#                 payload.card_no,
#                 payload.account_no,
#                 int(payload.atm_enabled),
#                 int(payload.online_enabled),
#                 billing_cycle
#             )
#         )

#     conn.commit()

#     conn.close()

#     return {
#         "message": "Spending limit saved",
#         "billing_cycle": billing_cycle
#     }




from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel

from app.auth.auth_bearer import (
    JWTBearer
)

from app.db.database import (
    get_connection
)

from app.utils.billing_cycle import (
    get_billing_cycle
)


router = APIRouter(
    prefix="/limit"
)


class LimitSchema(BaseModel):

    upi_limit: float

    credit_limit: float

    card_no: str

    account_no: str

    atm_enabled: bool

    online_enabled: bool


@router.post(
    "/create",
    dependencies=[Depends(JWTBearer())]
)
async def create_limit(

    payload: LimitSchema,

    token=Depends(JWTBearer())

):

    user_id = token["user_id"]

    billing_cycle = get_billing_cycle()

    conn = await get_connection()

    try:

        # ===================
        # Check Existing Limit
        # ===================

        cursor = await conn.execute(
            '''
            SELECT *

            FROM spending_limits

            WHERE user_id = ?

            AND billing_cycle = ?
            ''',
            (
                user_id,
                billing_cycle
            )
        )

        existing_limit = (
            await cursor.fetchone()
        )

        # ===================
        # Update Existing
        # ===================

        if existing_limit:

            await conn.execute(
                '''
                UPDATE spending_limits

                SET

                    upi_limit=?,

                    credit_limit=?,

                    card_no=?,

                    account_no=?,

                    atm_enabled=?,

                    online_enabled=?

                WHERE user_id=?

                AND billing_cycle=?
                ''',
                (

                    payload.upi_limit,

                    payload.credit_limit,

                    payload.card_no,

                    payload.account_no,

                    int(
                        payload.atm_enabled
                    ),

                    int(
                        payload.online_enabled
                    ),

                    user_id,

                    billing_cycle

                )
            )

        # ===================
        # Insert New
        # ===================

        else:

            await conn.execute(
                '''
                INSERT INTO spending_limits(

                    user_id,

                    upi_limit,

                    credit_limit,

                    card_no,

                    account_no,

                    atm_enabled,

                    online_enabled,

                    billing_cycle

                )

                VALUES(

                    ?, ?, ?, ?, ?, ?, ?, ?

                )
                ''',
                (

                    user_id,

                    payload.upi_limit,

                    payload.credit_limit,

                    payload.card_no,

                    payload.account_no,

                    int(
                        payload.atm_enabled
                    ),

                    int(
                        payload.online_enabled
                    ),

                    billing_cycle

                )
            )

        await conn.commit()

        await conn.close()

        return {

            "message":
            "Spending limit saved",

            "billing_cycle":
            billing_cycle

        }

    except Exception as e:

        await conn.close()

        raise e