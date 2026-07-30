from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os 
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root in sys.path:
    sys.path.insert(0, project_root)
# creating app
app = FastAPI()

# Include the JWT authentication router
from APP.auth.router import router as auth_router
app.include_router(auth_router)

# Mount static files directory (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point FastAPI to the templates directory
templates = Jinja2Templates(directory="templates")

# defining api endpoints
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"active_page": "home"}
    )

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"active_page": "login"}
    )

@app.post("/login", response_class=HTMLResponse)
async def do_login(request: Request, email: str = Form(...), password: str = Form(...)):
    from DB.create_db import get_database
    from APP.auth.utils import verify_password, create_access_token
    from APP.auth.router import ACCESS_TOKEN_EXPIRE_MINUTES
    from datetime import timedelta
    
    db = get_database()
    user = db["students"].find_one({"email": email})
    
    if user and verify_password(password, user.get("password_hash", "")):
        response = RedirectResponse(url="/dashboard", status_code=302)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
        
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={"active_page": "login", "error": "Invalid email or password"}
    )

@app.get("/signup", response_class=HTMLResponse)
async def read_signup(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={"active_page": "signup"}
    )

@app.post("/signup", response_class=HTMLResponse)
async def do_signup(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(""),
    email: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    country: str = Form(...),
    degree: str = Form(...),
    course: str = Form(...)
):
    from DB.create_db import get_database
    from APP.auth.utils import get_password_hash
    
    db = get_database()
    if db["students"].find_one({"email": email}):
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"active_page": "signup", "error": "Email already registered"}
        )
    
    hashed_password = get_password_hash(password)
    student = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password_hash": hashed_password,
        "age": age,
        "country": country,
        "degree": degree,
        "course": course
    }
    db["students"].insert_one(student)
    
    return RedirectResponse(url="/login", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    
    user_name = "Guest"
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email:
                db = get_database()
                user = db["students"].find_one({"email": email})
                if user and "first_name" in user:
                    user_name = user["first_name"]
        except Exception:
            pass

    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"active_page": "dashboard", "user_name": user_name}
    )

@app.get("/prediction", response_class=HTMLResponse)
async def read_prediction(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="placement_prediction.html", 
        context={"active_page": "prediction", "user_name": "Alice"}
    )

@app.get("/skill_gap", response_class=HTMLResponse)
async def read_skill_gap(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="skill_gap.html", 
        context={"active_page": "skill_gap", "user_name": "Alice"}
    )

@app.get("/roadmap", response_class=HTMLResponse)
async def read_roadmap(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="roadmap.html", 
        context={"active_page": "roadmap", "user_name": "Alice"}
    )