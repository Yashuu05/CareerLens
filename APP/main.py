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
    user_data = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email:
                db = get_database()
                user = db["students"].find_one({"email": email})
                if user:
                    if "_id" in user:
                        user["_id"] = str(user["_id"])
                    if "first_name" in user:
                        user_name = user["first_name"]
                    user_data = user
        except Exception:
            pass

    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"active_page": "dashboard", "user_name": user_name, "user": user_data}
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

@app.get("/export_roadmap_pdf")
async def export_roadmap_pdf(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    from fastapi.responses import Response
    import markdown
    from xhtml2pdf import pisa
    import io
    
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass

    if not email:
        return RedirectResponse(url="/login", status_code=302)

    db = get_database()
    user = db["students"].find_one({"email": email})
    
    if not user or not user.get("roadmap_results"):
        return RedirectResponse(url="/roadmap", status_code=302)

    roadmap_md = user.get("roadmap_results")
    
    html_content = markdown.markdown(roadmap_md)
    
    pdf_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; line-height: 1.6; color: #333; }}
            h1, h2, h3 {{ color: #4F46E5; margin-bottom: 10px; }}
            h1 {{ border-bottom: 2px solid #4F46E5; padding-bottom: 5px; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
            code {{ font-family: monospace; background-color: #f4f4f4; padding: 2px 4px; }}
            ul, ol {{ margin-left: 20px; margin-bottom: 15px; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">CareerLens Personalized Roadmap</h1>
        <br/>
        {html_content}
    </body>
    </html>
    """
    
    result_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(pdf_html), dest=result_file)
    
    if pisa_status.err:
        return Response(content="Error generating PDF", status_code=500)
        
    pdf_bytes = result_file.getvalue()
    
    headers = {
        'Content-Disposition': 'attachment; filename="CareerLens_Roadmap.pdf"'
    }
    
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    
    user_name = "Guest"
    user_data = None
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email:
                db = get_database()
                user = db["students"].find_one({"email": email})
                if user:
                    user_name = user.get("first_name", "Guest")
                    user_data = user
                    if "_id" in user_data:
                        user_data["_id"] = str(user_data["_id"])
        except Exception:
            pass

    if not email:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        request=request, 
        name="settings.html", 
        context={"active_page": "settings", "user_name": user_name, "user": user_data}
    )

@app.post("/settings/update_profile")
async def update_profile(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(""),
    age: int = Form(...),
    course: str = Form(...),
    degree: str = Form(...)
):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass
            
    if not email:
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"status": "error", "message": "Not authenticated"}, status_code=401)
        
    db = get_database()
    db["students"].update_one(
        {"email": email},
        {"$set": {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "course": course,
            "degree": degree
        }}
    )
    
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"status": "success", "message": "Profile updated successfully"})


@app.post("/settings/change_password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...)
):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM, verify_password, get_password_hash
    
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass
            
    from fastapi.responses import JSONResponse
    if not email:
        return JSONResponse(content={"status": "error", "message": "Not authenticated"}, status_code=401)
        
    db = get_database()
    user = db["students"].find_one({"email": email})
    
    if not user or not verify_password(current_password, user.get("password_hash", "")):
        return JSONResponse(content={"status": "error", "message": "Invalid current password"}, status_code=400)
        
    hashed_password = get_password_hash(new_password)
    db["students"].update_one(
        {"email": email},
        {"$set": {"password_hash": hashed_password}}
    )
    
    return JSONResponse(content={"status": "success", "message": "Password changed successfully"})

@app.post("/settings/delete_data")
async def delete_data(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass
            
    from fastapi.responses import JSONResponse
    if not email:
        return JSONResponse(content={"status": "error", "message": "Not authenticated"}, status_code=401)
        
    db = get_database()
    user = db["students"].find_one({"email": email})
    
    if user:
        # Keep essential data, remove everything else
        keep_keys = ["_id", "first_name", "last_name", "email", "password_hash"]
        update_query = {"$unset": {k: "" for k in user.keys() if k not in keep_keys}}
        if update_query["$unset"]:
            db["students"].update_one({"email": email}, update_query)
            
    return JSONResponse(content={"status": "success", "message": "Personal data deleted successfully"})

@app.post("/settings/delete_account")
async def delete_account(request: Request):
    from DB.create_db import get_database
    import jwt
    from APP.auth.utils import SECRET_KEY, ALGORITHM
    from fastapi.responses import JSONResponse
    
    email = None
    token_str = request.cookies.get("access_token")
    if token_str and token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except:
            pass
            
    if not email:
        return JSONResponse(content={"status": "error", "message": "Not authenticated"}, status_code=401)
        
    db = get_database()
    db["students"].delete_one({"email": email})
    
    response = JSONResponse(content={"status": "success", "message": "Account deleted successfully", "redirect": "/login"})
    response.delete_cookie("access_token")
    return response

@app.post("/settings/report_issue")
async def report_issue(
    request: Request,
    issue_type: str = Form(...),
    description: str = Form(...)
):
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"status": "success", "message": "Issue reported successfully"})

@app.post("/settings/give_feedback")
async def give_feedback(
    request: Request,
    feedback: str = Form(...)
):
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"status": "success", "message": "Feedback submitted successfully"})