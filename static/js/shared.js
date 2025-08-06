// Shared JavaScript functions for TikTok CDN Demo

// Status display helper
function showStatus(element, type, message) {
    element.className = `status status-${type}`;
    element.textContent = message;
    element.style.display = 'block';

    if (type !== 'error') {
        setTimeout(() => element.style.display = 'none', 5000);
    }
}

// Cookie management with localStorage
function loadSavedCookies() {
    const savedCookies = localStorage.getItem('tiktok_cdn_cookies');
    if (savedCookies) {
        const cookieField = document.getElementById('cdnCookies');
        if (cookieField) {
            cookieField.value = savedCookies;
            updateServerCookies(savedCookies);
        }
    }
}

async function updateServerCookies(cookies) {
    const formData = new FormData();
    formData.append('cookies', cookies);
    await fetch('/update-cdn-cookies', { method: 'POST', body: formData });
}

// Common cookie form handler
function setupCookieForm() {
    const cookieForm = document.getElementById('cookieForm');
    if (!cookieForm) return;

    cookieForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const cookies = document.getElementById('cdnCookies').value.trim();
        const status = document.getElementById('cookieStatus');

        showStatus(status, 'info', 'Saving cookies...');

        try {
            await updateServerCookies(cookies);

            if (cookies) {
                localStorage.setItem('tiktok_cdn_cookies', cookies);
                showStatus(status, 'success', '✅ Cookies saved successfully');
            } else {
                localStorage.removeItem('tiktok_cdn_cookies');
                showStatus(status, 'success', '✅ Cookies cleared');
            }
        } catch (error) {
            showStatus(status, 'error', `❌ Error: ${error.message}`);
        }
    });
}

// Common video list loading
async function loadVideoList() {
    const videoList = document.getElementById('videoList');
    if (!videoList) return;

    try {
        const response = await fetch('/videos');
        const data = await response.json();

        if (data.videos && data.videos.length > 0) {
            videoList.innerHTML = data.videos.map(video => `
                <div class="flex justify-between items-center py-3 border-b border-gray-100 last:border-b-0">
                    <div>
                        <div class="font-medium">${video.video_id}</div>
                        <div class="text-sm text-secondary">Uploaded video</div>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="playVideo('${video.video_id}')" class="btn btn-primary btn-sm">▶️ Play</button>
                        <button onclick="deleteVideo('${video.video_id}')" class="btn btn-secondary btn-sm">🗑️ Delete</button>
                    </div>
                </div>
            `).join('');
        } else {
            videoList.innerHTML = '<div class="text-center text-secondary">No videos uploaded yet</div>';
        }
    } catch (error) {
        console.error('Failed to load videos:', error);
        videoList.innerHTML = '<div class="text-center text-error">Failed to load videos</div>';
    }
}

// Common delete video function
async function deleteVideo(videoId) {
    if (!confirm('Delete this video?')) return;

    try {
        await fetch(`/video/${videoId}`, { method: 'DELETE' });
        loadVideoList();
    } catch (error) {
        console.error('Failed to delete video:', error);
    }
}

// Common system status loading
async function loadSystemStatus() {
    try {
        const [videosResponse, cdnResponse] = await Promise.all([
            fetch('/videos'),
            fetch('/cdn-status')
        ]);

        const videosData = await videosResponse.json();
        const cdnData = await cdnResponse.json();

        const totalVideosEl = document.getElementById('totalVideos');
        const cdnStatusEl = document.getElementById('cdnStatus');

        if (totalVideosEl) {
            totalVideosEl.textContent = videosData.videos ? videosData.videos.length : '0';
        }
        if (cdnStatusEl) {
            cdnStatusEl.textContent = cdnData.cdn_configured ? '✅ Configured' : '⚠️ Not Configured';
        }

    } catch (error) {
        console.error('Failed to load system status:', error);
        const totalVideosEl = document.getElementById('totalVideos');
        const cdnStatusEl = document.getElementById('cdnStatus');
        
        if (totalVideosEl) totalVideosEl.textContent = 'Error';
        if (cdnStatusEl) cdnStatusEl.textContent = 'Error';
    }
}

// Initialize shared functionality
function initializeSharedFunctions() {
    loadSavedCookies();
    setupCookieForm();
    loadVideoList();
    loadSystemStatus();
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeSharedFunctions);
