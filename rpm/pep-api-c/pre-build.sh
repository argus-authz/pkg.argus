if [ "${BUILD_PLATFORM}" = "centos5" ]; then
  yum -y install curl-devel
else
  yum -y install libcurl-devel
fi
