# 🎬 TikTok CDN Demo

⚠️ **Educational Demonstration Only** ⚠️

This is a proof-of-concept demonstration showing how CDN image upload endpoints can potentially be exploited for unauthorized video hosting through HLS playlist manipulation.

**Purpose:** Educational security research and vulnerability demonstration.

## 📋 Demo Overview

This demonstration shows how:
1. **Image Upload Exploitation**: Minimal fake images bypass content validation
2. **CDN Abuse**: Legitimate upload endpoints used for unauthorized hosting
3. **HLS Playlist Manipulation**: Fake CDN URLs injected into video playlists
4. **Traffic Obfuscation**: Video content disguised as image requests

## ✨ Demo Features

### 🎞️ Video Processing
- **Upload Interface**: Drag & drop video upload
- **HLS Conversion**: Convert videos to streaming segments
- **Demo Player**: Play obfuscated HLS streams

### 🎭 CDN Exploitation Demo
- **Fake Image Creation**: Generate minimal 1x1 PNG images
- **CDN Upload**: Upload fake images to TikTok's CDN
- **Playlist Injection**: Mix fake CDN URLs with real video segments
- **Traffic Analysis**: Monitor exploitation patterns

### 🖥️ Demo Interface
- **Simple UI**: Clean demonstration interface
- **Admin Panel**: CDN configuration and fake image management
- **Statistics**: Track demo activity and success rates

## 🚀 Quick Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg:**
```bash
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: Download from https://ffmpeg.org/
```

4. **Configure CDN (optional):**
```bash
# Copy .env.example to .env and add TikTok session cookies
cp .env.example .env
# Edit .env and set CDN_SESSION_COOKIES if testing real uploads
```

5. **Run the demo:**
```bash
python main.py
```

**Demo available at:** `http://localhost:8000`

## 🎯 Usage

1. **Upload fake images to CDN** (Admin panel)
2. **Upload a video** (converts to HLS segments)
3. **View generated playlist** (contains fake CDN image references)
4. **Play video** (player ignores fake segments)

## � Key Files

- `main.py` - FastAPI application
- `config.py` - Configuration settings
- `modules/cdn_service.py` - CDN upload functionality
- `modules/video_service.py` - HLS processing
- `docs/spec.md` - Technical vulnerability details

## ⚠️ Disclaimer

This tool is for **educational and authorized security research only**. Users are responsible for compliance with applicable laws and regulations. Unauthorized use against systems you don't own is prohibited.
