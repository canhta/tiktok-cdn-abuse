"""
Web Routes - HTML pages and templates
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Setup templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """Admin panel page"""
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/player/{video_id}")
async def player_redirect(video_id: str):
    """Redirect to main page"""
    return RedirectResponse(url="/", status_code=302)
