# Multi tenant app 

# How to run and test
- Use `docker compose up` to startup database and backend (tested with Docker version 24.0.6, build ed223bc, Docker Compose version v2.22.0-desktop.2, Mac M2)
- Run migrations with `docker exec -it backend poetry run python manage.py migrate`
- Run unit tests with `docker exec -it backend poetry run pytest`
- Access application docs at http://localhost:8000/api/schema/swagger-ui/

# Architecture
- Database uses shared tenant "public" to store tenants and user data
- Each tenant has its own schema to store its related models data