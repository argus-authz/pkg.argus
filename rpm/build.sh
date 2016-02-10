#!/bin/bash
set -ex

PLATFORM=${PLATFORM:-centos6}
PACKAGES_DIR=${PACKAGES_DIR:-packages}
MVN_REPO_CONTAINER_NAME=${MVN_REPO_CONTAINER_NAME:-maven-repo}
COMPONENTS=${COMPONENTS:-"pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout"}

# Create packages dir, if needed
mkdir -p ${PACKAGES_DIR}

pkg_base_image_name="italiangrid/pkg.base:${PLATFORM}"

if [ -n "${USE_DOCKER_REGISTRY}" ]; then
  pkg_base_image_name="${DOCKER_REGISTRY_HOST}/${pkg_base_image_name}"
fi

if [ -z ${MVN_REPO_CONTAINER_NAME+x} ]; then
  mvn_repo_name=$(basename $(mktemp -u -t mvn-repo-XXXXX))
  # Create mvn repo container
  docker create -v /m2-repository --name ${mvn_repo_name} ${pkg_base_image_name}
else
  mvn_repo_name=${MVN_REPO_CONTAINER_NAME}
fi

# Create stage area data container, if no container is provided
if [ -z ${STAGE_AREA_CONTAINER_NAME+x} ]; then
  stage_area_name=$(basename $(mktemp -u -t stage-area-XXXXX))
  # Create stage area container
  docker create -v /stage-area --name ${stage_area_name} ${pkg_base_image_name}
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

  if [ -n "${PKG_BUILD_NUMBER}" ]; then
    build_env="${build_env} -e BUILD_NUMBER=${PKG_BUILD_NUMBER}"
  fi

  if [ -n "${DATA_CONTAINER_NAME}" ]; then
    volumes_conf="${volumes_conf} --volumes-from ${DATA_CONTAINER_NAME}"

    if [ -n "${DATA_PREFIX}" ]; then
      volumes_conf="-v ${DATA_PREFIX}/${PACKAGES_DIR}:/packages:rw"
      volumes_conf="-v ${DATA_PREFIX}/pkg-repo:/pkg-repo:ro"
      build_env="${build_env} -e PKG_REPO=file:///pkg-repo"
    fi
  else

    volumes_conf="-v ${PACKAGES_DIR}:/packages:rw"

    if [ -n "${PKG_REPO_DIR}" ]; then
      volumes_conf="${volumes_conf} -v ${PKG_REPO_DIR}:/pkg-repo:ro"
      build_env="${build_env} -e PKG_REPO=file:///pkg-repo"
    fi
  fi

  if [ -n "${STAGE_ALL}" ]; then
    if [[ ${build_env} == *"PKG_STAGE_RPMS"* ]]
    then
      echo "PKG_STAGE_RPMS already set by build-env for this build"
    else
      build_env="${build_env} -e PKG_STAGE_RPMS=1"
    fi
  fi

  image_name="argus-authz/pkg.argus-${c}:${PLATFORM}"

  if [ -n "${USE_DOCKER_REGISTRY}" ]; then
    image_name="${DOCKER_REGISTRY_HOST}/${image_name}"
  fi

  docker pull ${image_name}

  docker run -i --volumes-from ${stage_area_name} --volumes-from ${MVN_REPO_CONTAINER_NAME} \
    ${volumes_conf} \
    ${build_env} \
    ${image_name}
done
