# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = perl
VERSION = 5.14.4

BASE_URL = ftp://ftp.cpan.org/pub/CPAN/src/5.0/

# Toolchain, Stage 3 build
#
ifeq ($(BUILD_PHASE), Stage_3)
#PATCH_FILE1 = perl-5.14.2-libc-1.patch
PATCH_FILE1 = perl-5.14.4-gdbm_compat-hack.patch

# Seems stage 3 perl won't build if it's for i486`
CONFIG_OPTS = -des -Dprefix=/tools -Dcc=gcc -A ccflags="$${CFLAGS/486/586}"

CONFIGURE = yes
configure: patch
	@cd $(COMPILE_DIR); sed -i -e 's/gdbm dbm db/dbm/' Configure
	@cd $(COMPILE_DIR)/hints; sed -i -e '/$libswanted gdbm_compat/d' linux.sh
	@cd $(COMPILE_DIR); sh Configure $(CONFIG_OPTS)

COMPILE = yes
compile: configure
	make $(JOBS) -C $(COMPILE_DIR) # perl utilities ext/Errno/pm_to_blib

INSTALL = yes
install: compile
	cd $(COMPILE_DIR); \
	  cp -v perl cpan/podlators/pod2man $(TOOLS_DIR)/bin; \
	  mkdir -pv $(TOOLS_DIR)/lib/perl5/$(VERSION); \
	  cp -Rv lib/* $(TOOLS_DIR)/lib/perl5/$(VERSION)
endif


# Final build
#
ifeq ($(BUILD_PHASE),Final)
CONFIGURE = yes
configure: patch
	@(cd $(COMPILE_DIR); \
	./configure.gnu --prefix=/$(PKG_DIR) -Dpager="/bin/less -isR" -Dusethreads);
endif


include ../Makefile.rules
