#!/usr/bin/env bash

docker-compose down
docker build -t api .
docker-compose up -d