# import sqlite3


# DATABASE_NAME = "budget.db"


# def get_connection():

#     conn = sqlite3.connect(
#         DATABASE_NAME
#     )

#     conn.row_factory = sqlite3.Row

#     return conn



import aiosqlite


DATABASE_NAME = "budget.db"


async def get_connection():

    conn = await aiosqlite.connect(
        DATABASE_NAME
    )

    conn.row_factory = aiosqlite.Row

    return conn