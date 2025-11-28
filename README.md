# Online Poll System Backend

A RESTful API backend for an online polling system built with Django and PostgreSQL.

## Features

- Create polls with multiple choices
- Vote on active polls (one vote per user)
- Real-time result calculation
- JWT authentication
- Automatic poll expiry
- Swagger API documentation

## Tech Stack

- Django 4.2.7
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Swagger/OpenAPI

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
cd poll_system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=polldb
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb polldb

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Access the API at: `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Polls
- `POST /api/polls/` - Create a new poll
- `GET /api/polls/` - List active polls
- `GET /api/polls/{id}/` - Get poll details
- `POST /api/polls/{id}/vote/` - Vote on a poll
- `GET /api/polls/{id}/results/` - Get poll results
- `POST /api/polls/{id}/close/` - Close a poll

### Documentation
- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc UI

## API Usage Examples

### Create a Poll

```bash
curl -X POST http://localhost:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Favorite Programming Language",
    "description": "Vote for your favorite language",
    "expires_at": "2024-12-31T23:59:59Z",
    "choices": [
      {"text": "Python"},
      {"text": "JavaScript"},
      {"text": "Java"}
    ]
  }'
```

### Vote on a Poll

```bash
curl -X POST http://localhost:8000/api/polls/1/vote/ \
  -H "Content-Type: application/json" \
  -d '{
    "choice_id": 1,
    "voter_identifier": "user@example.com"
  }'
```

### Get Results

```bash
curl http://localhost:8000/api/polls/1/results/
```

## Running Tests

```bash
pytest
# or
python manage.py test
```

## Deployment

### Render/Railway

1. Push code to GitHub
2. Connect repository to Render/Railway
3. Add environment variables
4. Deploy

### Environment Variables for Production

```
SECRET_KEY=<strong-secret-key>
DEBUG=False
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=5432
ALLOWED_HOSTS=yourdomain.com
```

## Security Features

- JWT authentication
- Input validation
- Duplicate vote prevention
- CSRF protection
- SQL injection prevention (Django ORM)

## License

MIT
