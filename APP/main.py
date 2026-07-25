from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# creating app
app = FastAPI()

# Mount static files directory (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point FastAPI to the templates directory
templates = Jinja2Templates(directory="templates")

# defining api endpoints
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"active_page": "dashboard", "user_name": "Alice"}
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