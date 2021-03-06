# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = kernel-drivers

VERSION = $(KERNEL_VERSION)

export KERNEL_DIR = $(SOURCES_DIR)/linux$(KERNEL_TYPE)/linux
export DRIVER_DIR = $(SOURCES_DIR)/${PACKAGE}

IGB_VER = 5.3.3.2
IXGBE_VER = 4.1.5
E1000E_VER = 3.2.7.1
IGBVF_VER = 2.3.8.2
IXGBEVF_VER = 2.16.4
I40EVF_VER = 1.3.33
I40E_VER = 1.3.46
R8168_VER = 8.039.00
NCT6775_VER = v1.1
ASIX_88179_178A_VER = 1.14.2


PACKAGES = package-r8168 package-nct6775 package-igb package-igbvf \
	   package-ixgbe package-ixgbevf package-i40evf package-i40e \
	   package-e1000e package-asix-88179_178a
BROKEN_PKGS = package-e1000


# The download section
download:
	@$(DL_CMD) https://github.com/groeck/nct6775/archive/nct6775-$(NCT6775_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/igb-$(IGB_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/igbvf-$(IGBVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/ixgbe-$(IXGBE_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/ixgbevf-$(IXGBEVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/e1000e-$(E1000E_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/i40evf-$(I40EVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/i40e-$(I40E_VER).tar.gz
	@$(DL_CMD) http://r8168dl.appspot.com/files/r8168-$(R8168_VER).tar.bz2
	@$(DL_CMD) http://www.asix.com.tw/FrootAttach/driver/AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE.tar.gz


# The preparation section: unpack and patch
prepare: download
	tar -xvf $(DOWNLOADS_DIR)/nct6775-$(NCT6775_VER).tar.gz
	mv nct6775-nct6775-$(NCT6775_VER) nct6775-$(NCT6775_VER)
	cd nct6775-$(NCT6775_VER); patch -p1 < ../nct6775-makefile.patch
	tar -xvf $(DOWNLOADS_DIR)/r8168-$(R8168_VER).tar.bz2
	cd r8168-$(R8168_VER); patch -p1 < ../r8168-build.patch
	tar -xvf $(DOWNLOADS_DIR)/igb-$(IGB_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/igbvf-$(IGBVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/ixgbe-$(IXGBE_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/ixgbevf-$(IXGBEVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/e1000e-$(E1000E_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/i40evf-$(I40EVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/i40e-$(I40E_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE.tar.gz
	cd AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE; \
	  patch -p1 < ../ax88179-makefile.patch


# The compile section
compile-igb:
	$(MAKE) $(JOBS) V=1 -C igb-$(IGB_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-igbvf:
	$(MAKE) $(JOBS) V=1 -C igbvf-$(IGBVF_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-ixgbe:
	$(MAKE) $(JOBS) V=1 -C ixgbe-$(IXGBE_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-ixgbevf:
	$(MAKE) $(JOBS) V=1 -C ixgbevf-$(IXGBEVF_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-e1000e:
	$(MAKE) $(JOBS) V=1 -C e1000e-$(E1000E_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-i40evf:
	$(MAKE) $(JOBS) V=1 -C i40evf-$(I40EVF_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-i40e:
	$(MAKE) $(JOBS) V=1 -C i40e-$(I40E_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-r8168:
	$(MAKE) $(JOBS) V=1 -C r8168-$(R8168_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" modules

compile-nct6775:
	$(MAKE) $(JOBS) V=1 -C nct6775-$(NCT6775_VER)/ -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

compile-asix-88179_178a:
	$(MAKE) $(JOBS) V=1 -C AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4


# The package section: install in buildroot
package-igb: compile-igb
	install -D $(DRIVER_DIR)/igb-$(IGB_VER)/src/igb.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/igb/igb.ko

package-igbvf: compile-igbvf
	install -D $(DRIVER_DIR)/igbvf-$(IGBVF_VER)/src/igbvf.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/igbvf/igbvf.ko

package-ixgbe: compile-ixgbe
	install -D $(DRIVER_DIR)/ixgbe-$(IXGBE_VER)/src/ixgbe.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/ixgbe/ixgbe.ko

package-ixgbevf: compile-ixgbevf
	install -D $(DRIVER_DIR)/ixgbevf-$(IXGBEVF_VER)/src/ixgbevf.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/ixgbevf/ixgbevf.ko

package-e1000e: compile-e1000e
	install -D $(DRIVER_DIR)/e1000e-$(E1000E_VER)/src/e1000e.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/e1000e/e1000e.ko

package-i40evf: compile-i40evf
	install -D $(DRIVER_DIR)/i40evf-$(I40EVF_VER)/src/i40evf.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/i40evf/i40evf.ko

package-i40e: compile-i40e
	install -D $(DRIVER_DIR)/i40e-$(I40E_VER)/src/i40e.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/i40e/i40e.ko

package-r8168: compile-r8168
	install -D $(DRIVER_DIR)/r8168-$(R8168_VER)/src/r8168.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/realtek//r8168.ko

package-nct6775: compile-nct6775
	install -D $(DRIVER_DIR)/nct6775-$(NCT6775_VER)/nct6775.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/hwmon/nct6775.ko

package-asix-88179_178a: compile-asix-88179_178a
	install -D $(DRIVER_DIR)/AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE/ax88179_178a.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/usb/ax88179_178a.ko


# The tarball section
$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: prepare $(PACKAGES)
	@( \
	  cd $(PKG_ROOT); \
	  tar cvfz $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz .; \
	  tar xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C / \
	)

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf pulsar-$(PULSAR_VER)
	@rm -rf e1000-$(E1000_VER)
	@rm -rf igb-$(IGB_VER)
	@rm -rf igbvf-$(IGBVF_VER)
	@rm -rf ixgbe-$(IXGBE_VER)
	@rm -rf ixgbevf-$(IXGBEVF_VER)
	@rm -rf e1000e-$(E1000E_VER)
	@rm -rf i40evf-$(I40EVF_VER)
	@rm -rf i40e-$(I40E_VER)
	@rm -rf r8168-$(R8168_VER)
	@rm -rf nct6775-$(NCT6775_VER)
	@rm -rf AX88179_178A_LINUX_DRIVER_v$(ASIX_88179_178A_VER)_SOURCE
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
endif

all: $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

packageinfo.html:
	echo "<li><span style='font-size:large;'>$(PACKAGE) $(KERNEL_VER)</span><br>" >>/tmp/packageinfo.html
