from sqlalchemy import Column, String, Integer, ForeignKey

from database import Base
from models.Users import Users


class Recipes(Base) :
    __tablename__ = "Recipes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(128),
        nullable=False
    )

    duration = Column(
        Integer,
        nullable=False
    )

    nbPersons = Column(
        Integer,
        nullable=False
    )

    ownerId = Column(
        Integer,
        ForeignKey(Users.id)
    )