#!/bin/bash
set -ex

PLATFORM=${PLATFORM:-centos6}
PACKAGES_DIR=${PACKAGES_DIR:-packages}
MVN_REPO_CONTAINER_NAME=${MVN_REPO_CONTAINER_NAME:-maven-repo}
COMPONENTS=${COMPONENTS:-"pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout"}

mkdir -p ${PACKAGES_DIR}

stage_area_name=$(basename $(mktemp -u -t stage-area-XXXXX))
# Create stage area container
docker create -v /stage-area --name ${stage_area_name} italiangrid/pkg.base:${PLATFORM}

# Run build
for c in ${COMPONENTS}; do
  build_env=""

  while read -r line
  do
    build_env="${build_env} -e ${line}"
  done < "$c/build-env"

  docker run --volumes-from ${stage_area_name} --volumes-from ${MVN_REPO_CONTAINER_NAME} \
    -v ${PKG_REPO_DIR}:/pkg-repo:ro \
    -v ${PACKAGES_DIR}:/packages:rw \
    -ti ${build_env} \
    -e PKG_REPO=file:///pkg-repo \
    argus-authz/pkg.argus-$c:${PLATFORM}
done
