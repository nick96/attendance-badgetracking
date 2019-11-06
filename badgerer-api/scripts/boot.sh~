#!/usr/bin/env bash
echo "=> Upgrading database..."
flask db upgrade
echo "=> Database upgraded"
cd ..
echo "=> Starting server..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - "api.app:create_app()"