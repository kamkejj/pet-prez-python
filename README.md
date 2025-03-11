# Python SQLAlchemy PostgreSQL Docker Setup

This project provides a complete development environment for a Python Flask application with SQLAlchemy ORM, PostgreSQL database, and pgAdmin for database management.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```
.
├── app.py                  # Flask application
├── models/models.py        # SQLAlchemy models
├── migrate.py              # Database migration script
├── alembic.ini             # Alembic configuration
├── migrations/             # Alembic migrations directory
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
└── requirements.txt        # Python dependencies
```

## Getting Started

### Starting the Application

1. Build and start all containers:
   ```bash
   docker-compose up -d
   ```

2. View logs to monitor startup:
   ```bash
   docker-compose logs -f
   ```

3. Access the application at [http://localhost:8000](http://localhost:8000)

4. Access pgAdmin at [http://localhost:5050](http://localhost:5050)
   - Email: admin@example.com
   - Password: adminpassword

### Stopping the Application

1. Stop all containers:
   ```bash
   docker-compose down
   ```

2. Stop and remove volumes (deletes database data):
   ```bash
   docker-compose down -v
   ```

### Rebuilding Containers

If you make changes to the Dockerfile or requirements.txt:
```bash
docker-compose build
docker-compose up -d
```

## Database Migrations

### Running Migrations

Migrations run automatically when the container starts, but you can also run them manually:

```bash
docker-compose exec web python migrate.py
```

### Creating a New Migration

1. Make changes to your models in `models.py`

2. Generate a new migration:
   ```bash
   docker-compose exec web bash -c "PYTHONPATH=/app alembic revision --autogenerate -m 'description_of_changes'"
   ```

3. Apply the migration:
   ```bash
   docker-compose exec web bash -c "PYTHONPATH=/app alembic upgrade head"
   ```

### Managing Migrations

- Show migration history:
  ```bash
  docker-compose exec web bash -c "PYTHONPATH=/app alembic history"
  ```

- Show current migration version:
  ```bash
  docker-compose exec web bash -c "PYTHONPATH=/app alembic current"
  ```

- Downgrade one migration:
  ```bash
  docker-compose exec web bash -c "PYTHONPATH=/app alembic downgrade -1"
  ```

- Downgrade to a specific migration:
  ```bash
  docker-compose exec web bash -c "PYTHONPATH=/app alembic downgrade <migration_id>"
  ```

- Downgrade all migrations (revert to empty database):
  ```bash
  docker-compose exec web bash -c "PYTHONPATH=/app alembic downgrade base"
  ```

## Connecting to PostgreSQL

### Via pgAdmin

1. Access pgAdmin at [http://localhost:5050](http://localhost:5050)
2. Log in with provided credentials
3. Add a new server:
   - Name: Any name
   - Host: db
   - Port: 5432
   - Database: postgres
   - Username: postgres
   - Password: postgres

### Via Command Line

```bash
docker-compose exec db psql -U postgres
```

## Troubleshooting

### Container Won't Start / Keeps Restarting

Check the logs:
```bash
docker-compose logs web
```

### Database Connection Issues

Check if PostgreSQL is running:
```bash
docker-compose exec db pg_isready
```

Test connection from web container:
```bash
docker-compose exec web python -c "import psycopg2; conn = psycopg2.connect('postgresql://postgres:postgres@db:5432/postgres'); print('Connected!')"
```

### Migration Issues

If you encounter "No module named 'models'" errors, use the PYTHONPATH environment variable:
```bash
docker-compose exec web bash -c "PYTHONPATH=/app alembic current"
```

# JWT Authentication

This application uses JWT (JSON Web Tokens) for authentication. Here's how to use it:

## Authentication Endpoints

### Register a New User
```
POST /auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "pet_name": "Fluffy",
  "pet_species": "Cat"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

### Login
```
POST /auth/login
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "pet_name": "Fluffy",
    "pet_species": "Cat",
    "created_at": "2025-03-11T12:34:56"
  }
}
```

## Using Protected Routes

For routes that require authentication, include the JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Protected Routes

- `GET /users/me` - Get current user's profile
- `POST /slogans` - Create a new slogan (requires authentication)

### Public Routes

- `GET /users/<username>` - Get user by username
- `GET /users/<username>/slogans` - Get user's slogans by username
- `GET /slogans` - Get all slogans
- `GET /health` - API health check

## Example: Creating a Slogan (Protected Route)

```
POST /slogans
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "slogan": "Just Do It!"
}
```

**Response (201 Created):**
```json
{
  "message": "Slogan created successfully",
  "slogan": {
    "id": 1,
    "user_id": 1,
    "slogan": "Just Do It!",
    "created_at": "2025-03-11T12:34:56"
  }
}
```

## Testing Authentication with curl

**Register a user:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

**Access protected route:**
```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
