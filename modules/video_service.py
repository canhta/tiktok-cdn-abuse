"""
Video Service - HLS processing and playlist generation
"""

import os
import subprocess
import random
from typing import List
from modules.cdn_service import create_fake_image, upload_fake_image_to_cdn


def process_video_to_hls(input_path: str, video_dir: str) -> List[str]:
    """Convert video to HLS segments"""
    segment_pattern = f"{video_dir}/%03d.ts"
    
    ffmpeg_cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264', '-c:a', 'aac',
        '-f', 'segment', '-segment_time', '10',
        '-reset_timestamps', '1',
        segment_pattern
    ]

    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")

    # Get segment files
    segments = [f for f in os.listdir(video_dir) if f.endswith('.ts')]
    segments.sort()
    return segments


async def generate_obfuscated_playlist(video_id: str, segments: List[str], injection_ratio: float = 0.5) -> str:
    """Generate M3U8 playlist with fake CDN images as decoys"""
    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        "#EXT-X-TARGETDURATION:10",
        "#EXT-X-MEDIA-SEQUENCE:0"
    ]

    for segment in segments:
        # Inject fake CDN image URL before real segment (per spec.md concept)
        if random.random() < injection_ratio:
            # Generate fake image on-demand and upload to TikTok CDN
            image_data = create_fake_image(1, 1)  # 1x1 PNG as per spec
            fake_url = await upload_fake_image_to_cdn(image_data, f"decoy_{random.randint(1000,9999)}.png")

            if fake_url:
                lines.extend([
                    "#EXTINF:0.1,",  # Very short duration - players will skip
                    fake_url
                ])

        # Add real video segment
        lines.extend([
            "#EXTINF:10.0,",
            f"/segment/{video_id}/{segment}"
        ])

    lines.append("#EXT-X-ENDLIST")
    return "\n".join(lines)


def save_playlist(video_id: str, playlist_content: str):
    """Save playlist to file"""
    playlist_path = f"storage/playlists/{video_id}.m3u8"
    with open(playlist_path, 'w') as f:
        f.write(playlist_content)


def get_playlist_content(video_id: str) -> str:
    """Get playlist content from file"""
    playlist_path = f"storage/playlists/{video_id}.m3u8"
    if not os.path.exists(playlist_path):
        raise FileNotFoundError("Playlist not found")
    
    with open(playlist_path, 'r') as f:
        return f.read()


def list_all_videos():
    """List all available videos"""
    videos = []
    playlist_dir = "storage/playlists"
    
    if os.path.exists(playlist_dir):
        for file in os.listdir(playlist_dir):
            if file.endswith('.m3u8'):
                video_id = file[:-5]  # Remove .m3u8
                videos.append({
                    "video_id": video_id,
                    "playlist_url": f"/playlist/{video_id}"
                })
    
    return {"videos": videos}


def delete_video_files(video_id: str):
    """Delete video and its files"""
    import shutil
    
    video_dir = f"storage/videos/{video_id}"
    playlist_path = f"storage/playlists/{video_id}.m3u8"
    
    deleted = []
    
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)
        deleted.append("video_segments")
    
    if os.path.exists(playlist_path):
        os.remove(playlist_path)
        deleted.append("playlist")
    
    return deleted
