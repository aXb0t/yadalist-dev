# Schmango

Django web application with PostgreSQL backend and modern frontend tooling.

## Local Development

### Start the application
```bash
docker-compose up
```

This starts:
- PostgreSQL database (port 5432)
- Django development server (http://localhost:8000)
- Frontend build with hot-reload CSS
- Storybook component library (http://localhost:6006)

### Run migrations
```bash
docker-compose run --rm web python manage.py migrate
```

### Create superuser
```bash
docker-compose run --rm web python manage.py createsuperuser
```

### Run tests
```bash
docker-compose run --rm web python manage.py test
```

### Reset containers (fresh start)
```bash
docker-compose down -v
docker-compose up --build
```

## Settings

The project uses environment-specific settings:

- **development** (`schmango.settings.development`) - Local dev with PostgreSQL via docker-compose
- **testing** (`schmango.settings.testing`) - CI/Jenkins with SQLite in-memory
- **production** (`schmango.settings.production`) - Production deployment

## Deployment

### CI/CD Pipeline (Jenkins)

1. **Build** - Builds frontend assets and Docker image
2. **Test** - Runs Django tests with SQLite
3. **Deploy** - Deploys to homelab or production environment

### Manual Deployment

The application is deployed using `docker-compose.prod.yml` on remote servers. The Jenkins pipeline handles:
- Building and transferring Docker images
- Running database migrations
- Collecting static files
- Starting services with nginx reverse proxy
