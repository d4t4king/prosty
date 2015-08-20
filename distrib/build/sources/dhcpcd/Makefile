# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = dhcpcd
VERSION =  6.9.1
EXTENSION = .tar.bz2

BASE_URL = http://roy.marples.name/downloads/dhcpcd/

TARBALL = $(PACKAGE)-$(VERSION)
EXTENSION = .tar.xz

DIR =  $(PACKAGE)-$(VERSION)

CONFIG_OPTS += --mandir=$(PKG_DIR)/man


INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/sbin

include ../Makefile.rules
