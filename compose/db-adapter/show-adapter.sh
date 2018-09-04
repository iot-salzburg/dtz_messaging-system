#!/usr/bin/env bash
echo "Printing 'docker service ls | grep db-adapter':"
docker service ls | grep db-adapter
echo ""
echo "Printing 'docker stack ps db-adapter':"
docker stack ps db-adapter

