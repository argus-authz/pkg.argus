#!/bin/bash
set -ex

sudo yum -y install argus-pep-api-c-devel \
  globus-gridmap-callout-error-devel \
  globus-gssapi-gsi-devel \
  globus-gssapi-error-devel \
  globus-gss-assist-devel
