# from app.db.database import (
#     get_connection
# )

# def create_tables():

#     conn = get_connection()

#     cursor = conn.cursor()

#     cursor.execute(
#         '''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             email TEXT UNIQUE,
#             password TEXT,
#             phone TEXT
#         )
#         '''
#     )

#     cursor.execute(
#     '''
#     CREATE TABLE IF NOT EXISTS spending_limits (

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER,

#         upi_limit REAL,

#         credit_limit REAL,

#         card_no TEXT,

#         account_no TEXT,

#         atm_enabled INTEGER,

#         online_enabled INTEGER,

#         billing_cycle TEXT
#     )
#     '''
# )

#     cursor.execute(
#     '''
#     CREATE TABLE IF NOT EXISTS transactions (

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER,

#         amount REAL,

#         merchant TEXT,

#         txn_mode TEXT,

#         payment_mode TEXT,

#         billing_cycle TEXT,

#         is_deleted INTEGER DEFAULT 0,

#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     '''
# )

#     conn.commit()

#     conn.close()



from app.db.database import (
    get_connection
)


async def create_tables():

    conn = await get_connection()

    try:

        # ==================
        # USERS
        # ==================

        await conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                email TEXT UNIQUE,

                password TEXT,

                phone TEXT

            )
            '''
        )

        # ==================
        # SPENDING LIMITS
        # ==================

        await conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS spending_limits(

                id INTEGER
                PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                upi_limit REAL,

                credit_limit REAL,

                card_no TEXT,

                account_no TEXT,

                atm_enabled INTEGER,

                online_enabled INTEGER,

                billing_cycle TEXT

            )
            '''
        )

        # ==================
        # TRANSACTIONS
        # ==================

        await conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS transactions(

                id INTEGER
                PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                amount REAL,

                merchant TEXT,

                txn_mode TEXT,

                payment_mode TEXT,

                billing_cycle TEXT,

                is_deleted INTEGER
                DEFAULT 0,

                created_at TIMESTAMP
                DEFAULT (

                    datetime(

                        'now',

                        '+5 hours',

                        '+30 minutes'

                    )

                )

            )
            '''
        )

        await conn.commit()

        await conn.close()

    except Exception:

        await conn.close()

        raise