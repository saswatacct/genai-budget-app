# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException
# )

# from app.auth.auth_bearer import (
#     JWTBearer
# )

# from app.db.database import (
#     get_connection
# )

# router = APIRouter(
#     prefix="/transaction"
# )


# @router.delete(
#     "/delete/{transaction_id}",
#     dependencies=[Depends(JWTBearer())]
# )
# def delete_transaction(
#     transaction_id: int,
#     token=Depends(JWTBearer())
# ):

#     user_id = token["user_id"]

#     conn = get_connection()

#     cursor = conn.cursor()

#     transaction = cursor.execute(
#         '''
#         SELECT *

#         FROM transactions

#         WHERE id = ?
#         AND user_id = ?
#         AND is_deleted = 0
#         ''',
#         (
#             transaction_id,
#             user_id
#         )
#     ).fetchone()

#     if not transaction:

#         conn.close()

#         raise HTTPException(
#             status_code=404,
#             detail="Transaction not found"
#         )

#     cursor.execute(
#         '''
#         UPDATE transactions

#         SET is_deleted = 1

#         WHERE id = ?
#         ''',
#         (transaction_id,)
#     )

#     conn.commit()

#     conn.close()

#     return {
#         "message": "Transaction deleted successfully"
#     }




from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.auth_bearer import (
    JWTBearer
)

from app.db.database import (
    get_connection
)


router = APIRouter(
    prefix="/transaction"
)


@router.delete(
    "/delete/{transaction_id}",
    dependencies=[Depends(JWTBearer())]
)
async def delete_transaction(

    transaction_id: int,

    token=Depends(JWTBearer())

):

    user_id = token["user_id"]

    conn = await get_connection()

    try:

        # ==================
        # Validate Ownership
        # ==================

        cursor = await conn.execute(
            '''
            SELECT *

            FROM transactions

            WHERE id = ?

            AND user_id = ?

            AND is_deleted = 0
            ''',
            (
                transaction_id,
                user_id
            )
        )

        transaction = (
            await cursor.fetchone()
        )

        if not transaction:

            await conn.close()

            raise HTTPException(

                status_code=404,

                detail=(
                    "Transaction "
                    "not found"
                )

            )

        # ==================
        # Soft Delete
        # ==================

        await conn.execute(
            '''
            UPDATE transactions

            SET is_deleted = 1

            WHERE id = ?
            ''',
            (
                transaction_id,
            )
        )

        await conn.commit()

        await conn.close()

        return {

            "message":
            "Transaction deleted successfully"

        }

    except HTTPException as e:

        await conn.close()

        raise e

    except Exception as e:

        await conn.close()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )