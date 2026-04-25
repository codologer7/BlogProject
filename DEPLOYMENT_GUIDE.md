# GitHub & Render Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top-right corner
3. Select "New repository"
4. Fill in:
   - **Repository name**: `blogproject`
   - **Description**: Django Blog Application
   - **Privacy**: Choose Public or Private
   - Do NOT initialize with README (we already have one)
5. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, you'll see commands like these. Run them in your terminal:

```bash
# Navigate to project directory
cd "d:\Downloads\FullStack\DJANGO PROJECTS\blogproject"

# Set the remote repository (replace YOUR_GITHUB_USERNAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/blogproject.git

# Rename branch if needed (GitHub uses 'main' by default now)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Prepare Render Deployment

### 3.1 Generate a Secret Key

Run this Python command to generate a new SECRET_KEY:

```bash
# In your project directory with venv activated
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output - you'll need it for Render.

### 3.2 Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up using your GitHub account (recommended)
3. Authorize Render to access your GitHub repositories

## Step 4: Deploy on Render

### 4.1 Create New Web Service

1. In Render dashboard, click "New +" button
2. Select "Web Service"
3. Click "Connect" next to your `blogproject` repository
4. Or authorize if needed and find your repository

### 4.2 Configure Deployment

Fill in the following settings:

**Basic Information:**
- **Name**: `blogproject`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main`

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

**Start Command:**
```
gunicorn blogproject.wsgi
```

### 4.3 Set Environment Variables

Click "Advanced" and add these environment variables:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Paste the generated key from Step 3.1 |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com,localhost,127.0.0.1` |

**Example SECRET_KEY:**
```
9abc&def123ghi456jkl789mno012pqr345stu678vwx901yzab234cde567fgh
```

### 4.4 Select Plan

- Choose "Free" tier for testing
- Render auto-suspends after 15 min of inactivity on free tier

### 4.5 Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete (usually 2-5 minutes)
3. Check the logs for any errors
4. Your app will be available at: `https://your-app-name.onrender.com`

## Post-Deployment Checks

### 5.1 Create Superuser on Render

Once deployed, create a superuser on the production database:

```bash
# This requires a way to run commands on Render (Shell)
# Or use Render's "Shell" feature in the dashboard
python manage.py createsuperuser
```

### 5.2 Admin Access

Access admin panel at:
```
https://your-app-name.onrender.com/admin
```

### 5.3 Test Application

1. Visit your app URL
2. Sign up a new user
3. Create a blog post
4. Test all features

## Troubleshooting Deployment

### Issue: Build fails

**Check logs:**
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. Look for error messages

**Common issues:**
- Missing `requirements.txt` - Ensure all dependencies are listed
- Python version mismatch - Check `runtime.txt` (should be `python-3.11.7`)
- Environment variables not set - Double-check all vars are added

### Issue: Static files not loading

Run:
```bash
python manage.py collectstatic --no-input
```

### Issue: Database errors

- Ensure migrations are in Procfile
- Check database URL is correct
- Verify database service is running

### Issue: Application crashes after deployment

1. Check Render logs for errors
2. Verify SECRET_KEY is properly set
3. Check ALLOWED_HOSTS includes your Render domain

## Future Deployments

After making changes locally:

```bash
# Commit changes
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main

# Render automatically deploys on push!
```

## Auto-Deploy Setup

Render automatically deploys when you push to GitHub:
1. No manual action needed
2. Check Render dashboard for deployment status
3. Logs show build progress in real-time

## Database Management

### SQLite (Default)

Currently using SQLite. For production, consider PostgreSQL:

1. In Render dashboard, create a PostgreSQL database
2. Get the connection string
3. Set `DATABASE_URL` environment variable
4. Update `requirements.txt` to include: `dj-database-url`

### Update settings.py for PostgreSQL

Add to your settings.py:

```python
import dj_database_url

if config('DATABASE_URL', default=None):
    DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'), conn_max_age=600)
```

## Custom Domain (Optional)

1. In Render dashboard, go to "Settings"
2. Under "Custom Domain", add your domain
3. Follow DNS configuration instructions
4. Wait for SSL certificate (usually 5-10 minutes)

## Monitoring & Logs

View your app logs:
1. Render dashboard → Your service
2. Click "Logs" tab
3. Real-time log streaming

## Scaling (Paid Plans)

For production with more traffic:
- Upgrade to Starter ($7/month) or Standard plan
- Auto-scaling options available
- PostgreSQL database integration

## Need Help?

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **GitHub Issues**: Create issue in your repository

## Quick Reference Commands

```bash
# View git status
git status

# View commit history
git log --oneline

# Push changes
git push origin main

# Pull latest
git pull origin main

# Create new branch
git checkout -b feature/my-feature

# Switch branches
git checkout main
```

---

**Congratulations! Your Django blog is now live on Render! 🎉**
