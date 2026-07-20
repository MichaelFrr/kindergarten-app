from backend.database import Base
import uuid
from sqlalchemy import Integer, String, text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional


class User(Base):
    __tablename__ = "users"
    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100), default="parent")
