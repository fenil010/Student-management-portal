#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "👥 Populating demo data..."
python populate_demo_data.py

echo "✅ Build complete!"
