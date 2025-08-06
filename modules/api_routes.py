"""
API Routes - Video upload, management, and CDN operations
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, PlainTextResponse
from modules.video_service import (
    process_video_to_hls, generate_obfuscated_playlist, 
    save_playlist, get_playlist_content, list_all_videos, delete_video_files
)
from modules.cdn_service import create_fake_image, upload_fake_image_to_cdn, get_cdn_status, update_session_cookies
import asyncio
import random
from config import APP_NAME, APP_VERSION

router = APIRouter()


@router.post("/upload-fake-images")
async def upload_fake_images(count: int = Form(10)):
    """Upload fake images to CDN"""
    uploaded_urls = []

    for i in range(count):
        # Create randomized fake image
        width = random.choice([1, 2])
        height = random.choice([1, 2])
        image_data = create_fake_image(width, height)
        filename = f"fake_{width}x{height}_{i:03d}.png"

        # Upload to CDN
        url = await upload_fake_image_to_cdn(image_data, filename)
        if url:
            uploaded_urls.append(url)

        # Rate limiting (5 req/sec as per spec)
        await asyncio.sleep(0.2)

    return {
        "uploaded": len(uploaded_urls),
        "total_requested": count,
        "urls": uploaded_urls[:5]  # Show first 5 URLs as examples
    }


@router.post("/upload")
async def upload_video(video: UploadFile = File(...), injection_ratio: float = Form(0.5)):
    """Upload and process video with playlist obfuscation"""

    # Validate file
    if not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    # Generate video ID
    video_id = str(uuid.uuid4())
    video_dir = f"storage/videos/{video_id}"
    os.makedirs(video_dir, exist_ok=True)

    try:
        # Save uploaded file
        input_path = f"{video_dir}/input.mp4"
        with open(input_path, "wb") as f:
            content = await video.read()
            f.write(content)

        # Convert to HLS
        segments = process_video_to_hls(input_path, video_dir)

        # Generate obfuscated playlist with CDN fake images
        playlist_content = await generate_obfuscated_playlist(video_id, segments, injection_ratio)

        # Save playlist
        save_playlist(video_id, playlist_content)

        # Cleanup
        os.remove(input_path)

        return {
            "video_id": video_id,
            "status": "ready",
            "playlist_url": f"/playlist/{video_id}",
            "segments": len(segments),
            "injection_ratio": injection_ratio
        }

    except Exception as e:
        # Cleanup on error
        import shutil
        if os.path.exists(video_dir):
            shutil.rmtree(video_dir)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/playlist/{video_id}", response_class=PlainTextResponse)
async def get_playlist(video_id: str):
    """Get M3U8 playlist"""
    try:
        return get_playlist_content(video_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Playlist not found")


@router.get("/segment/{video_id}/{segment_name}")
async def get_segment(video_id: str, segment_name: str):
    """Get video segment"""
    if not segment_name.endswith('.ts'):
        raise HTTPException(status_code=400, detail="Invalid segment")
    
    segment_path = f"storage/videos/{video_id}/{segment_name}"
    
    if not os.path.exists(segment_path):
        raise HTTPException(status_code=404, detail="Segment not found")
    
    return FileResponse(segment_path, media_type="video/mp2t")


@router.get("/videos")
async def list_videos():
    """List all videos"""
    return list_all_videos()


@router.delete("/video/{video_id}")
async def delete_video(video_id: str):
    """Delete video and its files"""
    deleted = delete_video_files(video_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"message": f"Deleted {video_id}", "deleted": deleted}


@router.post("/update-cdn-cookies")
async def update_cdn_cookies(cookies: str = Form(...)):
    """Update CDN session cookies"""
    try:
        result = update_session_cookies(cookies)
        return {
            "success": True,
            "message": "Cookies updated successfully",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update cookies: {str(e)}")


@router.get("/cdn-status")
async def cdn_status():
    """Get CDN configuration status"""
    return get_cdn_status()


@router.get("/info")
async def app_info():
    """Get application information"""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "features": [
            "HLS Video Conversion",
            "CDN Integration",
            "Playlist Obfuscation",
            "Real-time Upload",
            "Mobile Responsive"
        ],
        "endpoints": {
            "upload": "/upload",
            "videos": "/videos",
            "cdn_status": "/cdn-status",
            "health": "/health"
        }
    }


@router.post("/update-cdn-cookies")
async def update_cdn_cookies(cookies: str = Form(...)):
    """Update CDN session cookies dynamically"""
    from modules.cdn_service import update_session_cookies

    # Update the global CDN cookies
    result = update_session_cookies(cookies)

    return {
        "success": True,
        "message": "CDN cookies updated successfully",
        "cookies_configured": bool(cookies.strip()),
        "status": result
    }
