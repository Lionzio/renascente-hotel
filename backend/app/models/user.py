# backend/app/models/user.py
import enum
import uuid
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class UserRole(str, enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    SUPER_ADMIN = "SUPER_ADMIN"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(
        String, unique=True, index=True, nullable=False
    )  # O Nome agora é a chave de login
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
