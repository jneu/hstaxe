#!/bin/bash

set \
    -o errexit \
    -o pipefail \
    -o nounset

WCSTOOLS_VERSION='3.9.7'

WCSTOOLS_DIR="wcstools-${WCSTOOLS_VERSION}"
WCSTOOLS_TARBALL="${WCSTOOLS_DIR}.tar.gz"
WCSTOOLS_URL="http://tdc-www.harvard.edu/software/wcstools/${WCSTOOLS_TARBALL}"
WCSTOOLS_INSTALL="wcstools-install"

test -e "$WCSTOOLS_TARBALL" ||
    curl -OL "$WCSTOOLS_URL"

test -d "$WCSTOOLS_DIR" ||
    tar xzf "$WCSTOOLS_TARBALL"

test -e "${WCSTOOLS_DIR}/libwcs/libwcs.a" ||
    (
        cd "${WCSTOOLS_DIR}/libwcs" &&
        make libwcs.a
    )

mkdir -p "${WCSTOOLS_INSTALL}"/{include,lib}

test -e "${WCSTOOLS_INSTALL}/lib/libwcs.h" ||
    (
        cp "${WCSTOOLS_DIR}/libwcs/libwcs.a" "${WCSTOOLS_INSTALL}/lib/" &&
        cp "${WCSTOOLS_DIR}"/libwcs/{wcs,wcslib,fitshead,fitsfile}.h "${WCSTOOLS_INSTALL}/include/"
    )
