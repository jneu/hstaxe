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
WCSTOOLS_OLD_URL="http://tdc-www.harvard.edu/software/wcstools/Old/${WCSTOOLS_TARBALL}" # archive tarball URL
WCSTOOLS_INSTALL="wcstools-install" # install directory

# unpack the source (if necessary)
if test ! -d "$WCSTOOLS_DIR"; then

    # download WCSTools source (if necessary)
    if test ! -e "$WCSTOOLS_TARBALL"; then
        if ! curl -OfL "$WCSTOOLS_URL"; then
            curl -OfL "$WCSTOOLS_OLD_URL"
        fi
    fi

    tar xzf "$WCSTOOLS_TARBALL"

fi

# build libwcs using make
make -C "${WCSTOOLS_DIR}/libwcs" libwcs.a

# populate the install directories
mkdir -p "${WCSTOOLS_INSTALL}"/{include,lib}
ln -s -f "../../${WCSTOOLS_DIR}/libwcs/libwcs.a" "${WCSTOOLS_INSTALL}/lib/" &&
ln -s -f "../../${WCSTOOLS_DIR}"/libwcs/{wcs,wcslib,fitshead,fitsfile}.h "${WCSTOOLS_INSTALL}/include/"
