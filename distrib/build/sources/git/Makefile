# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile.conf

PACKAGE = git
VERSION = 1.8.1.3

EXTENSION = .tar.gz

BASE_URL = http://git-core.googlecode.com/files/

CONFIG_OPTS += --with-openssl --without-curl --without-tcltk --without-python

COMPILE = yes
INSTALL = yes
CLEAN = yes

compile: configure
	make $(JOBS) -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) V=1

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(COMPILE_DIR) PREFIX=$(PKG_DIR) DESTDIR=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
