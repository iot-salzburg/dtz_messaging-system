#!/usr/bin/env bash
sudo docker-compose build
sudo docker-compose push || true
sudo docker stack deploy --compose-file docker-compose.yml db-adapter
