# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = gdbm
VERSION = 1.10

BASE_URL = ftp://ftp.gnu.org/gnu/gdbm/

ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS = --prefix=/tools --enable-libgdbm-compat

CONFIGURE = yes
configure: patch
	@cd $(COMPILE_DIR); ./configure $(CONFIG_OPTS)
endif

include ../Makefile.rules
