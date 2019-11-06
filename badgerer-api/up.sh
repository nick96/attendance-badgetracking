#!/usr/bin/env bash

here=$(dirname $0)

echo "=> Building backend image..."
docker build -t nick96/attendance-badgetracking-backend -f "$here/Dockerfile" "$here"

echo "=> Starting backend..."
env $(cat "$here/.env") docker-compose -f "$here/docker-compose.yml" up -d

echo "=> Backend is running"````