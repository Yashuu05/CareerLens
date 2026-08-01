from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os

from DB.create_db import get_database
from RoadmapGenerator.APP.auth.utils import verify_password, create_access_token, get_password_hash
from RoadmapGenerator.APP.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    # Find user in "students" collection by email (username field in form maps to email)
    user = db["students"].find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # Return user details excluding the password hash
    user_data = current_user.copy()
    user_data.pop("password_hash", None)
    return user_data

# Optional helper route to register a new user easily with hashing
@router.post("/register")
async def register_student(email: str, password: str, name: str):
    db = get_database()
    if db["students"].find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(password)
    student = {
        "email": email,
        "password_hash": hashed_password,
        "name": name
    }
    result = db["students"].insert_one(student)
    return {"msg": "User created successfully", "id": str(result.inserted_id)}
