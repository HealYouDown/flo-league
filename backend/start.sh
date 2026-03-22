#!/bin/sh

set -e

echo "⏳ Waiting for database..."

# Wait for Postgres
until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

echo "✅ Database is ready"

# Run migrations (ONLY ONCE)
echo "🚀 Running migrations..."
alembic upgrade head

echo "✅ Migrations done"

# Start server
echo "🔥 Starting server..."
exec gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w ${UVICORN_WORKERS:-2} \
  -b 0.0.0.0:8000