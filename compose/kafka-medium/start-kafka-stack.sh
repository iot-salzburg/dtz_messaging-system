docker build -t kafka ./base-image
docker-compose build
docker-compose push || true
docker stack deploy --compose-file swarm-docker-compose.yml kafka
