from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)


def create_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # berisi data user, misalnya user_id
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401, detail="Token tidak valid atau expired."
        )
    return payload


def admin_only(current_user=Depends(get_current_user)):
    # current_user ini payload token
    if current_user.get("role") not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=403, detail="Endpoint ini khusus admin."
        )
    return current_user


def superadmin_only(current_user=Depends(get_current_user)):
    # current_user ini payload token
    if current_user.get("role") != "superadmin":
        raise HTTPException(
            status_code=403, detail="Endpoint ini khusus admin."
        )
    return current_user
