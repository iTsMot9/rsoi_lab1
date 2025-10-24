from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from . import crud, models, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(root_path="/api/v1")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.get("/persons", response_model=list[schemas.Person])
def read_persons(db: Session = Depends(get_db)):
    return crud.get_persons(db)

@app.post("/persons", status_code=201, response_model=schemas.Person)
def create_person(
    person: schemas.PersonCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    db_person = crud.create_person(db, person.name, person.age, person.address, person.work)
    response.headers["Location"] = f"/api/v1/persons/{db_person.id}"
    return db_person

@app.patch("/persons/{person_id}", response_model=schemas.Person)
def update_person(
    person_id: int,
    person_update: schemas.PersonUpdate,
    db: Session = Depends(get_db)
):
    update_data = person_update.model_dump(exclude_unset=True)
    db_person = crud.update_person(db, person_id, update_data)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.delete("/persons/{person_id}", status_code=204)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    if not crud.delete_person(db, person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return Response(status_code=204)
