from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()


# Get all users
@app.get("/users")
async def get_all_users():
    return {"users": []}


# Get user by ID
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return {"user_id": user_id}

# Update user
@app.put("/users/{user_id}")
async def update_user(user_id: int):
    return {"user_id": user_id}


