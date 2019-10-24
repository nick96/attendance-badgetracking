#!/usr/bin/env bash

echo "=> Building backend image..."
docker build -t nick96/attendance-badgetracking-backend -f api/Dockerfile api
echo "=> Building frontend image..."
docker build -t nick96/attendance-badgetracking-frontend -f frontend/Dockerfile frontend
echo "=> Starting..."
source api/.env
env $(cat api/.env) $(cat frontend/.env) docker-compose -f api/docker-compose.yml -f frontend/docker-compose.yml up "$@"