# backend/app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_name(db: Session, name: str) -> User:
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        db_user = User(
            name=user_in.name,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def delete_user(db: Session, user_id: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
