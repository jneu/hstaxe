#!/bin/bash

set \
    -o errexit \
    -o pipefail \
    -o nounset

#
# wcstools_build.bash [version]
#
# download, build, and locally install the WCSTools as part of the HSTaXe
# build, optionally specifying the version
#

# WCSTools version to build
WCSTOOLS_VERSION_DEFAULT='3.9.7'
WCSTOOLS_VERSION=${1:-$WCSTOOLS_VERSION_DEFAULT}

WCSTOOLS_DIR="wcstools-${WCSTOOLS_VERSION}" # build directory
WCSTOOLS_TARBALL="${WCSTOOLS_DIR}.tar.gz" # source tarball
WCSTOOLS_URL="http://tdc-www.harvard.edu/software/wcstools/${WCSTOOLS_TARBALL}" # source tarball URL
WCSTOOLS_INSTALL="wcstools-install" # install directory

# download WCSTools source if necessary
test -e "$WCSTOOLS_TARBALL" ||
    curl -OL "$WCSTOOLS_URL"

# unpack the source if necessary
test -d "$WCSTOOLS_DIR" ||
    tar xzf "$WCSTOOLS_TARBALL"

# build libwcs using make
make -C "${WCSTOOLS_DIR}/libwcs" libwcs.a

# populate the install directories
mkdir -p "${WCSTOOLS_INSTALL}"/{include,lib}
ln -s -f "../../${WCSTOOLS_DIR}/libwcs/libwcs.a" "${WCSTOOLS_INSTALL}/lib/" &&
ln -s -f "../../${WCSTOOLS_DIR}"/libwcs/{wcs,wcslib,fitshead,fitsfile}.h "${WCSTOOLS_INSTALL}/include/"
