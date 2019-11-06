#!/usr/bin/env bash

here=$(dirname $0)

"$here/up.sh"

echo "=> Building frontend image..."
docker build -t nick96/attendance-badgetracking-frontend -f frontend/Dockerfile frontend
echo "=> Starting..."
env $(cat frontend/.env) docker-compose -f api/docker-compose.yml -f frontend/docker-compose.yml up "$@"