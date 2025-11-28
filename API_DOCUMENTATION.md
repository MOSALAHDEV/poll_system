# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

### Obtain JWT Token
**Endpoint:** `POST /api/token/`

**Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Polls

### Create Poll
**Endpoint:** `POST /api/polls/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request:**
```json
{
  "title": "Favorite Programming Language",
  "description": "Vote for your favorite programming language",
  "expires_at": "2024-12-31T23:59:59Z",
  "choices": [
    {"text": "Python"},
    {"text": "JavaScript"},
    {"text": "Java"},
    {"text": "Go"}
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Favorite Programming Language",
  "description": "Vote for your favorite programming language",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-12-31T23:59:59Z",
  "status": "OPEN",
  "choices": [
    {"id": 1, "text": "Python"},
    {"id": 2, "text": "JavaScript"},
    {"id": 3, "text": "Java"},
    {"id": 4, "text": "Go"}
  ]
}
```

---

### List Active Polls
**Endpoint:** `GET /api/polls/`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Favorite Programming Language",
    "description": "Vote for your favorite programming language",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": "2024-12-31T23:59:59Z",
    "status": "OPEN",
    "choices": [
      {"id": 1, "text": "Python"},
      {"id": 2, "text": "JavaScript"}
    ]
  }
]
```

---

### Get Poll Details
**Endpoint:** `GET /api/polls/{id}/`

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Favorite Programming Language",
  "description": "Vote for your favorite programming language",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-12-31T23:59:59Z",
  "status": "OPEN",
  "choices": [
    {"id": 1, "text": "Python"},
    {"id": 2, "text": "JavaScript"},
    {"id": 3, "text": "Java"},
    {"id": 4, "text": "Go"}
  ]
}
```

---

### Vote on Poll
**Endpoint:** `POST /api/polls/{id}/vote/`

**Request:**
```json
{
  "choice_id": 1,
  "voter_identifier": "user@example.com"
}
```

**Response:** `201 Created`
```json
{
  "message": "Vote recorded successfully"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "non_field_errors": ["You have already voted on this poll."]
}
```

---

### Get Poll Results
**Endpoint:** `GET /api/polls/{id}/results/`

**Response:** `200 OK`
```json
{
  "poll": "Favorite Programming Language",
  "total_votes": 150,
  "results": [
    {"choice": "Python", "votes": 65},
    {"choice": "JavaScript", "votes": 45},
    {"choice": "Java", "votes": 25},
    {"choice": "Go", "votes": 15}
  ]
}
```

---

### Close Poll
**Endpoint:** `POST /api/polls/{id}/close/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Poll closed successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Validation Rules

### Poll Creation
- `title`: Required, max 255 characters
- `description`: Required
- `expires_at`: Required, must be future datetime
- `choices`: Required, minimum 2 choices

### Voting
- `choice_id`: Required, must exist in poll
- `voter_identifier`: Required, max 255 characters
- One vote per voter per poll
- Poll must be OPEN and not expired

---

## Rate Limiting
Currently no rate limiting is implemented. Consider adding it for production.

## CORS
Configure CORS settings in production to allow frontend access.
