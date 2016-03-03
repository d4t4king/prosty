# prosty
Smoothwall....off the wall.......simple.
=======

![Travis-CI Build Status Image](https://travis-ci.org/d4t4king/off-the-wall.svg?branch=master)

Newly added:
* 2015-10-29
	* Added sysstat executables.  Will probably (at least) add a drontab interface to show audit data captured by these tools.  May morph into RRD graphs, and/or an extension of the pgraphs mod.
	* New Perl Modules
		* MIME::Types
		* MailTools
		* Email::Date::Format
		* MIME::Lite

* 2015-10-02
	* Wireshark without the UI:
		* This is primarily to test a feature that may turn into something more.  I had this idea about capturing packets on both the RED+GREEN interfaces, and them merging them into one pcap file for analysis.  This is easiler facilitated using tshark (the commandline wireshark utility) and related tools (specifically `mergecap`).
* Previous
	* AIDE (and supporting libs) (Config is still WIP!)
		* libgpg-error
		* libgcrypt
		* libskba
		* libassuan
	* cracklib (Config WIP!)
	* linux-pam (Config WIP!)
	* ruby -- I find myself scripting with it more and more, it'd just be really handy to have it on SWE.
	* iptraf-ng
	* curl
	* htop
	* Perl Modules
		* Bit::Vector
		* Carp::Clan
		* Digest::HMAC
		* Geo::IP::PurePerl
		* Net::DNS
		* Net::IPv4Addr
		* Net::Nslookup
		* Sub::Uplevel
		* Test::Exception
	
	\* no real reason to keep tracking perl mods that are already included in SWE!

	Version bumps:
	* ntp -> 4.2.8p2
	* glibc -> 2.21
	* httpd -> 2.2.29

	Configuratin changes:
	* Added security HTTP headers to httpd.conf
	* Added `encode_entities` to header.pm
	* Tweaked SSL configuration based on pull request.  (This requires further attention.)
	* git now works with libcurl to allow for git communications over http/s
	NOTE: That git doesn't know where to access the certificate information in smoothwall, so you must tell it (`/usr/lib/ssl/certs/ca-certificates.crt`) or disable `sslVerify` in your git config.
	* advstatus.cgi now has friendlier, human readable memory stats.

	Other:
	* gdbm is now built in Stage 3 prior to perl, since building perl on Gentoo /demanded/ gdbm.  It wouldn't seem to accept any attempts to make it ignore gdbm.
	* Also incorporated some changes that help to tidy up the UI.
	* Most of the UI pages are now "strict-ified".  If you don't know what that means, accept it as "cleaner code".
	
Hoping to add Travis CI build badges.
