#!/bin/bash

components="pap pdp-pep-common pep-common pdp pep-server pep-api-c pep-api-java pepcli gsi-pep-callout"

for c in ${components}; do
  pushd $c
  sh build-images.sh
  popd
done
