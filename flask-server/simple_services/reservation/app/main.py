from fastapi import FastAPI, Depends

import crud, schemas
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/reservation", response_model=list[schemas.Reservation])
def get_reservation(db: Session = Depends(get_db)):
    return jsonable_encoder(crud.get_reservations(db))

@app.get("/reservation/{reservation_id}", response_model=schemas.Reservation)
def get_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    return crud.get_reservation_by_id(db, reservation_id)

@app.post("/reservation", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.Reservation, db: Session = Depends(get_db)):
    return crud.create_reservation(db, reservation)

@app.delete("/reservation/{reservation_id}")
def delete_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    return crud.delete_reservation_by_id(db, reservation_id)