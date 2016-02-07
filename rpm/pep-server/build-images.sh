#!/bin/bash
set -ex

IMAGE_TAG=argus-authz/pkg.argus-pep-server
tags="centos5 centos6 centos7"

for t in ${tags}; do
  docker build -t ${IMAGE_TAG}:${t} -f Dockerfile.${t} .
done
