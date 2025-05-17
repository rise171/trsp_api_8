from sqlalchemy import INTEGER, VARCHAR, Enum
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

class RoleEnum(PyEnum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum))
    age: Mapped[int] = mapped_column(INTEGER)