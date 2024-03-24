from fastapi import FastAPI, Depends
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
import crud, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()
origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Get all users
@app.get("/users", response_model=list[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    res = jsonable_encoder(crud.get_users(db))
    return res

# Create user
@app.post("/users")
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# Get user by ID
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return {"user_id": user_id}

# Update user
@app.put("/users/{user_id}")
async def update_user(user_id: int):
    return {"user_id": user_id}

