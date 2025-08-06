// Video Hosting CDN - Main JavaScript

class VideoHostingApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadVideos();
    }

    setupEventListeners() {
        // Upload form handling
        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) {
            uploadForm.addEventListener('submit', this.handleVideoUpload.bind(this));
        }

        // Drag and drop handling
        const uploadArea = document.getElementById('uploadArea');
        if (uploadArea) {
            this.setupDragAndDrop(uploadArea);
        }

        // File input handling
        const fileInput = document.getElementById('videoFile');
        if (fileInput) {
            fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        }

        // CDN upload handling
        const cdnForm = document.getElementById('cdnForm');
        if (cdnForm) {
            cdnForm.addEventListener('submit', this.handleCDNUpload.bind(this));
        }
    }

    setupDragAndDrop(uploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
        });

        uploadArea.addEventListener('drop', this.handleDrop.bind(this), false);
        uploadArea.addEventListener('click', () => {
            document.getElementById('videoFile').click();
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const fileInput = document.getElementById('videoFile');
            fileInput.files = files;
            this.handleFileSelect({ target: fileInput });
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.updateUploadArea(file);
        }
    }

    updateUploadArea(file) {
        const uploadArea = document.getElementById('uploadArea');
        const uploadText = uploadArea.querySelector('.upload-text');
        const uploadSubtext = uploadArea.querySelector('.upload-subtext');
        
        uploadText.textContent = file.name;
        uploadSubtext.textContent = `${this.formatFileSize(file.size)} • ${file.type}`;
        uploadArea.classList.add('file-selected');
    }

    async handleVideoUpload(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const progressBar = document.getElementById('uploadProgress');
        const statusDiv = document.getElementById('uploadStatus');
        const submitBtn = e.target.querySelector('button[type="submit"]');
        
        // Show progress bar
        progressBar.style.display = 'block';
        progressBar.querySelector('.progress-bar').style.width = '0%';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading...';
        
        try {
            const response = await this.uploadWithProgress('/upload', formData, (progress) => {
                progressBar.querySelector('.progress-bar').style.width = `${progress}%`;
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showStatus(statusDiv, 'success', `✅ Video uploaded successfully! ID: ${result.video_id}`);
                this.resetUploadForm();
                this.loadVideos(); // Refresh video list
            } else {
                this.showStatus(statusDiv, 'error', `❌ Upload failed: ${result.detail}`);
            }
        } catch (error) {
            this.showStatus(statusDiv, 'error', `❌ Upload error: ${error.message}`);
        } finally {
            progressBar.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Upload Video';
        }
    }

    async handleCDNUpload(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const statusDiv = document.getElementById('cdnStatus');
        const submitBtn = e.target.querySelector('button[type="submit"]');
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading...';
        
        try {
            const response = await fetch('/upload-fake-images', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showStatus(statusDiv, 'success', 
                    `✅ Uploaded ${result.uploaded}/${result.total_requested} fake images. Cache size: ${result.cache_size}`);
            } else {
                this.showStatus(statusDiv, 'error', `❌ CDN upload failed: ${result.detail}`);
            }
        } catch (error) {
            this.showStatus(statusDiv, 'error', `❌ CDN upload error: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Upload Fake Images';
        }
    }

    async uploadWithProgress(url, formData, onProgress) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const progress = (e.loaded / e.total) * 100;
                    onProgress(progress);
                }
            });
            
            xhr.addEventListener('load', () => {
                resolve(xhr);
            });
            
            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });
            
            xhr.open('POST', url);
            xhr.send(formData);
        });
    }

    async loadVideos() {
        const videoList = document.getElementById('videoList');
        if (!videoList) return;
        
        try {
            const response = await fetch('/videos');
            const data = await response.json();
            
            if (data.videos && data.videos.length > 0) {
                videoList.innerHTML = data.videos.map(video => this.createVideoItem(video)).join('');
            } else {
                videoList.innerHTML = '<div class="text-center text-secondary">No videos uploaded yet</div>';
            }
        } catch (error) {
            console.error('Failed to load videos:', error);
            videoList.innerHTML = '<div class="text-center text-error">Failed to load videos</div>';
        }
    }

    createVideoItem(video) {
        return `
            <div class="video-item">
                <div class="video-thumbnail">🎬</div>
                <div class="video-info">
                    <div class="video-title">${video.video_id}</div>
                    <div class="video-meta">
                        Playlist: <a href="${video.playlist_url}" target="_blank">View M3U8</a>
                    </div>
                </div>
                <div class="video-actions">
                    <button class="btn btn-primary btn-sm" onclick="app.playVideo('${video.video_id}')">
                        ▶️ Play
                    </button>
                    <button class="btn btn-secondary btn-sm" onclick="app.copyPlaylistUrl('${video.playlist_url}')">
                        📋 Copy URL
                    </button>
                    <button class="btn btn-error btn-sm" onclick="app.deleteVideo('${video.video_id}')">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `;
    }

    async playVideo(videoId) {
        // Navigate to player page
        window.location.href = `/player/${videoId}`;
    }

    async copyPlaylistUrl(url) {
        try {
            await navigator.clipboard.writeText(window.location.origin + url);
            this.showToast('Playlist URL copied to clipboard!');
        } catch (error) {
            console.error('Failed to copy URL:', error);
            this.showToast('Failed to copy URL', 'error');
        }
    }

    async deleteVideo(videoId) {
        if (!confirm('Are you sure you want to delete this video?')) {
            return;
        }
        
        try {
            const response = await fetch(`/video/${videoId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                this.showToast('Video deleted successfully!');
                this.loadVideos(); // Refresh list
            } else {
                const result = await response.json();
                this.showToast(`Failed to delete video: ${result.detail}`, 'error');
            }
        } catch (error) {
            this.showToast(`Delete error: ${error.message}`, 'error');
        }
    }

    resetUploadForm() {
        const form = document.getElementById('uploadForm');
        const uploadArea = document.getElementById('uploadArea');
        const uploadText = uploadArea.querySelector('.upload-text');
        const uploadSubtext = uploadArea.querySelector('.upload-subtext');
        
        form.reset();
        uploadArea.classList.remove('file-selected');
        uploadText.textContent = 'Drop video file here or click to browse';
        uploadSubtext.textContent = 'Supports MP4, AVI, MOV, MKV, WebM (max 500MB)';
    }

    showStatus(element, type, message) {
        element.className = `status status-${type}`;
        element.textContent = message;
        element.style.display = 'block';
    }

    showToast(message, type = 'success') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'error' ? 'var(--error-color)' : 'var(--success-color)'};
            color: white;
            border-radius: 0.375rem;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new VideoHostingApp();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .upload-area.file-selected {
        border-color: var(--success-color);
        background: rgb(16 185 129 / 0.05);
    }
`;
document.head.appendChild(style);
