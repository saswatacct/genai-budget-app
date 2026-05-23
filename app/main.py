# from fastapi import FastAPI

# from app.db.init_db import (
#     create_tables
# )

# from app.auth.routes import (
#     router as auth_router
# )

# from app.api.transaction_routes import (
#     router as transaction_router
# )

# from app.api.limit_routes import (
#     router as limit_router
# )

# from app.api.history_routes import (
#     router as history_router
# )

# from app.api.delete_transaction_routes import (
#     router as delete_transaction_router
# )

# app = FastAPI(
#     title="GenAI Budget Assistant"
# )

# create_tables()

# app.include_router(auth_router)

# app.include_router(transaction_router)

# app.include_router(limit_router)

# app.include_router(history_router)

# app.include_router(delete_transaction_router)


# @app.get("/")
# def home():

#     return {
#         "message": "Application Running"
#     }




from fastapi import FastAPI

from app.db.init_db import (
    create_tables
)

from app.auth.routes import (
    router as auth_router
)

from app.api.transaction_routes import (
    router as transaction_router
)

from app.api.limit_routes import (
    router as limit_router
)

from app.api.history_routes import (
    router as history_router
)

from app.api.delete_transaction_routes import (
    router as delete_transaction_router
)


app = FastAPI(

    title="GenAI Budget Assistant"

)


# ==========================
# STARTUP EVENT
# ==========================

@app.on_event("startup")
async def startup():

    await create_tables()


# ==========================
# ROUTERS
# ==========================

app.include_router(
    auth_router
)

app.include_router(
    transaction_router
)

app.include_router(
    limit_router
)

app.include_router(
    history_router
)

app.include_router(
    delete_transaction_router
)


# ==========================
# HEALTH CHECK
# ==========================

@app.get("/")
async def home():

    return {

        "message":
        "Application Running"

    }