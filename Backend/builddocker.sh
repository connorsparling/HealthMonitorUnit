#!/bin/sh

docker image build -t hmu-backend .
# docker container run --publish 8000:8080 --detach --name bb hmu-backend
docker tag hmu-backend gcr.io/healthmonitorunit-backend/hmu-backend
docker push gcr.io/healthmonitorunit-backend/hmu-backend
gcloud container images list-tags gcr.io/healthmonitorunit-backend/hmu-backend