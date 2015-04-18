# Copyright 2004-2010 SmoothWall Ltd

include ../Makefile
include ../Makefile.conf
include ../Makefile.versions

PACKAGE = kernel-drivers

VERSION = $(KERNEL_VERSION)

export KERNEL_DIR = $(SOURCES_DIR)/linux$(KERNEL_TYPE)/linux
export DRIVER_DIR = $(SOURCES_DIR)/${PACKAGE}

#PULSAR_VER = 4.0.24
#TG3_VER = 3.92n
#BNX2_VER = 1.5.10c
#E1000_VER = 8.0.35
IGB_VER = 5.2.9.4
IXGBE_VER = 3.22.3
E1000E_VER = 3.1.0.2
IGBVF_VER = 2.3.5
IXGBEVF_VER = 2.15.3
I40EVF_VER = 1.0.5
I40E_VER = 1.0.15
R8168_VER = 8.038.00

PACKAGES = package-igb package-igbvf package-ixgbe package-ixgbevf package-e1000e package-i40evf package-i40e
BROKEN_PKGS = package-e1000

#ifeq ($(mARCH), $(ARCH32))
#PACKAGES += package-pulsar
#endif

#ifeq ($(mARCH), $(ARCH64))
#export CFLAGS =
#endif

download:
#	$(DL_CMD) http://heanet.dl.sourceforge.net/sourceforge/openadsl/pulsar-$(PULSAR_VER).tar.gz
#	$(DL_CMD) http://sotonfs/tg3-$(TG3_VER).tar.gz
#	$(DL_CMD) http://sotonfs/bnx2-$(BNX2_VER).tar.gz
#	$(DL_CMD) http://kent.dl.sourceforge.net/sourceforge/e1000/e1000-$(E1000_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/igb-$(IGB_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/igbvf-$(IGBVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/ixgbe-$(IXGBE_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/ixgbevf-$(IXGBEVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/e1000e-$(E1000E_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/i40evf-$(I40EVF_VER).tar.gz
	@$(DL_CMD) http://dfn.dl.sourceforge.net/sourceforge/e1000/i40e-$(I40E_VER).tar.gz
	@$(DL_CMD) http://r8168dl.appspot.com/files/r8168-$(R8168_VER).tar.bz2

prepare: download
#	tar -xvf $(DOWNLOADS_DIR)/pulsar-$(PULSAR_VER).tar.gz
#	tar -xvf $(DOWNLOADS_DIR)/tg3-$(TG3_VER).tar.gz
#	tar -xvf $(DOWNLOADS_DIR)/bnx2-$(BNX2_VER).tar.gz
#	tar -xvf $(DOWNLOADS_DIR)/e1000-$(E1000_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/igb-$(IGB_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/igbvf-$(IGBVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/ixgbe-$(IXGBE_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/ixgbevf-$(IXGBEVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/e1000e-$(E1000E_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/i40evf-$(I40EVF_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/i40e-$(I40E_VER).tar.gz
	tar -xvf $(DOWNLOADS_DIR)/r8168-$(R8168_VER).tar.bz2

#compile-pulsar:
#	$(MAKE) $(JOBS) V=1 -C pulsar-$(PULSAR_VER) KDIR=$(KERNEL_DIR)

#compile-e1000:
#	$(MAKE) $(JOBS) V=1 -C e1000-$(E1000_VER)/src -j $(PARA_JOBS) CFLAGS="$(CFLAGS)" KSRC=$(KERNEL_DIR) K_VERSION=3.4

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


#package-pulsar: compile-pulsar
#	install -D $(DRIVER_DIR)/pulsar-$(PULSAR_VER)/pulsar_atm.ko \
		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/misc/pulsar_atm.ko

#package-tg3: compile-tg3
#	install -D $(DRIVER_DIR)/tg3-$(TG3_VER)/tg3.ko \
#		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/tg3.ko

#package-bnx2: compile-bnx2
#	install -D $(DRIVER_DIR)/bnx2-$(BNX2_VER)/src/bnx2.ko \
#		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/bnx2.ko

#package-e1000: compile-e1000
#	install -D $(DRIVER_DIR)/e1000-$(E1000_VER)/src/e1000.ko \
#		$(PKG_ROOT)/lib/modules/$(K_SWE_VERSION)/kernel/drivers/net/ethernet/intel/e1000/e1000.ko

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

$(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz: prepare $(PACKAGES)
	@( \
	  cd $(PKG_ROOT); \
	  tar cvfz $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz .; \
	  tar xvf $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz -C / \
	)

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf pulsar-$(PULSAR_VER)
#	@rm -rf tg3-$(TG3_VER)
#	@rm -rf bnx2-$(BNX2_VER)
	@rm -rf e1000-$(E1000_VER)
	@rm -rf igb-$(IGB_VER)
	@rm -rf igbvf-$(IGBVF_VER)
	@rm -rf ixgbe-$(IXGBE_VER)
	@rm -rf ixgbevf-$(IXGBEVF_VER)
	@rm -rf e1000e-$(E1000E_VER)
	@rm -rf i40evf-$(I40EVF_VER)
	@rm -rf i40e-$(I40E_VER)
	@rm -rf r8168-$(R8168_VER)
	@rm -rf $(PKG_ROOT)

all: $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

packageinfo.html:
	echo "<li><span style='font-size:large;'>$(PACKAGE) $(KERNEL_VER)</span><br>" >>/tmp/packageinfo.html
#	echo "Pulsar ADSL download: <a href='http://heanet.dl.sourceforge.net/sourceforge/openadsl/pulsar-$(PULSAR_VER).tar.gz'>http://heanet.dl.sourceforge.net/sourceforge/openadsl/pulsar-$(PULSAR_VER).tar.gz</a><br> " >> /tmp/packageinfo.html
#	cp -avR $(DOWNLOADS_DIR)/tg3-$(TG3_VER).tar.gz /tmp/downloads
#	echo "TG3 local mirror: <a href='downloads/tg3-$(TG3_VER).tar.gz'>tg3-$(TG3_VER).tar.gz</a><br> " >>/tmp/packageinfo.html
#	cp -avR $(DOWNLOADS_DIR)/bnx2-$(BNX2_VER).tar.gz /tmp/downloads
#	echo "BNX2 local mirror: <a href='downloads/bnx2-$(BNX2_VER).tar.gz'>bnx2-$(BNX2_VER).tar.gz</a><br> " >> /tmp/packageinfo.html
	echo "E1000 download: <a href='http://kent.dl.sourceforge.net/sourceforge/e1000/e1000-$(E1000_VER).tar.gz'>http://kent.dl.sourceforge.net/sourceforge/e1000/e1000-$(E1000_VER).tar.gz</a><br> " >> /tmp/packageinfo.html
	
#	echo "Patches:<br>" >>/tmp/packageinfo.html
#	echo "<ul>" >>/tmp/packageinfo.html
#	(for PATCH in linux-2.6.16-imq2.diff route_fwmark_mask.patch patch-2.6.16-nath323-1.3 openswan-procpermsfix.diff strongswan-interfaces.diff unicorn.patch eagle-2.6-fix.patch eagle-stats.patch patch-o-matic-mod-addition.patch; do \
#		echo "<li><a href='downloads/$$PATCH'>$$PATCH</a><br>" >>/tmp/packageinfo.html; \
#		cp -avR ../kernel-patches/$$PATCH /tmp/downloads; \
#	done) 
#	echo "</ul>" >>/tmp/packageinfo.html
