from sqlalchemy.orm import Session
from . import models

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session):
    return db.query(models.Person).all()

def create_person(db: Session, name: str, age: int, address: str, work: str):
    db_person = models.Person(name=name, age=age, address=address, work=work)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: int, name: str = None, age: int = None, address: str = None, work: str = None):
    db_person = get_person(db, person_id)
    if db_person:
        if name: db_person.name = name
        if age: db_person.age = age
        if address: db_person.address = address
        if work: db_person.work = work
        db.commit()
        db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    if db_person:
        db.delete(db_person)
        db.commit()
        return True
    return False
