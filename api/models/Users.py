from sqlalchemy import Column, String, Integer

from database import Base


class Users(Base) :
    __tablename__ = "Users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(32),
        unique=True,
        nullable=False
    )

    email = Column(
        String(256),
        unique=True,
        nullable=False
    )

    hashedPassword = Column(
        String(128),
        nullable=False
    )