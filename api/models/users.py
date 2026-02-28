from schemas.user_schema import UserRole
from sqlmodel import Field, SQLModel


# Model database User.
# Setiap class = tabel, setiap field = kolom.
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    role: UserRole = Field(sa_column_kwargs={"nullable": False})
