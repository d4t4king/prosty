# Smoothwall Build System
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.
#
# Written by: Charlie Heselton
#
# Makefile for all needed perl modules
#

include ../Makefile.conf

PACKAGE = perl-mods
VERSION = 0.1

# List of all mods to be built. Add here, then add dir and makefile in
#   version dir below. IO-Socket-SSL seems to depend on Net-SSLeay; both
#   are moved to the end of the list.
export PERL_MODS = \
	    App-Control \
	    Authen-NTLM \
	    Authen-SASL \
		Bit-Vector \
		Carp-Clan \
	    Config-Patch \
		Digest-HMAC \
		Sub-Uplevel \
		Test-Exception \
	    Date-Calc \
	    GD \
	    GDTextUtil \
	    GDGraph \
		Geo-IP-PurePerl \
	    HTML-Parser \
	    HTML-Tagset \
	    Log-Log4perl \
	    Net-CIDR \
		Net-DNS \
		Net-IPv4Addr \
	    Net-Netmask \
		Net-Nslookup \
	    NetAddr-IP \
	    RRD-Simple \
	    Set-IntSpan \
	    URI \
	    libnet \
	    libwww-perl \
	    local-lib \
	    Net-SSLeay \
		DBD-SQLite \
	    IO-Socket-SSL

DOWNLOAD = yes
download:
	@+$(MAKE) -C $(PACKAGE)-$(VERSION) download

COMPILE = yes
compile: download
	@+$(MAKE) $(JOBS) -C $(COMPILE_DIR)

INSTALL = yes
install: compile
	@true

CLEAN = yes
clean:
	@echo -n " $(PACKAGE)"
	@+$(MAKE) --no-print-directory -C $(COMPILE_DIR) clean >/dev/null 2>&1
	@rm -rf $(PKG_ROOT)
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz

include ../Makefile.rules
