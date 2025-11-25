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

## Database Workflow

### Pull Database from Server

Before making database model changes, **always sync your local database** with the deployment environment:

```bash
./scripts/pull
```

This command (inspired by Lando/Platform.sh) will:
1. Interactively select environment (testing/production)
2. Dump the remote database
3. Replace your local database with the remote copy
4. Ensure migration consistency

Or specify the environment directly:
```bash
./scripts/pull testing
./scripts/pull production
```

### Creating Migrations

After syncing, make your model changes and create migrations:

```bash
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
```

Test locally, then commit and deploy through Jenkins.

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

### Migration Issues

**Error: `InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency accounts.0001_initial`**

This occurs when the database was initialized before the custom User model was added. Solutions:

**Option 1: Reset Database (no data loss acceptable)**
```bash
# On the deployment server
cd /opt/schmango
./scripts/reset-database.sh
```

**Option 2: Fake Migrations (preserve existing data)**
```bash
# On the deployment server
cd /opt/schmango
docker compose run --rm web python manage.py migrate --fake accounts 0001_initial
docker compose run --rm web python manage.py migrate
```

Note: Option 2 only works if your database schema matches what the migrations would create.
