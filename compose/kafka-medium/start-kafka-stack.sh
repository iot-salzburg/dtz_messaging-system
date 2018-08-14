docker build -t kafka ./base-image
docker stack deploy --compose-file swarm-docker-compose.yml kafka
