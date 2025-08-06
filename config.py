"""
TikTok CDN Demo - Configuration

⚠️  Demo Purpose Only ⚠️
This is a proof-of-concept demonstration for educational purposes.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Configuration
APP_NAME = "TikTok CDN Demo"
APP_VERSION = "1.0.0"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CDN Configuration
CDN_UPLOAD_URL = os.getenv("CDN_UPLOAD_URL", "https://ads.tiktok.com/api/v2/i18n/material/image/upload/")
