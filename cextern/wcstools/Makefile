#
# wcstools/Makefile
#
# download, build, and locally install the WCSTools as part of the HSTaXe build
#

# WCSTools version to build
WCSTOOLS_VERSION ?= 3.9.7

# build directory
WCSTOOLS_DIR = wcstools-$(WCSTOOLS_VERSION)
# source tarball
WCSTOOLS_TARBALL = $(WCSTOOLS_DIR).tar.gz
# source tarball URL
WCSTOOLS_URL = http://tdc-www.harvard.edu/software/wcstools/$(WCSTOOLS_TARBALL)
# archive tarball URL
WCSTOOLS_OLD_URL = http://tdc-www.harvard.edu/software/wcstools/Old/$(WCSTOOLS_TARBALL)

# library target
LIBWCS = $(WCSTOOLS_DIR)/libwcs/libwcs.a

.PHONY: all
all: $(LIBWCS)
	mkdir -p ./lib ./include
	ln -s -f ../$(LIBWCS) ./lib/
	ln -s -f ../$(WCSTOOLS_DIR)/libwcs/wcs.h ./include
	ln -s -f ../$(WCSTOOLS_DIR)/libwcs/wcslib.h ./include
	ln -s -f ../$(WCSTOOLS_DIR)/libwcs/fitshead.h ./include
	ln -s -f ../$(WCSTOOLS_DIR)/libwcs/fitsfile.h ./include

$(LIBWCS): | $(WCSTOOLS_DIR)
	$(MAKE) -C $(WCSTOOLS_DIR)/libwcs libwcs.a

$(WCSTOOLS_DIR): | $(WCSTOOLS_TARBALL)
	tar -xzf $(WCSTOOLS_TARBALL)

$(WCSTOOLS_TARBALL):
	curl -OfL $(WCSTOOLS_URL) || \
	curl -OfL $(WCSTOOLS_OLD_URL) || \
	wget $(WCSTOOLS_URL) || \
	wget $(WCSTOOLS_OLD_URL)

.PHONY: clean
clean:
	rm -rf $(WCSTOOLS_DIR) ./lib ./include
