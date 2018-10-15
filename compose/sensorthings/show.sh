#!/usr/bin/env bash
echo "Printing 'docker service ls | grep st_':"
docker service ls | grep st_
echo ""
echo "Printing 'docker stack ps st_gost-db':"
docker stack ps st_gost-db
