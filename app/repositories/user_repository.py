from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(
        self,
        email: str,
        hashed_password: str,
        is_active: bool = True,
        role: str = "user",
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_active=is_active,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def email_exists(self, email: str) -> bool:
        return self.get_user_by_email(email) is not None
