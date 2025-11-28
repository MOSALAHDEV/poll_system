# Deployment Guide

## Deploy to Render

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Create PostgreSQL Database on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Name: `polldb`
4. Select free tier
5. Click "Create Database"
6. Copy the "Internal Database URL"

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `poll-system-api`
   - Environment: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
   - Instance Type: Free

### Step 4: Add Environment Variables
Add these in the "Environment" section:
```
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
DATABASE_URL=<paste-internal-database-url>
ALLOWED_HOSTS=<your-app-name>.onrender.com
PYTHON_VERSION=3.12.0
```

### Step 5: Deploy
Click "Create Web Service" and wait for deployment.

Your API will be live at: `https://<your-app-name>.onrender.com`

---

## Deploy to Railway

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
railway login
```

### Step 2: Initialize Project
```bash
railway init
railway add --database postgresql
```

### Step 3: Set Environment Variables
```bash
railway variables set SECRET_KEY=<your-secret-key>
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=<your-domain>.railway.app
```

### Step 4: Deploy
```bash
railway up
```

Your API will be live at the provided Railway URL.

---

## Post-Deployment

### Create Superuser
```bash
# Render
render shell
python manage.py createsuperuser

# Railway
railway run python manage.py createsuperuser
```

### Access API Documentation
- Swagger UI: `https://your-domain.com/swagger/`
- ReDoc: `https://your-domain.com/redoc/`
- Admin Panel: `https://your-domain.com/admin/`

### Test Endpoints
```bash
# Get JWT Token
curl -X POST https://your-domain.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# Create Poll
curl -X POST https://your-domain.com/api/polls/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "Test Poll",
    "description": "Testing deployment",
    "expires_at": "2024-12-31T23:59:59Z",
    "choices": [
      {"text": "Option 1"},
      {"text": "Option 2"}
    ]
  }'
```

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check if PostgreSQL service is running
- Ensure migrations have run

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings
- Verify WhiteNoise is in MIDDLEWARE

### 500 Errors
- Set DEBUG=True temporarily to see errors
- Check application logs
- Verify all environment variables are set
