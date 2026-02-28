import os

from auth import (
    admin_only,
    create_token,
    get_current_user,
    hash_password,
    superadmin_only,
    verify_password,
)
from database import create_db_and_tables, get_session
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User
from schemas.user_schema import LoginRequest, LoginResponse, User, UserCreate
from sqlmodel import Session, and_, select

load_dotenv()

# Dummy user
SA_EMAIL = os.getenv("SA_EMAIL")
SA_PASSWORD = os.getenv("SA_PASSWORD")

# Membuat objek router.
router = APIRouter(tags=["Users"])


@router.on_event("startup")
def startup_event():
    create_db_and_tables()


@router.get("/users")
def get_users(
    name: str | None = None,
    role: str | None = None,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):

    statement = select(User)
    filters = []
    if name:
        filters.append(User.name.ilike(f"%{name}%"))
    if role:
        filters.append(User.role.contains(role.lower()))
    if filters:
        statement = statement.where(and_(*filters))

    return session.exec(statement).all()


@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):
    # Cari user berdasarkan id
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"User dengan id {user_id} tidak ditemukan.",
        )
    return result


@router.post("/users")
def create_user(
    new_user: UserCreate,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):
    # 1) cek apakah nama sudah ada (cek duplikasi)
    statement = select(User).where(User.email == new_user.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Nama user sudah dipakai.")

    hashed_pw = hash_password(new_user.password)

    user = User(
        name=new_user.name,
        email=new_user.email,
        password_hash=hashed_pw,
        role=new_user.role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.patch("/users/{user_id}")
def update_user(
    user_id: int,
    new_data: UserCreate,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):
    # 1) cari user dulu berdasarkan id
    user = session.get(User, user_id)

    # jika tidak ada, raise error 404
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")

    # 2) update field yang mau diubah
    user.name = new_data.name

    # 3) simpan perubahan ke database
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_admin=Depends(superadmin_only),
):
    # 1) cari user berdasarkan id
    user = session.get(User, user_id)

    # jika tidak ada, kasih error 404
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")

    # 2) hapus user dari database
    session.delete(user)
    session.commit()

    return {"message": f"User dengan id {user_id} berhasil dihapus."}


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    # current_user adalah payload dari token
    return {
        "message": "Ini endpoint yang dilindungi.",
        "user_data": current_user,
    }


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    if login_data.email == SA_EMAIL or login_data.password == SA_PASSWORD:
        role = "superadmin"
        userid = -1
    else:
        statement = select(User).where(User.email == login_data.email)
        user = session.exec(statement).first()
        role = user.role
        userid = user.id

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah.",
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah.",
            )

    token = create_token({"user_id": userid, "role": role})

    return LoginResponse(
        access_token=token, token_type="bearer", user_id=userid, role=role
    )


@router.get("/admin/dashboard")
def admin_dashboard(current_admin=Depends(admin_only)):
    return {
        "message": f"Selamat datang {current_admin['role']}!",
        "admin_data": current_admin,
    }
