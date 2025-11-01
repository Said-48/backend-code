# Deployment Guide - ProjectX Backend

This guide covers deploying the ProjectX backend application to Render with CI/CD pipeline.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Render Deployment](#render-deployment)
- [CI/CD Setup](#cicd-setup)
- [Environment Variables](#environment-variables)
- [Post-Deployment](#post-deployment)

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Git repository hosted on GitHub
- Render account (free tier available)
- SendGrid API key (for email)
- Cloudinary account (for image uploads)

## Local Development

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the server directory:

```env
FLASK_ENV=development
FLASK_APP=run.py

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/projectx_db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# SendGrid
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_SENDER_EMAIL=your-email@example.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend
FRONTEND_URL=http://127.0.0.1:5173
```

### 3. Run Migrations

```bash
# Initialize migrations (if not already done)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 4. Run Development Server

```bash
# Using Flask development server
python run.py

# Or using Gunicorn (production-like)
gunicorn run:app --bind 0.0.0.0:5000
```

## Render Deployment

### Method 1: Blueprint (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing `render.yaml`
   - Render will automatically create:
     - PostgreSQL database
     - Web service with auto-deploy

3. **Configure Environment Variables**

   The following are auto-generated:
   - `DATABASE_URL` (from database)
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`

   You must manually add:
   - `SENDGRID_API_KEY`
   - `SENDGRID_SENDER_EMAIL`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `FRONTEND_URL`

### Method 2: Manual Setup

1. **Create PostgreSQL Database**
   - New → PostgreSQL
   - Name: `projectx-db`
   - Region: Oregon (or your preference)
   - Plan: Free

2. **Create Web Service**
   - New → Web Service
   - Connect your GitHub repository
   - Configuration:
     - Name: `projectx-backend`
     - Environment: Python
     - Region: Oregon
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn run:app --bind 0.0.0.0:$PORT`

3. **Add Environment Variables** (same as Method 1)

### Post-Deployment on Render

After first deployment, run migrations:

```bash
# In Render Shell (Dashboard → Service → Shell)
flask db upgrade
```

## CI/CD Setup

### GitHub Actions Configuration

The CI/CD pipeline is configured in `.github/workflows/ci-cd.yml` and runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Pipeline Stages

1. **Test** - Runs unit tests with PostgreSQL
2. **Security Scan** - Checks for vulnerabilities
3. **Build Docker** - Tests Docker build
4. **Deploy** - Auto-deploys to Render (main branch only)

### Setup GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
RENDER_API_KEY=<your-render-api-key>
RENDER_SERVICE_ID=<your-service-id>
```

#### Get Render API Key:
1. Go to Render Dashboard → Account Settings
2. API Keys → Create API Key
3. Copy and add to GitHub Secrets

#### Get Service ID:
1. Go to your service on Render
2. URL will be: `https://dashboard.render.com/web/<SERVICE_ID>`
3. Copy the SERVICE_ID and add to GitHub Secrets

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Flask secret key | Auto-generated on Render |
| `JWT_SECRET_KEY` | JWT signing key | Auto-generated on Render |
| `SENDGRID_API_KEY` | SendGrid API key | `SG.xxx` |
| `SENDGRID_SENDER_EMAIL` | Verified sender email | `noreply@yourdomain.com` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | `your-cloud` |
| `CLOUDINARY_API_KEY` | Cloudinary API key | `123456789` |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | `xxx` |
| `FRONTEND_URL` | Frontend application URL | `https://your-frontend.com` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `PORT` | Server port | `10000` (Render) |

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health endpoint
curl https://your-app.onrender.com/health

# Should return:
{"status": "ok"}
```

### 2. View API Documentation

Visit: `https://your-app.onrender.com/apidocs/`

### 3. Monitor Logs

- Render Dashboard → Your Service → Logs
- Watch for errors or warnings

### 4. Run Database Seeds (Optional)

If you have a seed file:

```bash
# In Render Shell
python seed.py
```

## Common Issues

### Issue: Database Connection Error

**Solution:** Ensure `DATABASE_URL` is properly set and database is running

```bash
# In Render Shell
echo $DATABASE_URL
```

### Issue: Migration Errors

**Solution:** Clear alembic version and re-run migrations

```bash
# In Render Shell or local with production DB
python << EOF
from run import create_app
from app.models import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE;'))
        conn.commit()
EOF

flask db upgrade
```

### Issue: Static Files 404

**Solution:** Render serves static files automatically, ensure routes don't conflict

### Issue: Slow Cold Starts

**Solution:**
- Upgrade to paid plan for always-on instance
- Or implement health check pings every 10 minutes

## Scaling

### Horizontal Scaling
- Render allows multiple instances on paid plans
- Add more workers in start command:
  ```
  gunicorn run:app --bind 0.0.0.0:$PORT --workers 4
  ```

### Database Scaling
- Upgrade PostgreSQL plan on Render
- Add read replicas for read-heavy workloads

### Caching
- Add Redis for session/cache storage
- Use Render's Redis add-on

## Monitoring

### Application Monitoring
- View logs in Render Dashboard
- Set up error tracking (Sentry, Rollbar)

### Database Monitoring
- Render provides built-in database metrics
- Monitor connection pool usage

### Uptime Monitoring
- Use UptimeRobot or similar
- Ping health endpoint every 5 minutes

## Backup Strategy

### Database Backups
- Render provides automatic daily backups (paid plans)
- Manual backups via Render Dashboard

### Manual Backup
```bash
# From local machine
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

## Rollback Strategy

### Code Rollback
1. Render Dashboard → Service → Deploy History
2. Select previous deployment
3. Click "Rollback to this version"

### Database Rollback
```bash
flask db downgrade
```

## Security Checklist

- [ ] All sensitive data in environment variables
- [ ] SECRET_KEY is strong and unique
- [ ] CORS configured for production frontend only
- [ ] Database has strong password
- [ ] API rate limiting enabled
- [ ] HTTPS enforced (automatic on Render)
- [ ] Dependencies updated regularly
- [ ] Security scans passing in CI/CD

## Support

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Report issues: [Your GitHub Issues URL]

---

**Last Updated:** 2025-11-01
**Maintained By:** ProjectX Team
