# Deployment Checklist

Use this checklist to ensure successful deployment to Render with CI/CD.

## Pre-Deployment

### Code Preparation
- [ ] All tests passing locally
- [ ] Code committed to Git
- [ ] `.env` file excluded from Git (in `.gitignore`)
- [ ] Dependencies updated in `requirements.txt`
- [ ] Database migrations created and tested
- [ ] Sensitive data removed from code

### GitHub Repository
- [ ] Repository created on GitHub
- [ ] Code pushed to `main` branch
- [ ] Repository is public or Render has access
- [ ] `.github/workflows/ci-cd.yml` present

## Render Setup

### Database Setup
- [ ] PostgreSQL database created on Render
- [ ] Database name: `projectx-db`
- [ ] Region selected (e.g., Oregon)
- [ ] Database credentials noted

### Web Service Setup
- [ ] Web service created (Blueprint or Manual)
- [ ] Service name: `projectx-backend`
- [ ] Python environment selected
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn run:app --bind 0.0.0.0:$PORT`
- [ ] Auto-deploy enabled from `main` branch

### Environment Variables
Required variables configured:
- [ ] `DATABASE_URL` (auto-generated from database)
- [ ] `SECRET_KEY` (auto-generated or custom)
- [ ] `JWT_SECRET_KEY` (auto-generated or custom)
- [ ] `SENDGRID_API_KEY`
- [ ] `SENDGRID_SENDER_EMAIL`
- [ ] `CLOUDINARY_CLOUD_NAME`
- [ ] `CLOUDINARY_API_KEY`
- [ ] `CLOUDINARY_API_SECRET`
- [ ] `FRONTEND_URL`
- [ ] `FLASK_ENV=production`

## CI/CD Setup

### GitHub Secrets
- [ ] `RENDER_API_KEY` added to GitHub Secrets
- [ ] `RENDER_SERVICE_ID` added to GitHub Secrets

### Pipeline Verification
- [ ] GitHub Actions workflow running
- [ ] Tests passing in CI
- [ ] Linting checks passing
- [ ] Security scans passing
- [ ] Docker build succeeding

## Post-Deployment

### Initial Deployment
- [ ] First deployment completed successfully
- [ ] No build errors in Render logs
- [ ] Service is "Live" on Render dashboard

### Database Setup
- [ ] Run migrations via Render Shell: `flask db upgrade`
- [ ] (Optional) Seed database: `python seed.py`
- [ ] Verify tables created in database

### Testing
- [ ] Health endpoint responding: `curl https://your-app.onrender.com/health`
- [ ] API documentation accessible: `https://your-app.onrender.com/apidocs/`
- [ ] Test authentication endpoints
- [ ] Test create/read operations
- [ ] Verify CORS with frontend

### Monitoring
- [ ] Check Render logs for errors
- [ ] Verify database connections
- [ ] Test email sending (SendGrid)
- [ ] Test file uploads (Cloudinary)

## Security Checklist

- [ ] All secrets in environment variables
- [ ] Strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Database password is strong
- [ ] CORS configured for production frontend only
- [ ] HTTPS enabled (automatic on Render)
- [ ] No hardcoded credentials in code
- [ ] `.env` file gitignored
- [ ] API rate limiting considered

## Performance Checklist

- [ ] Gunicorn worker count configured (default: 4)
- [ ] Database connection pooling configured
- [ ] Static file serving optimized
- [ ] Compression enabled
- [ ] Health check endpoint responding quickly

## Maintenance

### Regular Tasks
- [ ] Monitor Render logs weekly
- [ ] Update dependencies monthly
- [ ] Review security scans
- [ ] Check database usage/limits
- [ ] Backup database regularly (paid plans)

### Scaling Considerations
- [ ] Monitor response times
- [ ] Check database query performance
- [ ] Consider upgrading to paid plan if needed
- [ ] Plan for increased worker counts
- [ ] Consider adding Redis for caching

## Rollback Plan

### If Deployment Fails
1. [ ] Check Render logs for errors
2. [ ] Verify environment variables
3. [ ] Check database connectivity
4. [ ] Rollback to previous deployment via Render dashboard
5. [ ] Fix issues locally and redeploy

### Database Rollback
1. [ ] Run `flask db downgrade` in Render Shell
2. [ ] Verify database state
3. [ ] Test application functionality

## Support Resources

- [ ] Render documentation reviewed: https://render.com/docs
- [ ] Flask deployment guide reviewed
- [ ] Team members have access to Render dashboard
- [ ] Emergency contacts documented

## Final Verification

- [ ] Application accessible via production URL
- [ ] All features working as expected
- [ ] Frontend can connect to backend
- [ ] Authentication flow working
- [ ] Email notifications working
- [ ] File uploads working
- [ ] No console errors
- [ ] API documentation accurate

## Sign-off

- **Deployed By:** _________________
- **Date:** _________________
- **Production URL:** https://_________________.onrender.com
- **Status:** [ ] Success  [ ] Issues (document below)

### Issues Encountered:
```
(Document any issues and resolutions here)
```

---

**Deployment Completed:** ___/___/_____
