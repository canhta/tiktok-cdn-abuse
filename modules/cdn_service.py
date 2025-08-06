"""
CDN Service - TikTok CDN Demo

Creates fake images and uploads them to CDN.
"""

import random
import aiohttp
from typing import Optional
from PIL import Image
import io
from config import CDN_UPLOAD_URL, CDN_SESSION_COOKIES

fake_image_cache = []


async def upload_fake_image_to_cdn(image_data: bytes, filename: str) -> Optional[str]:
    """Upload fake image to CDN"""
    if not CDN_SESSION_COOKIES:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            cookies = {}
            for cookie in CDN_SESSION_COOKIES.split(';'):
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
    return {
        "cdn_configured": bool(CDN_SESSION_COOKIES),
        "fake_images_cached": len(fake_image_cache)
    }
