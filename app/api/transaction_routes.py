# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException
# )

# from pydantic import BaseModel

# from datetime import datetime

# from app.auth.auth_bearer import (
#     JWTBearer
# )

# from app.db.database import (
#     get_connection
# )

# from app.services.analytics import (
#     calculate_metrics
# )

# from app.ai.groq_service import (
#     generate_financial_suggestion
# )

# from app.services.message_builder import (
#     build_message
# )

# from app.whatsapp.service import (
#     send_whatsapp
# )

# from app.utils.billing_cycle import (
#     get_billing_cycle
# )

# router = APIRouter(
#     prefix="/transaction"
# )


# class TransactionSchema(BaseModel):

#     amount: float

#     merchant: str

#     txn_mode: str

#     payment_mode: str


# @router.post(
#     "/add",
#     dependencies=[Depends(JWTBearer())]
# )
# def add_transaction(
#     payload: TransactionSchema,
#     token=Depends(JWTBearer())
# ):

#     user_id = token["user_id"]

#     billing_cycle = get_billing_cycle()

#     conn = get_connection()

#     cursor = conn.cursor()

#     try:

#         # Duplicate Detection
#         duplicate_txn = cursor.execute(
#             '''
#             SELECT *

#             FROM transactions

#             WHERE user_id = ?
#             AND amount = ?
#             AND merchant = ?
#             AND billing_cycle = ?
#             AND is_deleted = 0
#             AND datetime(created_at)
#                 >= datetime('now', '-2 minutes')
#             ''',
#             (
#                 user_id,
#                 payload.amount,
#                 payload.merchant,
#                 billing_cycle
#             )
#         ).fetchone()

#         if duplicate_txn:

#             raise HTTPException(
#                 status_code=400,
#                 detail="Possible duplicate transaction detected"
#             )

#         # Insert Transaction
#         cursor.execute(
#             '''
#             INSERT INTO transactions (
#                 user_id,
#                 amount,
#                 merchant,
#                 txn_mode,
#                 payment_mode,
#                 billing_cycle
#             )
#             VALUES (?, ?, ?, ?, ?, ?)
#             ''',
#             (
#                 user_id,
#                 payload.amount,
#                 payload.merchant,
#                 payload.txn_mode,
#                 payload.payment_mode,
#                 billing_cycle
#             )
#         )

#         conn.commit()

#         # Monthly Total Spend
#         total_spent_data = cursor.execute(
#             '''
#             SELECT SUM(amount) AS total

#             FROM transactions

#             WHERE user_id = ?
#             AND billing_cycle = ?
#             AND is_deleted = 0
#             ''',
#             (
#                 user_id,
#                 billing_cycle
#             )
#         ).fetchone()

#         total_spent = (
#             total_spent_data["total"]
#             if total_spent_data["total"]
#             else 0
#         )

#         print("TOTAL SPENT:", total_spent)

#         # Monthly Spending Limit
#         limit_data = cursor.execute(
#             '''
#             SELECT *

#             FROM spending_limits

#             WHERE user_id = ?
#             AND billing_cycle = ?
#             ''',
#             (
#                 user_id,
#                 billing_cycle
#             )
#         ).fetchone()

#         if not limit_data:

#             raise HTTPException(
#                 status_code=404,
#                 detail=f"No spending limit configured for cycle {billing_cycle}"
#             )

#         # Dynamic Day Calculation
#         current_day = datetime.now().day

#         days_left = max(
#             30 - current_day,
#             1
#         )

#         # Calculate Metrics
#         metrics = calculate_metrics(
#             limit_data["credit_limit"],
#             total_spent,
#             current_day
#         )

#         # Generate AI Suggestion
#         suggestion = generate_financial_suggestion({

#             "total_limit": limit_data["credit_limit"],

#             "remaining": metrics["remaining"],

#             "avg_daily": metrics["avg_daily"],

#             "days_left": days_left
#         })

#         print("AI SUGGESTION:", suggestion)

#         # Get User
#         user = cursor.execute(
#             '''
#             SELECT *

#             FROM users

#             WHERE id = ?
#             ''',
#             (user_id,)
#         ).fetchone()

#         if not user:

#             raise HTTPException(
#                 status_code=404,
#                 detail="User not found"
#             )

#         # Build WhatsApp Message
#         message = build_message({

#         "user_name": user["name"],

#         "billing_cycle": billing_cycle,

#         "upi_limit": limit_data["upi_limit"],

#         "credit_limit": limit_data["credit_limit"],

#         "atm_flag": bool(
#             limit_data["atm_enabled"]
#         ),

#         "online_flag": bool(
#             limit_data["online_enabled"]
#         ),

#         "amount": payload.amount,

#         "merchant": payload.merchant,

#         "txn_mode": payload.txn_mode,

#         "alert": metrics["alert"],

#         "avg_daily": metrics["avg_daily"],

#         "suggestion": suggestion
#     })

#         print("WHATSAPP MESSAGE:")
#         print(message)

#         # Send WhatsApp
#         whatsapp_sid = send_whatsapp(
#             user["phone"],
#             message
#         )

#         print("WHATSAPP SID:", whatsapp_sid)

