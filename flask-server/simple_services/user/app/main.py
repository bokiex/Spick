from fastapi import FastAPI, Depends
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
import crud, schemas
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all users
@app.get("/users", response_model=list[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    return jsonable_encoder(crud.get_users(db))

# Create user
@app.post("/users")
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# Get user by ID
@app.get("/users/{user_id}", response_model=list[schemas.UserResponse])
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return jsonable_encoder(crud.get_user(user_id))

# Update user
@app.put("/users")
async def update_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db, user)

