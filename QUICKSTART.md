# Quick Start Guide

## Option 1: Docker (Recommended for Quick Setup)

### Prerequisites
- Docker and Docker Compose installed

### Steps
```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the API
# API: http://localhost:8000/api/
# Swagger: http://localhost:8000/swagger/
# Admin: http://localhost:8000/admin/
```

---

## Option 2: Local Setup

### Prerequisites
- Python 3.12
- PostgreSQL installed and running

### Steps

1. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL database**
```bash
# Create database
createdb polldb

# Or using psql
psql -U postgres
CREATE DATABASE polldb;
\q
```

4. **Configure environment**
Edit `.env` file with your database credentials:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=polldb
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

---

## Testing the API

### 1. Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### 2. Create a Poll
```bash
curl -X POST http://localhost:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Best Framework",
    "description": "Vote for the best web framework",
    "expires_at": "2024-12-31T23:59:59Z",
    "choices": [
      {"text": "Django"},
      {"text": "Flask"},
      {"text": "FastAPI"}
    ]
  }'
```

### 3. List Polls
```bash
curl http://localhost:8000/api/polls/
```

### 4. Vote on a Poll
```bash
curl -X POST http://localhost:8000/api/polls/1/vote/ \
  -H "Content-Type: application/json" \
  -d '{
    "choice_id": 1,
    "voter_identifier": "user@example.com"
  }'
```

### 5. Get Results
```bash
curl http://localhost:8000/api/polls/1/results/
```

---

## Running Tests

```bash
# Using pytest
pytest

# Using Django test runner
python manage.py test

# With coverage
pytest --cov=polls
```

---

## Next Steps

1. Explore the Swagger UI at http://localhost:8000/swagger/
2. Check API_DOCUMENTATION.md for detailed endpoint information
3. Read DEPLOYMENT.md for production deployment instructions
4. Customize the models and add more features as needed

---

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -l`

### Port Already in Use
```bash
# Change port in docker-compose.yml or use different port
python manage.py runserver 8001
```

### Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate polls zero
python manage.py makemigrations
python manage.py migrate
```
