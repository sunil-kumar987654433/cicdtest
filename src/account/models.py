from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, Uuid, UUID, Enum as SqlEnum, Boolean, DateTime
from src.db.database import Base
import uuid
from enum import Enum
from datetime import datetime, timezone, timedelta


class UserRole(str, Enum):
    customer = 'customer'
    admin = 'admin'
    saler = 'saler'





class User(Base):
    __tablename__ = "account_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), default=uuid.uuid4, unique=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    user_role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.customer, nullable=False)
    user_image: Mapped[str] = mapped_column(String(500), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )
    
    @property
    def profile_image(self)->str:
        if self.user_image is None:
            return "/static/profile/user.png"
        return f'/media/profile/{self.user_image}'

    


class UserBlackListToken(Base):
    __tablename__ = "account_user_blacklist_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), default=uuid.uuid4, unique=True)
    user_uid: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("account_users.key"), index=True)
    jti_token: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )