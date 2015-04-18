# Copyright Neal P. Murphy
# Licensed under Smoothwall Express' GPLv2

include ../Makefile.conf

PACKAGE = setkerneltz
VERSION = 0.0

DOWNLOAD = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

download:
	@true

compile:
	make -C $(DIR)

install: compile
	@mkdir -p $(PKG_ROOT)/usr/bin/smoothwall
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -f $(DIR)/$(PACKAGE)
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

include ../Makefile.rules
