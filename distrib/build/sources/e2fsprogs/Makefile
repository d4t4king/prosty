# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = e2fsprogs
VERSION = 1.42.13

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)/v$(VERSION)/

COMPILE_DIR = $(DIR)-compile


ifeq ($(BUILD_PHASE), Stage_3)

CONFIG_OPTS += --prefix=$(TOOLS_DIR) --enable-verbose-makecmds

INSTALL = yes
install: compile
	@make -C $(COMPILE_DIR) install-libs
	chmod -v u+w $(TOOLS_DIR)/lib/{libblkid,libuuid,libcom_err,libe2p,libext2fs,libss}.a

endif


ifeq ($(BUILD_PHASE), Final)

CONFIG_OPTS += --prefix="" --with-root-prefix="" --enable-elf-shlibs \
	      --enable-verbose-makecmds

PATCH = yes

patch: $(DIR)/
	sed -i 's@/bin/rm@$(TOOLS_DIR)&@' $(DIR)/lib/blkid/test_probe.in
#	sed -i -e "s/July/Jul/" $(DIR)/version.h

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install-libs
	chmod -v u+w $(PKG_ROOT)$(PKG_DIR)/lib/{libblkid,libcom_err,libe2p,libext2fs,libss,libuuid}.a
endif
	
include ../Makefile.rules
