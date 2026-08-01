from backend.database import Base
import uuid
from sqlalchemy import Integer, String, text, UUID, ForeignKey, Date
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

class Child(Base):
    __tablename__ = "children"
    uuid: Mapped[uuid.UUID] = mapped_column(
            UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    parent_uuid: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.uuid"))
    parent_email: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.email"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    grade: Mapped[str] = mapped_column(String(100))
    membership_date: Mapped[Date] = mapped_column(Date, nullable=False)

class Classroom(Base):
    __tablename__ = "classrooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer)