"""
Web Routes - HTML pages and templates
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Setup templates
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Upload page"""
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/videos", response_class=HTMLResponse)
async def videos_page(request: Request):
    """Videos listing page"""
    return templates.TemplateResponse("videos.html", {"request": request})


@router.get("/player/{video_id}", response_class=HTMLResponse)
async def player_page(request: Request, video_id: str):
    """Video player page"""
    return templates.TemplateResponse("player.html", {"request": request, "video_id": video_id})


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """Admin panel"""
    return templates.TemplateResponse("admin.html", {"request": request})
