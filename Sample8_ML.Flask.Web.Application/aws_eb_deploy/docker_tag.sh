#!/bin/bash

# Define images and tags
images=("app-v0.0.2" "nginx-v0.0.2" "redis-v0.0.2" "psql-v0.0.2" "celery-v0.0.2")
repository="andrewodrain/web-applications"

# Tag and push images
for image in "${images[@]}"; do
  docker tag "${repository}:${image}" "${repository}:${images}"
  docker push "${repository}:${image}"
done