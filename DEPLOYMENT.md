# Deployment Guide - African AI Strategies Portal

## 🚀 Deploying to Vercel

This guide will help you deploy the African AI Strategies Portal to Vercel for live hosting.

### Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Vercel CLI** (optional): `npm install -g vercel`

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Sign in with your GitHub account

2. **Import Project**
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose `kevshakes/african-ai-strategies-portal`

3. **Configure Project**
   - **Project Name**: `african-ai-strategies-portal`
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Environment Variables** (Optional)
   - Add `SECRET_KEY` with a secure random string
   - Add `FLASK_ENV` with value `production`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)
   - Your app will be live at: `https://african-ai-strategies-portal.vercel.app`

### Method 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd african-ai-strategies-portal
vercel

# Follow the prompts:
# ? Set up and deploy "~/african-ai-strategies-portal"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Account]
# ? Link to existing project? [y/N] n
# ? What's your project's name? african-ai-strategies-portal
# ? In which directory is your code located? ./

# Deploy to production
vercel --prod
```

### Method 3: Deploy via GitHub Integration

1. **Connect GitHub to Vercel**
   - Go to Vercel Dashboard
   - Click "Import Project"
   - Connect your GitHub account

2. **Auto-Deploy Setup**
   - Select your repository
   - Vercel will automatically deploy on every push to main branch
   - Configure build settings as needed

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "functions": {
    "app.py": {
      "maxDuration": 30
    }
  }
}
```

### requirements.txt (Optimized for Vercel)
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dateutil==2.8.2
Jinja2==3.1.2
Werkzeug==2.3.7
```

## 🌐 Custom Domain (Optional)

### Add Custom Domain
1. Go to your project dashboard on Vercel
2. Click "Settings" → "Domains"
3. Add your custom domain (e.g., `aistrategies.africa`)
4. Configure DNS records as instructed
5. SSL certificate will be automatically provisioned

### DNS Configuration
```
Type: CNAME
Name: www (or @)
Value: cname.vercel-dns.com
```

## 📊 Performance Optimization

### Vercel Edge Functions
- Static assets served from global CDN
- Automatic image optimization
- Gzip compression enabled
- HTTP/2 support

### Caching Strategy
```python
# Add to app.py for better caching
from flask import make_response

@app.after_request
def after_request(response):
    # Cache static assets for 1 year
    if request.endpoint == 'static':
        response.cache_control.max_age = 31536000
    # Cache API responses for 5 minutes
    elif request.path.startswith('/api/'):
        response.cache_control.max_age = 300
    return response
```

## 🔍 Monitoring and Analytics

### Vercel Analytics
1. Go to project dashboard
2. Click "Analytics" tab
3. Enable Web Analytics
4. View real-time performance metrics

### Error Monitoring
- Check Vercel Functions logs
- Monitor response times
- Track error rates

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check requirements.txt for incompatible packages
   # Ensure Python version compatibility
   # Verify vercel.json configuration
   ```

2. **Import Errors**
   ```python
   # Ensure all imports are available in serverless environment
   # Use try/except for optional dependencies
   ```

3. **Timeout Issues**
   ```json
   // Increase function timeout in vercel.json
   "functions": {
     "app.py": {
       "maxDuration": 30
     }
   }
   ```

4. **Static Files Not Loading**
   ```python
   # Ensure static files are in static/ directory
   # Check Flask static_folder configuration
   ```

### Debug Mode
```bash
# Enable debug mode locally
export FLASK_DEBUG=1
python app.py

# Check Vercel logs
vercel logs [deployment-url]
```

## 📈 Post-Deployment Steps

### 1. Test All Features
- [ ] Dashboard loads correctly
- [ ] Country pages work
- [ ] API endpoints respond
- [ ] Visualizations render
- [ ] Mobile responsiveness

### 2. Performance Testing
- [ ] Page load times < 3 seconds
- [ ] API response times < 1 second
- [ ] Mobile performance score > 90

### 3. SEO Optimization
- [ ] Add meta descriptions
- [ ] Configure Open Graph tags
- [ ] Submit sitemap to search engines

### 4. Share Your Deployment
```bash
# Your live URL will be:
https://african-ai-strategies-portal.vercel.app

# Or with custom domain:
https://your-custom-domain.com
```

## 🎯 Success Metrics

After deployment, monitor:
- **Uptime**: Should be 99.9%+
- **Response Time**: < 2 seconds globally
- **User Engagement**: Time on site, page views
- **API Usage**: Endpoint popularity, error rates

## 🔄 Continuous Deployment

### Automatic Deployments
- Every push to `main` branch triggers deployment
- Preview deployments for pull requests
- Rollback capability for failed deployments

### Manual Deployments
```bash
# Deploy specific branch
vercel --prod --confirm

# Deploy with environment variables
vercel --prod --env SECRET_KEY=your-secret-key
```

## 🌟 Going Live Checklist

- [ ] Repository is public and accessible
- [ ] All dependencies are in requirements.txt
- [ ] vercel.json is properly configured
- [ ] Environment variables are set
- [ ] Custom domain is configured (optional)
- [ ] Analytics are enabled
- [ ] Error monitoring is set up
- [ ] Performance is optimized
- [ ] All features are tested
- [ ] Documentation is updated

## 🎉 Congratulations!

Once deployed, your African AI Strategies Portal will be:
- ✅ **Live and accessible** globally
- ✅ **Automatically scaled** based on traffic
- ✅ **Continuously deployed** from GitHub
- ✅ **Monitored and optimized** by Vercel
- ✅ **Ready for real-world impact**

Your portal is now ready to serve policymakers, researchers, and AI enthusiasts worldwide! 🌍✨
