"""
CDN Service - TikTok CDN Demo

Creates fake images and uploads them to CDN.
"""

import random
import aiohttp
from typing import Optional
from PIL import Image
import io
from config import CDN_UPLOAD_URL

# Global variable to store dynamic CDN cookies
_dynamic_cdn_cookies = ""


def update_session_cookies(cookies: str) -> dict:
    """Update CDN session cookies dynamically"""
    global _dynamic_cdn_cookies
    _dynamic_cdn_cookies = cookies.strip()

    return {
        "cookies_set": bool(_dynamic_cdn_cookies),
        "cookies_length": len(_dynamic_cdn_cookies) if _dynamic_cdn_cookies else 0
    }


def get_current_cookies() -> str:
    """Get current CDN cookies"""
    return _dynamic_cdn_cookies


async def upload_fake_image_to_cdn(image_data: bytes, filename: str) -> Optional[str]:
    """Upload fake image to CDN"""
    current_cookies = get_current_cookies()
    if not current_cookies:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            cookies = {}
            for cookie in current_cookies.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value

            data = aiohttp.FormData()
            data.add_field('image', image_data, filename=filename, content_type='image/png')

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://ads.tiktok.com/',
            }

            async with session.post(CDN_UPLOAD_URL, data=data, headers=headers, cookies=cookies, timeout=30) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('code') == 0:
                        return result.get('data', {}).get('url')
                return None

    except Exception:
        return None


def create_fake_image(width: int = 1, height: int = 1) -> bytes:
    """Create a minimal PNG image"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    pixels = img.load()
    for x in range(width):
        for y in range(height):
            pixels[x, y] = (0, 0, 0, random.randint(0, 5))

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG', optimize=True)
    return img_bytes.getvalue()


def get_cdn_status():
    """Get CDN status"""
    current_cookies = get_current_cookies()
    return {
        "cdn_configured": bool(current_cookies),
        "cookies_source": "dynamic" if _dynamic_cdn_cookies else "config",
        "cookies_length": len(current_cookies) if current_cookies else 0
    }
