#!/bin/bash
set -ex
tags=${tags:-"centos5 centos6 centos7"}

IMAGE_TAG=argus-authz/pkg.argus-pep-api-java

if [ -z "${DOCKER_REGISTRY_HOST}" ]; then
  echo "Please define the DOCKER_REGISTRY_HOST environment variable before running this script."
  exit 1
fi

for t in ${tags}; do
  docker tag -f  ${IMAGE_TAG}:${t} ${DOCKER_REGISTRY_HOST}/${IMAGE_TAG}:${t}
  docker push ${DOCKER_REGISTRY_HOST}/${IMAGE_TAG}:${t}
done
