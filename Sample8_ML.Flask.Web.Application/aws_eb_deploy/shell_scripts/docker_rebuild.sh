#!/bin/bash

images=("app-v0.0.2" "nginx-v0.0.2" "redis-v0.0.2" "psql-v0.0.2" "celery-v0.0.2")
repository="andrewodrain/web-applications"


docker compose down
docker compose down --volumes

for images in "${images[@]}"; do
  docker rmi "${repository}:${images}"
done

docker compose up --build -d

#clear





































