#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
# Mark existing migrations as applied without running them
python manage.py migrate --fake hello 0001_initial || true
python manage.py migrate

echo "✅ Build complete!"
