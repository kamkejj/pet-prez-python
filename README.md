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

3. Access the application at [http://localhost:5000](http://localhost:8000)

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