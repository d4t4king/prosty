# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = klibc
VER_MM = 2.0
VERSION = $(VER_MM).1

EXTENSION = .tar.bz2

BASE_URL = http://www.kernel.org/pub/linux/libs/klibc/$(VER_MM)/

DOWNLOAD = yes
download:
	@$(DL_CMD) $(BASE_URL)/$(TARBALL)$(EXTENSION) $(MD5)

CONFIGURE = yes
configure: patch
	true

COMPILE = yes

compile: configure
	cd ../linux$(KERNEL_TYPE)/linux-$(KERNEL_VER); if [ ! -h include/asm ]; then \
	  ln -s ../arch/x86/include/asm include/asm; fi; \
	  cp arch/x86/include/generated/asm/* arch/x86/include/asm/
	cd $(DIR); \
	  make mrproper; \
	  ln -sf ../../linux$(KERNEL_TYPE)/linux-$(KERNEL_VER) linux; \
	  sed -i -e 's/^\(export HOSTCFLAGS.*\)/\1 $(CFLAGS)/' Makefile; \
	  make $(JOBS)

INSTALL = yes
install: compile
	@mkdir -p $(PKG_ROOT)
	cd $(DIR); \
	  make prefix=$(PKG_ROOT)$(PKG_DIR) install

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
	@rm -rf linux-$(KLIBKERNVER)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
