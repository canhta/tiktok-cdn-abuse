#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Building TikTok CDN Demo for Render..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create storage directories
echo "📁 Creating storage directories..."
mkdir -p storage/videos
mkdir -p storage/playlists

# Verify FFmpeg is available (pre-installed on Render)
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n1)"
else
    echo "⚠️ FFmpeg not found - video processing may fail"
fi

echo "✅ Build completed successfully!"
