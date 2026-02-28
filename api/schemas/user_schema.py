from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    public = "public"
    admin = "admin"


class User(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, description="Minimal 6 karakter.")
    role: UserRole


class UserCreate(BaseModel):
    name: str = Field(
        ...,  # berarti wajib
        min_length=3,  # minimal 3 karakter
        max_length=50,  # maksimal 50 karakter
        description="Nama harus antara 3 hingga 50 karakter.",
    )
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, description="Minimal 6 karakter.")
    role: UserRole = Field(
        ..., description="Role user hanya boleh: public, admin"
    )


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
