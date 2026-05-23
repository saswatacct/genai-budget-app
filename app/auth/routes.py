# from fastapi import (
#     APIRouter,
#     HTTPException
# )

# from pydantic import BaseModel

# from app.db.database import (
#     get_connection
# )

# from app.auth.password_handler import (
#     hash_password,
#     verify_password
# )

# from app.auth.jwt_handler import (
#     create_access_token
# )

# router = APIRouter(
#     prefix="/auth"
# )


# class SignupSchema(BaseModel):

#     name: str

#     email: str

#     password: str

#     phone: str


# class LoginSchema(BaseModel):

#     email: str

#     password: str


# @router.post("/signup")
# def signup(payload: SignupSchema):

#     conn = get_connection()

#     cursor = conn.cursor()

#     existing_user = cursor.execute(
#         '''
#         SELECT * FROM users
#         WHERE email = ?
#         ''',
#         (payload.email,)
#     ).fetchone()

#     if existing_user:

#         raise HTTPException(
#             status_code=400,
#             detail="User already exists"
#         )

#     hashed_password = hash_password(
#         payload.password
#     )

#     cursor.execute(
#         '''
#         INSERT INTO users (
#             name,
#             email,
#             password,
#             phone
#         )
#         VALUES (?, ?, ?, ?)
#         ''',
#         (
#             payload.name,
#             payload.email,
#             hashed_password,
#             payload.phone
#         )
#     )

#     conn.commit()

#     user_id = cursor.lastrowid

#     conn.close()

#     token = create_access_token({
#         "user_id": user_id
#     })

#     return {
#         "message": "Signup successful",
#         "access_token": token
#     }


# @router.post("/login")
# def login(payload: LoginSchema):

#     conn = get_connection()

#     cursor = conn.cursor()

#     user = cursor.execute(
#         '''
#         SELECT * FROM users
#         WHERE email = ?
#         ''',
#         (payload.email,)
#     ).fetchone()

#     conn.close()

#     if not user:

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials"
#         )

#     valid = verify_password(
#         payload.password,
#         user["password"]
#     )

#     if not valid:

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials"
#         )

#     token = create_access_token({
#         "user_id": user["id"]
#     })

#     return {
#         "message": "Login successful",
#         "access_token": token
#     }




# from fastapi import (
#     APIRouter,
#     HTTPException
# )

# from pydantic import BaseModel

# from app.db.database import (
#     get_connection
# )

# from app.auth.password_handler import (
#     hash_password,
#     verify_password
# )

# from app.auth.jwt_handler import (
#     create_access_token
# )


# router = APIRouter(
#     prefix="/auth"
# )


# class SignupSchema(BaseModel):

#     name: str

#     email: str

#     password: str

#     phone: str


# class LoginSchema(BaseModel):

#     email: str

#     password: str


# @router.post("/signup")
# async def signup(

#     payload: SignupSchema

# ):

#     conn = await get_connection()

#     try:

#         # ==================
#         # Existing User Check
#         # ==================

#         cursor = await conn.execute(
#             '''
#             SELECT *

#             FROM users

#             WHERE email = ?
#             ''',
#             (
#                 payload.email,
#             )
#         )

#         existing_user = (
#             await cursor.fetchone()
#         )

#         if existing_user:

#             await conn.close()

#             raise HTTPException(

#                 status_code=400,

#                 detail=(
#                     "User already exists"
#                 )

#             )

#         # ==================
#         # Password Hash
#         # ==================

#         hashed_password = (
#             hash_password(
#                 payload.password
#             )
#         )

#         # ==================
#         # Insert User
#         # ==================

#         cursor = await conn.execute(
#             '''
#             INSERT INTO users(

#                 name,

#                 email,

#                 password,

#                 phone

#             )

#             VALUES(

#                 ?, ?, ?, ?

#             )
#             ''',
#             (

#                 payload.name,

#                 payload.email,

#                 hashed_password,

#                 payload.phone

#             )
#         )

#         await conn.commit()

#         user_id = (
#             cursor.lastrowid
#         )

#         await conn.close()

#         token = (
#             create_access_token({

#                 "user_id":
#                 user_id

#             })
#         )

#         return {

#             "message":
#             "Signup successful",

#             "access_token":
#             token

#         }

#     except HTTPException as e:

#         await conn.close()

#         raise e

#     except Exception as e:

#         await conn.close()

#         raise HTTPException(

#             status_code=500,

#             detail=str(e)

#         )


# @router.post("/login")
# async def login(

#     payload: LoginSchema

# ):

#     conn = await get_connection()

#     try:

#         cursor = await conn.execute(
#             '''
#             SELECT *

#             FROM users

#             WHERE email = ?
#             ''',
#             (
#                 payload.email,
#             )
#         )

#         user = (
#             await cursor.fetchone()
#         )

#         await conn.close()

#         if not user:

#             raise HTTPException(

#                 status_code=401,

#                 detail=(
#                     "Invalid credentials"
#                 )

#             )

#         valid = verify_password(

#             payload.password,

#             user["password"]

#         )

#         if not valid:

#             raise HTTPException(

#                 status_code=401,

