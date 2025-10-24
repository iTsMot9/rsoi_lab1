from pydantic import BaseModel, Field
from typing import Optional

class PersonBase(BaseModel):
    name: str
    age: int = Field(..., ge=0, le=150)
    address: str
    work: str

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    address: Optional[str] = None
    work: Optional[str] = None

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
