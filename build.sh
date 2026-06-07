#!/usr/bin/env bash
# Render build script — runs once per deploy.
#
# First deploy:  set SEED_DB=true in Render env vars → seeds the DB.
# Later deploys: leave SEED_DB unset (or false) → skip seeding so real
#                data entered through the admin panel is never wiped.
set -o errexit

# Force production settings for all manage.py calls in this script.
# manage.py defaults to 'development' (SQLite); without this override
# migrations would run against SQLite instead of Supabase PostgreSQL.
export DJANGO_SETTINGS_MODULE=interlink_backend.settings.production

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Collecting static files"
python manage.py collectstatic --no-input

echo "==> Running migrations"
python manage.py migrate


python manage.py seed_all


