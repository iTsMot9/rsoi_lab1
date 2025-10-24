from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from . import models

def get_person(db: Session, person_id: int) -> Optional[models.Person]:
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session):
    return db.query(models.Person).all()

def create_person(
    db: Session,
    name: str,
    age: int,
    address: str,
    work: str
) -> models.Person:
    db_person = models.Person(
        name=name,
        age=age,
        address=address,
        work=work
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(
    db: Session,
    person_id: int,
    updates: Dict[str, Any]
) -> Optional[models.Person]:
    db_person = get_person(db, person_id)
    if not db_person:
        return None

    for field, value in updates.items():
        if hasattr(db_person, field):
            setattr(db_person, field, value)

    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int) -> bool:
    db_person = get_person(db, person_id)
    if db_person:
        db.delete(db_person)
        db.commit()
        return True
    return False