#                 detail=(
#                     "Invalid credentials"
#                 )

#             )

#         token = (
#             create_access_token({

#                 "user_id":
#                 user["id"]

#             })
#         )

#         return {

#             "message":
#             "Login successful",

#             "access_token":
#             token

#         }

#     except HTTPException as e:

#         raise e

#     except Exception as e:

#         raise HTTPException(

#             status_code=500,

#             detail=str(e)

#         )




from fastapi import (
    APIRouter,
    HTTPException,
    BackgroundTasks
)

from pydantic import BaseModel

from app.db.database import (
    get_connection
)

from app.auth.password_handler import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)

from app.whatsapp.service import (
    send_whatsapp
)

from app.auth.reset_token_store import (

    create_reset_token,

    validate_token,

    remove_token

)


router = APIRouter(
    prefix="/auth"
)


# =========================
# SCHEMAS
# =========================

class SignupSchema(
    BaseModel
):

    name: str

    email: str

    password: str

    phone: str


class LoginSchema(
    BaseModel
):

    email: str

    password: str


class ForgotPasswordSchema(
    BaseModel
):

    email: str


class ResetPasswordSchema(
    BaseModel
):

    token: str

    password: str


# =========================
# SIGNUP
# =========================

@router.post(
    "/signup"
)
async def signup(

    payload: SignupSchema

):

    conn = await get_connection()

    try:

        cursor = await conn.execute(
            '''
            SELECT *

            FROM users

            WHERE email=?
            ''',
            (
                payload.email,
            )
        )

        existing_user = (
            await cursor.fetchone()
        )

        if existing_user:

            await conn.close()

            raise HTTPException(

                status_code=400,

                detail=(
                    "User already exists"
                )

            )

        hashed_password = (
            hash_password(
                payload.password
            )
        )

        cursor = await conn.execute(
            '''
            INSERT INTO users(

                name,

                email,

                password,

                phone

            )

            VALUES(

                ?, ?, ?, ?

            )
            ''',
            (

                payload.name,

                payload.email,

                hashed_password,

                payload.phone

            )
        )

        await conn.commit()

        user_id = (
            cursor.lastrowid
        )

        await conn.close()

        token = (
            create_access_token({

                "user_id":
                user_id

            })
        )

        return {

            "message":
            "Signup successful",

            "access_token":
            token

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


# =========================
# LOGIN
# =========================

@router.post(
    "/login"
)
async def login(

    payload: LoginSchema

):

    conn = await get_connection()

    try:

        cursor = await conn.execute(
            '''
            SELECT *

            FROM users

            WHERE email=?
            ''',
            (
                payload.email,
            )
        )

        user = (
            await cursor.fetchone()
        )

        await conn.close()

        if not user:

            raise HTTPException(

                status_code=401,

                detail=(
                    "Invalid credentials"
                )

            )

        valid = verify_password(

            payload.password,

            user["password"]

        )

        if not valid:

            raise HTTPException(

                status_code=401,

                detail=(
                    "Invalid credentials"
                )

            )

        token = (
            create_access_token({

                "user_id":
                user["id"]

            })
        )

        return {

            "message":
            "Login successful",

            "access_token":
            token

        }

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =========================
# FORGOT PASSWORD
# =========================

@router.post(
    "/forgot-password"
)
async def forgot_password(

    payload:
    ForgotPasswordSchema,

    background_tasks:
    BackgroundTasks

):

    conn = await get_connection()

    try:

        cursor = await conn.execute(
            '''
            SELECT *

            FROM users

            WHERE email=?
            ''',
            (
                payload.email,
            )
        )

        user = (
            await cursor.fetchone()
        )

        await conn.close()

        if not user:

            return {

                "message":
                (
                    "If account exists "
                    "notification sent"
                )

            }

        token = (
            create_reset_token(
                payload.email
            )
        )

        reset_link = (

            "http://localhost:3000"

            f"/reset-password"

            f"?token={token}"

        )

        message = f"""

Hello {user['name']},

🔐 SmartSpend Password Reset

Please click below link:

{reset_link}

⏳ Valid for 5 minutes.

If not requested by you,
ignore this message.

SmartSpend AI Team

"""

        background_tasks.add_task(

            send_whatsapp,

            user["phone"],

            message

        )

        return {

            "message":
            (
                "Reset link sent "
                "to WhatsApp"
            )

        }

    except Exception as e:

        await conn.close()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =========================
# RESET PASSWORD
# =========================

@router.post(
    "/reset-password"
)
async def reset_password(

    payload:
    ResetPasswordSchema

):

    email = (
        validate_token(
            payload.token
        )
    )

    if not email:

        raise HTTPException(

            status_code=400,

            detail=
            (
                "Invalid or "
                "expired token"
            )

        )

    conn = await get_connection()

    try:

        new_hash = (
            hash_password(
                payload.password
            )
        )

        await conn.execute(
            '''
            UPDATE users

            SET password=?

            WHERE email=?
            ''',
            (
                new_hash,
                email
            )
        )

        await conn.commit()

        await conn.close()

        remove_token(
            payload.token
        )

        return {

            "message":
            "Password updated"

        }

    except Exception as e:

        await conn.close()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )