#!/bin/bash

set -ex

set -a
source ./build-env
set +a

PLATFORM=${PLATFORM:-centos7}
ALL_COMPONENTS="pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout metapackage"

COMPONENTS=${COMPONENT_LIST:-${COMPONENTS}}
COMPONENTS=${COMPONENTS:-${ALL_COMPONENTS}}

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

if [ -z "${SKIP_PKG_BASE_PULL_IMAGE}" ]; then
 docker pull ${pkg_base_image_name}
fi

# Run packaging
for c in ${COMPONENTS}; do
  build_env_file="$c/build-env"
  comp_name=$(echo ${c} | tr '[:lower:]' '[:upper:]' | tr '-' '_')
  
  var_names="BUILD_REPO PKG_PACKAGES_DIR PKG_STAGE_DIR PKG_TAG PKG_REPO PKG_STAGE_RPMS"
  
  for v in ${var_names}; do
    c_var_name="${v}_${comp_name}"

    if [ -n "${!c_var_name}" ]; then
      build_env="${build_env} -e ${v}=${!c_var_name}"
    elif [ -n "${!v}" ]; then
        build_env="${build_env} -e ${v}=${!v}"
    fi
  done
 
  if [ "${INCLUDE_BUILD_NUMBER}" == "1" ]; then
    build_env="${build_env} -e BUILD_NUMBER=${PKG_BUILD_NUMBER:-test}"
  fi

  if [ -n "${DATA_CONTAINER_NAME}" ]; then
    volumes_conf="${volumes_conf} --volumes-from ${DATA_CONTAINER_NAME}"
  fi

  docker run -i --volumes-from ${mvn_repo_name} \
    ${volumes_conf} \
    ${DOCKER_ARGS} \
    --env-file ${build_env_file} \
    ${build_env} \
    ${pkg_base_image_name}
	
done
