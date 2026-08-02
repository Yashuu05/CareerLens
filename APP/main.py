from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os 
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root in sys.path:
    sys.path.insert(0, project_root)
from logger import logging as log
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

@app.post("/prediction", response_class=HTMLResponse)
async def post_prediction(
    request: Request,
    branch: str = Form(...),
    college_tier: str = Form(...),
    cgpa: float = Form(...),
    backlogs: int = Form(...),
    coding_skills: int = Form(...),
    dsa_score: int = Form(...),
    aptitude_score: int = Form(...),
    communication_skills: int = Form(...),
    ml_knowledge: int = Form(...),
    system_design: int = Form(...),
    internships: int = Form(...),
    projects_count: int = Form(...),
    certifications: int = Form(...),
    hackathons: int = Form(...),
    open_source_contributions: int = Form(...),
    extracurriculars: int = Form(...)
):
    input_data = {
        "branch": branch,
        "college_tier": college_tier,
        "cgpa": cgpa,
        "backlogs": backlogs,
        "coding_skills": coding_skills,
        "dsa_score": dsa_score,
        "aptitude_score": aptitude_score,
        "communication_skills": communication_skills,
        "ml_knowledge": ml_knowledge,
        "system_design": system_design,
        "internships": internships,
        "projects_count": projects_count,
        "certifications": certifications,
        "hackathons": hackathons,
        "open_source_contributions": open_source_contributions,
        "extracurriculars": extracurriculars
    }

    from PlacementPrediction.prediction import load_model, predict_placement, MODEL_DIR
    
    model = load_model(MODEL_DIR)
    
    placement_probability = 0.0
    if model:
        
        result, prob = predict_placement(model, input_data)
        
        if result == "not placed":
            placement_probability = 1.0 - prob
        else:
            placement_probability = prob
        placement_probability = round(placement_probability * 100, 2)
    
    # Save to MongoDB
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            import jwt
            from APP.auth.utils import SECRET_KEY, ALGORITHM
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass

    if email:
        from DB.create_db import get_database
        db = get_database()
        
        db["students"].update_one(
            {"email": email}, 
            {"$set": {"placement_probability": placement_probability}},
            upsert=True
        )

    return templates.TemplateResponse(
        request=request, 
        name="placement_prediction.html", 
        context={
            "active_page": "prediction", 
            "user_name": "Alice",
            "probability": placement_probability
        }
    )

@app.get("/skill_gap", response_class=HTMLResponse)
async def read_skill_gap(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="skill_gap.html", 
        context={"active_page": "skill_gap", "user_name": "Alice"}
    )

@app.post("/skill_gap", response_class=HTMLResponse)
async def calculate_skill_gap(
    request: Request,
    target_domain: str = Form(...),
    python: str = Form(...),
    java: float = Form(...),
    javascript: int = Form(...),
    html_css: int = Form(...),
    react: int = Form(...),
    nodejs: int = Form(...),
    sql: int = Form(...),
    machine_learning: int = Form(...),
    deep_learning: int = Form(...),
    data_visualization: int = Form(...),
    statistics: int = Form(...),
    docker: int = Form(...),
    kubernetes: int = Form(...),
    aws: int = Form(...),
    git: int = Form(...),
    linux: int = Form(...),
    communication: int = Form(...),
    aptitude: int = Form(...),
    projects: int = Form(...),
    internship: int = Form(...)
):
    log.info("collecting the students data")
    student_input = {
        "target_domain": target_domain,
        "python":python, 
        "java": java,
        "javascript": javascript,
        "html_css": html_css,
        "react": react,
        "nodejs": nodejs,
        "sql": sql,
        "machine_learning": machine_learning,
        "deep_learning": deep_learning,
        "data_visualization": data_visualization,
        "statistics": statistics,
        "docker": docker,
        "kubernetes": kubernetes,
        "aws": aws,
        "git": git,
        "linux": linux,
        "communication": communication,
        "aptitude": aptitude,
        "projects": projects,
        "internship": internship
    }

    log.info("connecting to database")
    from DB.create_db import get_database
    db = get_database()
    domain = db['domains'].find_one({"domain_name": target_domain})
    
    result_data = {}
    if domain:
        log.info(f"{domain} exist in datbase.")
        # get dataset of chosen domain
        domain_skill_weights = db['domain_skill_weights'].find_one({"domain": target_domain})
        skill_requiremnt = db['skill_requirements'].find_one({'domain': target_domain})
        category_weights = db['category_weights'].find_one({'domain': target_domain})
        
        from SkillGap.main_calculation import calculate_skill_gap_from_db
        
        if domain_skill_weights and skill_requiremnt and category_weights:
            log.info("calculating skill gap")
            result = calculate_skill_gap_from_db(
                domain=target_domain,
                student_scores=student_input,
                domain_weights=domain_skill_weights,
                domain_reqs=skill_requiremnt,
                domain_cat_weights=category_weights
            )
            
            # Prepare data to save to DB (convert DataFrames to list of dicts)
            result_data = {
                "total_gap": result["total_gap"],
                "tag": result["tag"],
                "technical_gap_percent": result["technical_gap_percent"],
                "technical_breakdown": result["technical_breakdown"].to_dict('records'),
                "category_gap_breakdown": result["category_gap_breakdown"].to_dict('records'),
                "overall_results": result["overall_results"].to_dict('records')
            }
            
            # Get user email from token
            log.info("getting the email of user")
            email = None
            token_str = request.cookies.get("access_token")
            if token_str and token_str.startswith("Bearer "):
                token = token_str.split(" ")[1]
                try:
                    import jwt
                    from APP.auth.utils import SECRET_KEY, ALGORITHM
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    email = payload.get("sub")
                except:
                    pass

            if email:
                log.info(f"{email} exist. Saving results to database")
                db["students"].update_one(
                    {"email": email},
                    {"$set": {"skill_gap_results": result_data}},
                    upsert=True
                )

    return templates.TemplateResponse(
        request=request, 
        name="skill_gap.html", 
        context={
            "active_page": "skill_gap", 
            "user_name": "Alice", 
            "result": result_data
        }
    )

@app.get("/roadmap", response_class=HTMLResponse)
async def read_roadmap(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    
    user_name = "Guest"
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass

    roadmap = None
    if email:
        db = get_database()
        user = db["students"].find_one({"email": email})
        if user:
            user_name = user.get("first_name", "Guest")
            roadmap = user.get("roadmap_results")
            
    return templates.TemplateResponse(
        request=request, 
        name="roadmap.html", 
        context={"active_page": "roadmap", "user_name": user_name, "roadmap": roadmap}
    )

@app.post("/roadmap", response_class=HTMLResponse)
async def generate_roadmap_route(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    from RoadmapGenerator.gemini_roadmap_generate import generate_roadmap
    
    user_name = "Guest"
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass

    roadmap = None
    if email:
        db = get_database()
        user = db["students"].find_one({"email": email})
        if user:
            user_name = user.get("first_name", "Guest")
            skill_gap_results = user.get("skill_gap_results")
            if skill_gap_results:
                roadmap = generate_roadmap(skill_gap_results)
                if roadmap:
                    db["students"].update_one(
                        {"email": email},
                        {"$set": {"roadmap_results": roadmap}}
                    )

    return templates.TemplateResponse(
        request=request, 
        name="roadmap.html", 
        context={"active_page": "roadmap", "user_name": user_name, "roadmap": roadmap}
    )