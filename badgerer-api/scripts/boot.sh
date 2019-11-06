#!/usr/bin/env bash
FLASK_APP="$1"

echo "=> Upgrading database..."
flask db upgrade
echo "=> Database upgraded"
cd ..
echo "=> Starting server..."
exec gunicorn -b :5000 --access-logfile - --error-logfile - "$FLASK_APP:create_app()"
