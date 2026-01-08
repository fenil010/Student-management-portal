#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
# Fake all migrations since tables already exist
python manage.py migrate --fake

echo "✅ Build complete!"
