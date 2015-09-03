# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libgcrypt
VERSION = 1.6.3

EXTENSION = .tar.bz2
BASE_URL = https://www.gnupg.org/ftp/gcrypt/$(PACKAGE)

CONFIG_OPTS = --prefix=$(PKG_DIR) --enable-random=linux

include ../Makefile.rules
