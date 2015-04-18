# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = speedtouch
VERSION = 1.3.1

BASE_URL = http://prdownloads.sourceforge.net/speedtouch

#CONFIG_OPTS =

INSTALL = yes

install: compile
	-mkdir -p $(PKG_ROOT)/$(PKG_DIR)/bin
	@(cd $(DIR); install src/pppoa2 src/pppoa3 src/modem_run $(PKG_ROOT)/$(PKG_DIR)/bin)

include ../Makefile.rules
