#!/usr/bin/env bash
# Render build script — runs once per deploy.
#
# First deploy:  set SEED_DB=true in Render env vars → seeds the DB.
# Later deploys: leave SEED_DB unset (or false) → skip seeding so real
#                data entered through the admin panel is never wiped.
set -o errexit

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Collecting static files"
python manage.py collectstatic --no-input

echo "==> Running migrations"
python manage.py migrate

if [[ "${SEED_DB:-false}" == "true" ]]; then
    echo "==> Seeding database (SEED_DB=true)"
    python manage.py seed_all
    echo "==> Seeding complete"
fi
