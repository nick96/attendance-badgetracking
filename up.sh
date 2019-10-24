#!/usr/bin/env bash

docker-compose -f api/docker-compose.yml -f frontend/docker-compose.yml up $@