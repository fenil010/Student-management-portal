#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
python manage.py migrate --fake-initial

echo "✅ Build complete!"
