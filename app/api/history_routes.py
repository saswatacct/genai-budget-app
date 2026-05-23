# from fastapi import (
#     APIRouter,
#     Depends
# )

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
#     prefix="/history"
# )


# @router.get(
#     "/transactions",
#     dependencies=[Depends(JWTBearer())]
# )
# def get_transactions(
#     token=Depends(JWTBearer())
# ):

#     user_id = token["user_id"]

#     billing_cycle = get_billing_cycle()

#     conn = get_connection()

#     cursor = conn.cursor()

#     transactions = cursor.execute(
#         '''
#         SELECT
#             id,
#             amount,
#             merchant,
#             txn_mode,
#             payment_mode,
#             created_at

#         FROM transactions

#         WHERE user_id = ?
#         AND billing_cycle = ?
#         AND is_deleted = 0

#         ORDER BY created_at DESC
#         ''',
#         (
#             user_id,
#             billing_cycle
#         )
#     ).fetchall()

#     conn.close()

#     return {
#         "transactions": [
#             dict(txn)
#             for txn in transactions
#         ]
#     }


from fastapi import (
    APIRouter,
    Depends
)

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
    prefix="/history"
)


@router.get(
    "/transactions",
    dependencies=[Depends(JWTBearer())]
)
async def get_transactions(

    token=Depends(JWTBearer())

):

    user_id = token["user_id"]

    billing_cycle = get_billing_cycle()

    conn = await get_connection()

    try:

        cursor = await conn.execute(
            '''
            SELECT

                id,

                amount,

                merchant,

                txn_mode,

                payment_mode,

                created_at

            FROM transactions

            WHERE user_id = ?

            AND billing_cycle = ?

            AND is_deleted = 0

            ORDER BY created_at DESC
            ''',
            (
                user_id,
                billing_cycle
            )
        )

        transactions = (
            await cursor.fetchall()
        )

        await conn.close()

        return {

            "transactions": [

                dict(txn)

                for txn in transactions

            ]

        }

    except Exception as e:

        await conn.close()

        raise e