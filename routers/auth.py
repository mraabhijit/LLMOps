import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from database import get_db

router = APIRouter()
security = HTTPBearer()


def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    conn = get_db()
    cursor = conn.cursor()

    # Verify token
    cursor.execute("SELECT email FROM tokens WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = row["email"]

    # Ensure user is not deleted
    cursor.execute("SELECT deleted FROM users WHERE email = ?", (email,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row or user_row["deleted"] == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account does not have necessary privileges.",
        )

    return email


class UserAuth(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: UserAuth):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    # the deleted field relies on DEFAULT 0, so it's transparent and protected
    cursor.execute(
        "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
        (user.email, hashed_password),
    )
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserAuth):
    conn = get_db()
    cursor = conn.cursor()
    hashed_password = get_password_hash(user.password)

    cursor.execute(
        "SELECT hashed_password, deleted FROM users WHERE email = ?", (user.email,)
    )
    row = cursor.fetchone()

    if not row or row["hashed_password"] != hashed_password:
        conn.close()
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if row["deleted"] == 1:
        conn.close()
        raise HTTPException(status_code=403, detail="Account is disabled or deleted")

    token = secrets.token_hex(32)
    cursor.execute(
        "INSERT INTO tokens (token, email) VALUES (?, ?)", (token, user.email)
    )
    conn.commit()
    conn.close()

    return {"access_token": token, "token_type": "bearer"}
