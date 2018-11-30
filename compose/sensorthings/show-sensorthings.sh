#!/usr/bin/env bash
echo "Printing 'docker service ls | grep st_':"
docker service ls | grep st_
echo ""
echo "Printing 'docker service ps st_gost-db':"
docker service ps st_gost-db
