from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(root_path="/api/v1")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/persons/{person_id}")
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.get("/persons")
def read_persons(db: Session = Depends(get_db)):
    return crud.get_persons(db)

@app.post("/persons", status_code=201)
def create_person(name: str, age: int, address: str, work: str, response: Response, db: Session = Depends(get_db)):
    person = crud.create_person(db, name, age, address, work)
    response.headers["Location"] = f"/api/v1/persons/{person.id}"
    return ""

@app.patch("/persons/{person_id}")
def update_person(person_id: int, name: str = None, age: int = None, address: str = None, work: str = None, db: Session = Depends(get_db)):
    person = crud.update_person(db, person_id, name, age, address, work)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.delete("/persons/{person_id}", status_code=204)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    if not crud.delete_person(db, person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return ""
