from fastapi import FastAPI, Depends

import crud, schemas, models
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/online")
def online():
    return JSONResponse(status_code=200, content={"message": "Reservation is online."})

@app.get("/reservation", response_model=list[schemas.ReservationResponse])
def get_reservation(db: Session = Depends(get_db)):
    return jsonable_encoder(crud.get_reservations(db))

@app.get("/reservation/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    return crud.get_reservation_by_id(db, reservation_id)

@app.post("/reservation", response_model=schemas.ReservationResponse)
def create_reservation(reservation: schemas.Reservation, db: Session = Depends(get_db)):
    res = crud.create_reservation(db, reservation)
    if res is None:
        return JSONResponse(status_code=400, content={"message": "Reservation creation failed. Please check the input data."})
    return JSONResponse(status_code=201, content={"message": "Reservation created successfully.", "reservation": jsonable_encoder(res)})

@app.delete("/reservation/{reservation_id}")
def delete_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    return crud.delete_reservation_by_id(db, reservation_id)