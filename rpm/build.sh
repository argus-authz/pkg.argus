#!/bin/bash
set -ex

PLATFORM=${PLATFORM:-centos6}
PACKAGES_DIR=${PACKAGES_DIR:-packages}
MVN_REPO_CONTAINER_NAME=${MVN_REPO_CONTAINER_NAME:-maven-repo}
COMPONENTS=${COMPONENTS:-"pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout"}

# Create packages dir, if needed
mkdir -p ${PACKAGES_DIR}

# Create stage area data container, if no container is provided
if [ -z ${STAGE_AREA_CONTAINER_NAME+x} ]; then
  stage_area_name=$(basename $(mktemp -u -t stage-area-XXXXX))
  # Create stage area container
  docker create -v /stage-area --name ${stage_area_name} italiangrid/pkg.base:${PLATFORM}
else
  stage_area_name="${STAGE_AREA_CONTAINER_NAME}"
fi

# Run packaging
for c in ${COMPONENTS}; do
  build_env=""

  while read -r line
  do
    build_env="${build_env} -e ${line}"
  done < "$c/build-env"

  if [ -n "${BUILD_NUMBER}" ]; then
    build_env="${build_env} -e BUILD_NUMBER=${BUILD_NUMBER}"
  fi

  volumes_conf="-v ${PACKAGES_DIR}:/packages:rw"

  if [ -n "${PKG_REPO_DIR}" ]; then
    volumes_conf="${volumes_conf} -v ${PKG_REPO_DIR}:/pkg-repo:ro"
    build_env="${build_env} -e PKG_REPO=file:///pkg-repo"
  fi

  image_name="argus-authz/pkg-argus-${c}:${PLATFORM}"

  if [ -n "${USE_DOCKER_REGISTRY}" ]; then
    image_name="${DOCKER_REGISTRY_HOST}/${image_name}"
  fi

  docker pull ${image_name}

  docker run -ti --volumes-from ${stage_area_name} --volumes-from ${MVN_REPO_CONTAINER_NAME} \
    ${volumes_conf} \
    ${build_env} \
    ${image_name}
done
