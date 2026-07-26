from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from APP.auth.utils import SECRET_KEY, ALGORITHM
from DB.create_db import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    db = get_database()
    # Find user in the "students" collection as per the user's feedback
    user = db["students"].find_one({"email": email})
    if user is None:
        raise credentials_exception
    
    # Convert ObjectId to string to avoid serialization issues later
    user["_id"] = str(user["_id"])
    return user
