off-the-wall
============
Smoothwall Express 3.1.....plus some.

Added so far:
* iptraf-ng
* curl
* htop
* Perl Modules
	* App::Control *
	* Authen::NTLM *
	* Authen::SASL *
	* Bit::Vector
	* Carp::Clan
	* Config::Patch *
	* Date::Calc *
	* Digest::HMAC
	* GD *
	* GDGraph *
	* GDTextUtil *
	* Geo::IP::PurePerl
	* HTML-Parser *
	* HTML-Tagset *
	* IO-Socket-SSL *
	* libnet *
	* libwww-perl *
	* local-lib *
	* Log::Log4perl *
	* NetAddr::IP *
	* Net::CIDR *
	* Net::DNS
	* Net::IPv4Addr
	* Net::Netmask *
	* Net::Nslookup
	* Net::SSLeay *
	* RRD::Simple *
	* Set::IntSpan *
	* Sub::Uplevel
	* Test::Exception
	* URI *

\* Included in SWE3.1u3

Version bumps:
* ntp -> 4.2.8p2
* glibc -> 2.21

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

