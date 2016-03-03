# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = openntpd
VERSION = 5.7p4

BASE_URL = ftp://ftp.openbsd.org/pub/OpenBSD/OpenNTPD/

PATCH_FILE1 = openntpd-username.patch

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@install -D $(COMPILE_DIR)/src/ntpd $(PKG_ROOT)$(PKG_DIR)/sbin/ntpd

include ../Makefile.rules
