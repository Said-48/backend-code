# ProjectX Backend API

A Flask-based REST API for managing projects, tasks, users, cohorts, and classes with authentication and authorization.

[![CI/CD Pipeline](https://github.com/your-username/your-repo/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/your-username/your-repo/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- **User Authentication** - JWT-based authentication with 2FA support
- **Project Management** - Create, manage, and collaborate on projects
- **Task Management** - Assign and track tasks within projects
- **User Roles** - Admin and Student role-based access control
- **Cohort System** - Organize users into cohorts
- **Class Management** - Manage different specialization tracks
- **Activity Logging** - Track user actions and changes
- **API Documentation** - Auto-generated Swagger/OpenAPI docs
- **Email Notifications** - SendGrid integration for emails
- **Image Uploads** - Cloudinary integration

## Tech Stack

- **Framework:** Flask 3.0.3
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Authentication:** JWT (PyJWT) with 2FA (PyOTP)
- **Migrations:** Flask-Migrate (Alembic)
- **Email:** SendGrid
- **Storage:** Cloudinary
- **Testing:** Pytest with coverage
- **Production Server:** Gunicorn
- **API Docs:** Flasgger (Swagger)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- SendGrid API key
- Cloudinary account

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd server

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Create .env and fill in your values

# Run database migrations
flask db upgrade

# (Optional) Seed database
python seed.py

# Run development server
python run.py
```

The API will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/projectx_db

# JWT
JWT_SECRET_KEY=your-jwt-secret

# SendGrid
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_SENDER_EMAIL=your-email@example.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend
FRONTEND_URL=http://127.0.0.1:5173
```

## API Documentation

Once the server is running, visit:

- **Swagger UI:** `http://localhost:5000/apidocs/`
- **API Spec:** `http://localhost:5000/apispec_1.json`

### Main Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/enable-2fa` - Enable two-factor authentication
- `POST /auth/verify-2fa` - Verify 2FA code

#### Users
- `GET /users/` - List all users (Admin only)
- `GET /users/<id>` - Get user by ID
- `POST /users/` - Create user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

#### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create project
- `GET /projects/<id>` - Get project by ID
- `PUT /projects/<id>` - Update project
- `DELETE /projects/<id>` - Delete project
- `PATCH /projects/<id>/status` - Update project status

#### Tasks
- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create task
- `GET /tasks/<id>` - Get task by ID
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task
- `GET /tasks/project/<project_id>` - Get tasks by project

#### Classes
- `GET /classes/` - List all classes
- `POST /classes/` - Create class (Admin only)
- `GET /classes/<id>` - Get class by ID
- `PUT /classes/<id>` - Update class (Admin only)
- `DELETE /classes/<id>` - Delete class (Admin only)
- `GET /classes/<id>/students` - Get students in class

#### Cohorts
- `GET /cohorts/` - List all cohorts
- `POST /cohorts/` - Create cohort
- `PUT /cohorts/<id>` - Update cohort
- `DELETE /cohorts/<id>` - Delete cohort
- `POST /cohorts/<id>/join` - Join cohort

#### Activity Logs
- `GET /activities/activities` - List activities (Admin only)

## Testing

```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run with coverage
PYTHONPATH=. pytest tests/ --cov=app --cov-report=html

# Run specific test file
PYTHONPATH=. pytest tests/test_auth.py -v

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

## Database Migrations

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to Render

1. Push code to GitHub
2. Create account on [Render](https://render.com)
3. New → Blueprint
4. Connect repository
5. Render auto-deploys from `render.yaml`

### Docker Deployment

```bash
# Build image
docker build -t projectx-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=your-db-url \
  -e SECRET_KEY=your-secret \
  projectx-backend
```

## Project Structure

```
server/
├── app/
│   ├── models.py           # Database models
│   ├── config.py           # Configuration
│   └── routes/             # API routes
│       ├── auth_routes.py
│       ├── user_routes.py
│       ├── project_routes.py
│       ├── task_routes.py
│       ├── class_routes.py
│       ├── cohort_routes.py
│       ├── member_routes.py
│       └── activity_routes.py
├── migrations/             # Database migrations
├── tests/                  # Test files
├── run.py                  # Application entry point
├── seed.py                 # Database seeding
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── render.yaml             # Render deployment config
└── .github/
    └── workflows/
        └── ci-cd.yml       # CI/CD pipeline
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Linting** - Code quality checks with flake8
2. **Testing** - Automated tests with pytest
3. **Security** - Vulnerability scanning with safety and bandit
4. **Build** - Docker image build test
5. **Deploy** - Auto-deploy to Render on main branch

View pipeline status in the Actions tab of your GitHub repository.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Write tests for new features

## Security

- Never commit `.env` file or secrets
- Use environment variables for sensitive data
- Keep dependencies updated
- Follow security best practices
- Report security issues privately

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues:** [GitHub Issues](https://github.com/your-username/your-repo/issues)
- **Email:** support@yourproject.com

## Acknowledgments

- Flask framework and community
- SQLAlchemy ORM
- PostgreSQL database
- Render hosting platform
- All contributors

---

**Built with Flask** | **Deployed on Render** | **Powered by PostgreSQL**
