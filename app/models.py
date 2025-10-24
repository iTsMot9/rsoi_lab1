from sqlalchemy import Column, Integer, String, CheckConstraint
from .database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    work = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint('age >= 0', name='age_positive'),
        CheckConstraint('age <= 150', name='age_not_too_old'),
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"
