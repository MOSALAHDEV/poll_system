# Start the Server

## ✅ Setup Complete!

Database has been migrated and superuser created.

**Credentials:**
- Username: `admin`
- Password: `admin123`

## Start the Development Server

Run this command:

```bash
cd /home/salah/Downloads/poll_system
venv/bin/python manage.py runserver
```

## Access the Application

Once the server is running:

- **API Base**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **ReDoc**: http://localhost:8000/redoc/

## Quick Test

### 1. Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Create a Poll
```bash
curl -X POST http://localhost:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Best Programming Language",
    "description": "Vote for your favorite",
    "expires_at": "2024-12-31T23:59:59Z",
    "choices": [
      {"text": "Python"},
      {"text": "JavaScript"},
      {"text": "Java"}
    ]
  }'
```

### 3. Vote on Poll
```bash
curl -X POST http://localhost:8000/api/polls/1/vote/ \
  -H "Content-Type: application/json" \
  -d '{
    "choice_id": 1,
    "voter_identifier": "user@example.com"
  }'
```

### 4. Get Results
```bash
curl http://localhost:8000/api/polls/1/results/
```

## Database

Currently using **SQLite** (db.sqlite3) for local development.

For production with PostgreSQL, set DATABASE_URL in .env:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```
