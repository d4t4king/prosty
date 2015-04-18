# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = apcupsd
VERSION = 3.14.13

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)%20-%20Stable/$(VERSION)

CONFIG_OPTS = --enable-modbus-usb --enable-usb --with-generic-usb --with-pid-dir=/var/run

PRE_COMPILE = VERBOSE=1

include ../Makefile.rules
