# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cacert-bundle
VERSION = 0.0

DOWNLOAD = yes
INSTALL = yes
CLEAN = yes

download:
	@true

install:
	@mkdir -p $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs
	@./mk-ca-bundle.pl $(PKG_ROOT)/$(PKG_DIR)/lib/ssl/certs/ca-certificates.crt
	@rm -f certdata.txt

clean:
	@echo -n " $(PACKAGE)"
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