#         conn.close()

#         return {

#             "message": "Transaction added successfully",

#             "billing_cycle": billing_cycle,

#             "metrics": metrics,

#             "ai_suggestion": suggestion,

#             "whatsapp_status": "sent"
#         }

#     except HTTPException as e:

#         conn.close()

#         raise e

#     except Exception as e:

#         conn.close()

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )
    



from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from pydantic import BaseModel

from datetime import datetime

from app.auth.auth_bearer import (
    JWTBearer
)

from app.db.database import (
    get_connection
)

from app.services.analytics import (
    calculate_metrics
)

from app.ai.groq_service import (
    generate_financial_suggestion
)

from app.services.message_builder import (
    build_message
)

from app.whatsapp.service import (
    send_whatsapp
)

from app.utils.billing_cycle import (
    get_billing_cycle
)


router = APIRouter(
    prefix="/transaction"
)


class TransactionSchema(BaseModel):

    amount: float

    merchant: str

    txn_mode: str

    payment_mode: str


@router.post(
    "/add",
    dependencies=[Depends(JWTBearer())]
)
async def add_transaction(

    payload: TransactionSchema,

    background_tasks: BackgroundTasks,

    token=Depends(JWTBearer())

):

    user_id = token["user_id"]

    billing_cycle = get_billing_cycle()

    conn = await get_connection()

    try:

        # ====================
        # Duplicate Detection
        # ====================

        cursor = await conn.execute(
            '''
            SELECT *

            FROM transactions

            WHERE user_id = ?

            AND amount = ?

            AND merchant = ?

            AND billing_cycle = ?

            AND is_deleted = 0

            AND datetime(created_at)
            >= datetime('now','-2 minutes')
            ''',
            (
                user_id,
                payload.amount,
                payload.merchant,
                billing_cycle
            )
        )

        duplicate_txn = await cursor.fetchone()

        if duplicate_txn:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Possible duplicate "
                    "transaction detected"
                )
            )

        # ====================
        # Insert Transaction
        # ====================

        await conn.execute(
            '''
            INSERT INTO transactions(

                user_id,

                amount,

                merchant,

                txn_mode,

                payment_mode,

                billing_cycle

            )

            VALUES(

                ?, ?, ?, ?, ?, ?

            )
            ''',
            (
                user_id,

                payload.amount,

                payload.merchant,

                payload.txn_mode,

                payload.payment_mode,

                billing_cycle
            )
        )

        await conn.commit()

        # ====================
        # Monthly Spend
        # ====================

        cursor = await conn.execute(
            '''
            SELECT SUM(amount)
            AS total

            FROM transactions

            WHERE user_id=?

            AND billing_cycle=?

            AND is_deleted=0
            ''',
            (
                user_id,
                billing_cycle
            )
        )

        total_spent_data = await cursor.fetchone()

        total_spent = (

            total_spent_data["total"]

            if total_spent_data["total"]

            else 0

        )

        # ====================
        # Limit Data
        # ====================

        cursor = await conn.execute(
            '''
            SELECT *

            FROM spending_limits

            WHERE user_id=?

            AND billing_cycle=?
            ''',
            (
                user_id,
                billing_cycle
            )
        )

        limit_data = await cursor.fetchone()

        if not limit_data:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No spending limit "
                    f"configured for "
                    f"{billing_cycle}"
                )
            )

        # ====================
        # Metrics
        # ====================

        current_day = datetime.now().day

        days_left = max(
            30-current_day,
            1
        )

        metrics = calculate_metrics(

            limit_data["credit_limit"],

            total_spent,

            current_day

        )

        # ====================
        # AI Suggestion
        # ====================

        suggestion = (
            generate_financial_suggestion({

                "total_limit":
                limit_data["credit_limit"],

                "remaining":
                metrics["remaining"],

                "avg_daily":
                metrics["avg_daily"],

                "days_left":
                days_left

            })
        )

        # ====================
        # User
        # ====================

        cursor = await conn.execute(
            '''
            SELECT *

            FROM users

            WHERE id=?
            ''',
            (user_id,)
        )

        user = await cursor.fetchone()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # ====================
        # Build Message
        # ====================

        message = build_message({

            "user_name":
            user["name"],

            "billing_cycle":
            billing_cycle,

            "upi_limit":
            limit_data["upi_limit"],

            "credit_limit":
            limit_data["credit_limit"],

            "atm_flag":
            bool(
                limit_data["atm_enabled"]
            ),

            "online_flag":
            bool(
                limit_data["online_enabled"]
            ),

            "amount":
            payload.amount,

            "merchant":
            payload.merchant,

            "txn_mode":
            payload.txn_mode,

            "alert":
            metrics["alert"],

            "avg_daily":
            metrics["avg_daily"],

            "suggestion":
            suggestion

        })

        # ====================
        # Async WhatsApp
        # ====================

        background_tasks.add_task(

            send_whatsapp,

            user["phone"],

            message

        )

        await conn.close()

        return {

            "message":
            "Transaction added successfully",

            "billing_cycle":
            billing_cycle,

            "metrics":
            metrics,

            "ai_suggestion":
            suggestion,

            "whatsapp_status":
            "queued"

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