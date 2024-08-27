"""Database entity classes. For each change here there must be a corresponding alembic migration."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SomeEntity(Base):
    """An entity class representing a table in the database"""

    __tablename__ = "some_entity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    def __eq__(self, other):
        return self.name == other.name and self.is_active == other.is_active
