# 🚀 Deploying TikTok CDN Demo to Render

This guide walks you through deploying the TikTok CDN demonstration to Render.com for live testing and demonstration purposes.

## 📋 Prerequisites

- GitHub account with the demo repository
- Render.com account (free tier available)
- Optional: TikTok Ads account for real CDN testing

## 🔧 Deployment Methods

### Method 1: One-Click Deploy (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/canhta/tiktok-cdn-abuse)

1. Click the "Deploy to Render" button above
2. Connect your GitHub account if prompted
3. Select the repository
4. Configure environment variables (see below)
5. Click "Create Web Service"

### Method 2: Manual Deployment

1. **Fork the Repository**
   ```bash
   # Fork https://github.com/canhta/tiktok-cdn-abuse to your GitHub
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service Settings**
   ```
   Name: tiktok-cdn-abuse
   Language: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Method 3: Infrastructure as Code

Use the included `render.yaml` file for automated deployment:

1. **Push render.yaml to your repository**
   ```bash
   git add render.yaml
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Connect repository to Render**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing `render.yaml`

3. **Render automatically detects and deploys the configuration**

## ⚙️ Environment Variables

Configure these environment variables in your Render service:

### Required Variables
```bash
# Server Configuration
HOST=0.0.0.0
PORT=$PORT  # Automatically set by Render

# CDN Configuration
CDN_UPLOAD_URL=https://ads.tiktok.com/api/v2/i18n/material/image/upload/
```

### Optional Variables (for real CDN testing)
```bash
# TikTok Session Cookies (leave empty for demo mode)
CDN_SESSION_COOKIES=session_id=your_session_here;other_cookie=value;
```

## 🔐 Setting Up CDN Credentials (Optional)

To test real CDN uploads, you need TikTok Ads session cookies:

1. **Login to TikTok Ads Manager**
   - Go to [ads.tiktok.com](https://ads.tiktok.com)
   - Login with your TikTok Ads account

2. **Extract Session Cookies**
   - Open Browser DevTools (F12)
   - Go to Network tab
   - Make any request on the site
   - Copy cookies from request headers

3. **Add to Render Environment Variables**
   ```bash
   CDN_SESSION_COOKIES=session_id=abc123;csrf_token=xyz789;
   ```

## 🌐 Accessing Your Deployed Demo

After deployment, your demo will be available at:
```
https://your-service-name.onrender.com
```

### Demo Features Available:
- **Home Page**: Overview and demo explanation
- **Upload**: Video upload and HLS conversion
- **Videos**: Browse uploaded videos
- **Admin**: CDN configuration and fake image management
- **API Docs**: FastAPI documentation at `/docs`

## 📊 Monitoring and Logs

### View Application Logs
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Monitor real-time application output

### Health Checks
- **Health Endpoint**: `https://your-app.onrender.com/health`
- **App Info**: `https://your-app.onrender.com/info`

## 🔧 Troubleshooting

### Common Issues

**1. Build Failures**
```bash
# Check requirements.txt is present and valid
pip install -r requirements.txt
```

**2. Port Binding Issues**
```bash
# Ensure start command uses $PORT variable
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**3. FFmpeg Not Found**
```bash
# FFmpeg is pre-installed on Render Python environments
# No additional setup required
```

**4. CDN Upload Failures**
- Verify `CDN_SESSION_COOKIES` format
- Check TikTok Ads account access
- Monitor logs for authentication errors

### Performance Optimization

**1. Free Tier Limitations**
- Service sleeps after 15 minutes of inactivity
- 750 hours/month limit
- Shared CPU resources

**2. Upgrade Considerations**
- Starter plan: $7/month, no sleep
- Standard plan: $25/month, more resources

## 🔄 Continuous Deployment

### Automatic Deploys
Render automatically deploys when you push to your connected branch:

```bash
git add .
git commit -m "Update demo"
git push origin main  # Triggers automatic deploy
```

### Manual Deploys
Trigger manual deploys via:
- Render Dashboard → "Manual Deploy"
- Deploy Hooks (webhooks)
- Render API

### Deploy Hooks
```bash
# Get deploy hook URL from Render Dashboard
curl https://api.render.com/deploy/srv-xyz...
```

## 🧪 Testing Your Deployment

### 1. Verify Service Health
```bash
curl https://your-app.onrender.com/health
# Expected response: {"status":"healthy","app":"TikTok CDN Demo","version":"1.0.0"}
```

### 2. Test API Endpoints
```bash
# Check CDN status
curl https://your-app.onrender.com/cdn-status

# List videos
curl https://your-app.onrender.com/videos

# Get app info
curl https://your-app.onrender.com/info
```

### 3. Test Web Interface
- **Home**: `https://your-app.onrender.com/`
- **Upload**: `https://your-app.onrender.com/upload`
- **Admin**: `https://your-app.onrender.com/admin`
- **API Docs**: `https://your-app.onrender.com/docs`

## 📝 Demo Usage Tips

1. **Start with Admin Panel**
   - Upload fake images to CDN first
   - Monitor CDN status and cache

2. **Upload Test Videos**
   - Use short videos (< 1 minute) for faster processing
   - Supported formats: MP4, AVI, MOV, etc.

3. **View Generated Playlists**
   - Check playlist URLs contain fake CDN references
   - Verify HLS players ignore fake segments

4. **Monitor Performance**
   - Watch logs for processing times
   - Check CDN upload success rates

## ⚠️ Security Considerations

- **Demo Mode**: Safe for public demonstration
- **CDN Mode**: Only use with authorized TikTok Ads accounts
- **Rate Limiting**: Built-in protection against abuse
- **Environment Variables**: Keep CDN credentials secure

## 🆘 Support

For deployment issues:
1. Check [Render Documentation](https://render.com/docs)
2. Review application logs
3. Verify environment variables
4. Test locally first

---

**⚠️ Educational Purpose Only**: This deployment is for security research and educational demonstration. Use responsibly and only with proper authorization.
