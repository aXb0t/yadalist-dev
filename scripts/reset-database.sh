#!/bin/bash
# Reset production database - WARNING: This deletes all data!

set -e

echo "WARNING: This will delete ALL data in the database!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

echo "Stopping services..."
docker compose down

echo "Removing database volume..."
docker volume rm schmango_postgres_data || true

echo "Starting database..."
docker compose up -d db

echo "Waiting for database to be ready..."
sleep 10

echo "Running migrations..."
docker compose run --rm web python manage.py migrate

echo "Creating superuser (you'll be prompted for credentials)..."
docker compose run --rm web python manage.py createsuperuser

echo "Collecting static files..."
docker compose run --rm web python manage.py collectstatic --noinput

echo "Starting all services..."
docker compose up -d

echo "Database reset complete!"
