#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# Time Zone conversion script borrowed from perlmonks.org
#
use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

use Time::Local;

my %dhcpsettings;
my %netsettings;
my $dhcptmpfile = "${swroot}/dhcp/leasesconfig";
my $display_dhcplease = 'yes';
my $subnet;

&showhttpheaders();

$netsettings{'GREEN_DRIVER'} = '';
$netsettings{'GREEN_ADDRESS'} = '';
$netsettings{'GREEN_NETADDRESS'} = '';
$netsettings{'GREEN_NETMASK'} = '';

$netsettings{'PURPLE_DRIVER'} = '';
$netsettings{'PURPLE_ADDRESS'} = '';
$netsettings{'PURPLE_NETADDRESS'} = '';
$netsettings{'PURPLE_NETMASK'} = '';

&readhash("${swroot}/ethernet/settings", \%netsettings);

$dhcpsettings{'ACTION'} = '';
$dhcpsettings{'VALID'} = '';

$dhcpsettings{'ENABLE'} = 'off';
$dhcpsettings{'START_ADDR'} = '';
$dhcpsettings{'END_ADDR'} = '';
$dhcpsettings{'DNS1'} = '';
$dhcpsettings{'DNS2'} = '';
$dhcpsettings{'DOMAIN_NAME'} = '';
$dhcpsettings{'DEFAULT_LEASE_TIME'} = '';
$dhcpsettings{'MAX_LEASE_TIME'} = '';

$dhcpsettings{'NIS_ENABLE'} = 'off';
$dhcpsettings{'BOOT_SERVER'} = '';
$dhcpsettings{'BOOT_FILE'} = '';
$dhcpsettings{'BOOT_ROOT'} = '';
$dhcpsettings{'BOOT_ENABLE'} = 'off';

$dhcpsettings{'COLUMN_ONE'} = 1;
$dhcpsettings{'ORDER_ONE'} = $tr{'log ascending'};
$dhcpsettings{'COLUMN_TWO'} = 2;
$dhcpsettings{'ORDER_TWO'} = $tr{'log descending'};

&getcgihash(\%dhcpsettings);

if ($ENV{'QUERY_STRING'} && ( not defined $dhcpsettings{'ACTION'} or $dhcpsettings{'ACTION'} eq "" ))
{
	my @temp = split(',',$ENV{'QUERY_STRING'});
  	$subnet = $temp[4] if ( defined $temp[ 4 ] and $temp[ 4 ] ne "" );
  	$dhcpsettings{'SUBNET'}  = $subnet;
  	$dhcpsettings{'ORDER_TWO'}  = $temp[3] if ( defined $temp[ 3 ] and $temp[ 3 ] ne "" );
  	$dhcpsettings{'COLUMN_TWO'} = $temp[2] if ( defined $temp[ 2 ] and $temp[ 2 ] ne "" );
  	$dhcpsettings{'ORDER_ONE'}  = $temp[1] if ( defined $temp[ 1 ] and $temp[ 1 ] ne "" );
	$dhcpsettings{'COLUMN_ONE'} = $temp[0] if ( defined $temp[ 0 ] and $temp[ 0 ] ne "" );
}

my $errormessage = '';
if ($dhcpsettings{'ACTION'} eq $tr{'save'})
{
	unless ($dhcpsettings{'NIS_DOMAIN'} eq "" or $dhcpsettings{'NIS_DOMAIN'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/) {
		$errormessage .= $tr{'invalid domain name'} ."<br />\n";
	}

	if ($dhcpsettings{'SUBNET'} ne 'green' && $dhcpsettings{'SUBNET'} ne 'purple')
	{
		$errormessage .= $tr{'invalid input'} ."<br />\n";
	}
	if ($dhcpsettings{'SUBNET'} ne $dhcpsettings{'CHECKSUBNET'})
	{
		$errormessage .= 'Cannot save without selecting first.' ."<br />\n";
	}
	if (!(&validip($dhcpsettings{'START_ADDR'})))
	{
		$errormessage .= $tr{'invalid start address'} ."<br />\n";
	}
	if (!(&validip($dhcpsettings{'END_ADDR'})))
	{
		$errormessage .= $tr{'invalid end address'} ."<br />\n";
	}
	if (!(&ip2number($dhcpsettings{'END_ADDR'}) > &ip2number($dhcpsettings{'START_ADDR'})))
	{
		$errormessage .= $tr{'end must be greater than start'} ."<br />\n";
	}
	open(FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	my $line;
	foreach $line (@current)
	{
		chomp($line);
		my @temp = split(/\,/,$line);
		if ($temp[5] eq 'on')
		{
			unless(!((&ip2number($temp[2]) <= &ip2number($dhcpsettings{'END_ADDR'}) 
				&& (&ip2number($temp[2]) >= &ip2number($dhcpsettings{'START_ADDR'}))))) {
				$errormessage .= $tr{'dynamic range cannot overlap static'} ."<br />\n";
			}
		}
	}
	if ($dhcpsettings{'DNS1'})
	{
		if (!(&validip($dhcpsettings{'DNS1'}))) {
			$errormessage .= $tr{'invalid primary dns'} ."<br />\n";
		}
	}
	if (!($dhcpsettings{'DNS1'}) && $dhcpsettings{'DNS2'})
	{
		$errormessage .= $tr{'cannot specify secondary dns without specifying primary'} ."<br />\n";
	}
	if ($dhcpsettings{'DNS2'})
	{
		if (!(&validip($dhcpsettings{'DNS2'}))) {
			$errormessage .= $tr{'invalid secondary dns'} ."<br />\n";
		}
	}
	if ($dhcpsettings{'NTP1'})
	{
		if (!(&validip($dhcpsettings{'NTP1'}))) {
			$errormessage .= $tr{'invalid primary ntp'} ."<br />\n";
		}
	}
	if (!($dhcpsettings{'NTP1'}) && $dhcpsettings{'NTP2'})
	{
		$errormessage .= $tr{'cannot specify secondary ntp without specifying primary'} ."<br />\n";
	}
	if ($dhcpsettings{'NTP2'})
	{
		if (!(&validip($dhcpsettings{'NTP2'}))) {
			$errormessage .= $tr{'invalid secondary ntp'} ."<br />\n";
		}
	}
	if (!($dhcpsettings{'WINS1'}) && $dhcpsettings{'WINS2'})
	{
		$errormessage .= $tr{'cannot specify secondary wins without specifying primary'} ."<br />\n"; 
	}
	if ($dhcpsettings{'WINS1'})
	{
		if (!(&validip($dhcpsettings{'WINS1'})))
		{
			$errormessage .= $tr{'invalid primary wins'} ."<br />\n";
		}
	}
	if ($dhcpsettings{'WINS2'})
	{
		if (!(&validip($dhcpsettings{'WINS2'})))
		{
			$errormessage .= $tr{'invalid secondary wins'} ."<br />\n";
		}
	}
	if (!($dhcpsettings{'DNS1'}) && $dhcpsettings{'DNS2'}) {
		$errormessage .= $tr{'cannot specify secondary dns without specifying primary'} ."<br />\n"; 
	}
	if (!($dhcpsettings{'NIS_DOMAIN'}) && $dhcpsettings{'NIS1'}) {
		$errormessage .= $tr{'cannot specify nis server without specifying nis domain'} ."<br />\n";
	}
	if (!($dhcpsettings{'NIS1'}) && $dhcpsettings{'NIS2'}) {
		$errormessage .= $tr{'cannot specify secondary nis without specifying primary'} ."<br />\n";
	}
	if ($dhcpsettings{'NIS1'})
	{
		if (!(&validip($dhcpsettings{'NIS1'}))) {
			$errormessage .= $tr{'invalid primary nis'} ."<br />\n";
		}
	}
	if ($dhcpsettings{'NIS2'})
	{
		if (!(&validip($dhcpsettings{'NIS2'}))) {
			$errormessage .= $tr{'invalid secondary nis'} ."<br />\n";
		}
	}
	unless (!$dhcpsettings{'DOMAIN_NAME'} || $dhcpsettings{'DOMAIN_NAME'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/) {
		$errormessage .= $tr{'invalid domain name'} ."<br />\n";
	}
	if (!($dhcpsettings{'DEFAULT_LEASE_TIME'} =~ /^\d+$/))
	{
		$errormessage .= $tr{'invalid default lease time'} ."<br />\n";
	}
	if (!($dhcpsettings{'MAX_LEASE_TIME'} =~ /^\d+$/))
	{
		$errormessage .= $tr{'invalid max lease time'} ."<br />\n";
	}
#	if ($dhcpsettings{'BOOT_SERVER'} ne "" and
#	    !(validip($dhcpsettings{'BOOT_SERVER'}) or
#	      validhostname($dhcpsettings{'BOOT_SERVER'})))
#	{
#		$errormessage .= "FIX_TR bad boot server name/IP". $tr{'invalid boot_server_ip_or_name'} ."<br />\n";
#	}
#	if ($dhcpsettings{'BOOT_ROOT'} ne "" and $dhcpsettings{'BOOT_ROOT'} !~ m=[^<>'"]*=)
#	{
#		$errormessage .= "FIX_TR bad boot root path". $tr{'invalid boot_root_path'} ."<br />\n";
#	}
#	if ($dhcpsettings{'BOOT_FILE'} ne "" and ! ($dhcpsettings{'BOOT_FILE'} =~ m=[^/<>'"]*=))
#	{
#		$errormessage .= "FIX_TR bad boot file name". $tr{'invalid boot_file_name'} ."<br />\n";
#	}
	
ERROR:
	if ($errormessage) {
		$dhcpsettings{'VALID'} = 'no'; }
	else {
		$dhcpsettings{'VALID'} = 'yes'; }
		
	if ($dhcpsettings{'VALID'} eq 'yes')
	{
		my %tempsettings;
	
		$tempsettings{'BOOT_ENABLE'} = $dhcpsettings{'BOOT_ENABLE'};
		$tempsettings{'BOOT_SERVER'} = $dhcpsettings{'BOOT_SERVER'};
		$tempsettings{'BOOT_FILE'} = $dhcpsettings{'BOOT_FILE'};
		$tempsettings{'BOOT_ROOT'} = $dhcpsettings{'BOOT_ROOT'};
	
		&writehash("${swroot}/dhcp/global", \%tempsettings);
	
		delete $dhcpsettings{'STATIC_DESC'};
		delete $dhcpsettings{'STATIC_MAC'};
		delete $dhcpsettings{'STATIC_IP'};
		delete $dhcpsettings{'DEFAULT_ENABLE_STATIC'};
	
		&writehash("${swroot}/dhcp/settings-$dhcpsettings{'SUBNET'}", \%dhcpsettings);

		system('/usr/bin/smoothwall/writedhcp.pl');

		unlink "${swroot}/dhcp/uptodate";
	
		my $success = message('dhcpdrestart');
		
		if (not defined $success) {
			$errormessage .= "DHCPD Restart:". $tr{'smoothd failure'} ."<br />\n"; 
		}

		system('/usr/bin/smoothwall/writehosts.pl');

		my $success = message('dnsproxyhup');
		if (not defined $success)
		{
			$errormessage .= "DNSProxy SIGHUP:". $tr{'smoothd failure'} ."<br />\n";
		}
	}
}

if ($dhcpsettings{'ACTION'} eq $tr{'add'})
{
	# Munge the MAC into something good.
	my $mac = $dhcpsettings{'STATIC_MAC'};
	$mac =~ s/[^0-9a-f]//ig;
	$mac = uc($mac);
	$mac =~ /^(..)(..)(..)(..)(..)(..)$/;
	$mac = "$1:$2:$3:$4:$5:$6";
	if (&validmac($mac)) {
		$dhcpsettings{'STATIC_MAC'} = $mac; }

	unless($dhcpsettings{'STATIC_HOST'}) { $errormessage .= $tr{'please enter a host name'} ."<br />\n"; }
	unless($dhcpsettings{'STATIC_HOST'} =~ /^([a-zA-Z])+([\.a-zA-Z0-9_-])+$/) { $errormessage .= $tr{'invalid host name'} ."<br />\n"; }
	unless(&validmac($dhcpsettings{'STATIC_MAC'})) { $errormessage .= $tr{'mac address not valid'} ."<br />\n"; }
	unless(&validip($dhcpsettings{'STATIC_IP'})) { $errormessage .= $tr{'ip address not valid'} ."<br />\n"; }
	if ($dhcpsettings{'DEFAULT_ENABLE_STATIC'} eq 'on')
	{
		unless(!((&ip2number($dhcpsettings{'STATIC_IP'}) <= &ip2number($dhcpsettings{'END_ADDR'}) 
			&& (&ip2number($dhcpsettings{'STATIC_IP'}) >= &ip2number($dhcpsettings{'START_ADDR'}))))) {
			$errormessage .= $tr{'static must be outside dynamic range'} ."<br />\n";
		}
	}
	open(FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	my $line;
	foreach $line (@current)
	{
		chomp($line);
		my @temp = split(/\,/,$line);
		if ($dhcpsettings{'DEFAULT_ENABLE_STATIC'} eq 'on')
		{
			if (($dhcpsettings{'STATIC_HOST'} eq $temp[0]) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'hostnamec'} $temp[0] $tr{'already exists and has assigned ip'} $tr{'ip address'} $temp[2].<br />\n";
			}
			if (($dhcpsettings{'STATIC_MAC'} eq $temp[1]) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'mac address'} $temp[1] ($tr{'hostnamec'} $temp[0]) $tr{'already assigned to ip'} $tr{'ip address'} $temp[2].<br />\n";
			}
			if (($dhcpsettings{'STATIC_IP'} eq $temp[2]) && ($temp[4] eq 'on')) {
				$errormessage .= "$tr{'ip address'} $temp[2] $tr{'ip already assigned to'} $tr{'mac address'} $temp[1] ($tr{'hostnamec'} $temp[0]).<br />\n";
			}
		}
	}
	unless($dhcpsettings{'STATIC_DESC'} =~ /^([a-zA-Z 0-9]*)$/) { $errormessage .= $tr{'description contains bad characters'} ."<br />\n"; }
	unless(&validmac($dhcpsettings{'STATIC_MAC'})) { $errormessage .= $tr{'mac address not valid'} ."<br />\n"; }
	unless(&validip($dhcpsettings{'STATIC_IP'})) { $errormessage .= $tr{'ip address not valid'} ."<br />\n"; }
	unless ($errormessage)
	{
		open(FILE, ">>${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$dhcpsettings{'STATIC_HOST'},$dhcpsettings{'STATIC_MAC'},$dhcpsettings{'STATIC_IP'},$dhcpsettings{'STATIC_DESC'},$dhcpsettings{'DEFAULT_ENABLE_STATIC'}\n";
		close(FILE);
		delete $dhcpsettings{'STATIC_HOST'};		
		delete $dhcpsettings{'STATIC_MAC'};
		delete $dhcpsettings{'STATIC_IP'};
		delete $dhcpsettings{'STATIC_DESC'};
		delete $dhcpsettings{'DEFAULT_ENABLE_STATIC'};
		system ('/bin/touch', "${swroot}/dhcp/uptodate");
	}
}

if ($dhcpsettings{'ACTION'} eq $tr{'remove'} || $dhcpsettings{'ACTION'} eq $tr{'edit'})
{
	open(FILE, "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current)
	{
		$id++;
		if ($dhcpsettings{$id} eq "on") {
			$count++; }
	}
	if ($count == 0) {
		$errormessage .= $tr{'nothing selected'} ."<br />\n"; }
	if ($count > 1 && $dhcpsettings{'ACTION'} eq $tr{'edit'}) {
		$errormessage .= $tr{'you can only select one item to edit'} ."<br />\n"; }
	unless ($errormessage)
	{
		open(FILE, ">${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}") or die 'Unable to open config file.';
		flock FILE, 2;
 		$id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($dhcpsettings{$id} eq "on") {
				print FILE "$line"; }
			elsif ($dhcpsettings{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$dhcpsettings{'STATIC_HOST'} = $temp[0];
				$dhcpsettings{'STATIC_MAC'} = $temp[1];
				$dhcpsettings{'STATIC_IP'} = $temp[2];
				$dhcpsettings{'STATIC_DESC'} = $temp[3];
				$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = $temp[4];
			}
		}
		close(FILE);
		system ('/bin/touch', "${swroot}/dhcp/uptodate");
	}
}

if ($dhcpsettings{'ACTION'} eq '' || $dhcpsettings{'ACTION'} eq $tr{'select'})
{
	my $c = $dhcpsettings{'COLUMN_ONE'};
	my $o = $dhcpsettings{'ORDER_ONE'};
	my $d = $dhcpsettings{'COLUMN_TWO'};
	my $p = $dhcpsettings{'ORDER_TWO'};

	if ($dhcpsettings{'ACTION'} eq '') {
		if ($subnet eq '') {
			$subnet = "green";
		}
	}
	else {
		$subnet = $dhcpsettings{'SUBNET'};
	}

	undef %dhcpsettings;

 	$dhcpsettings{'ENABLE'} = 'off';
	$dhcpsettings{'DEFAULT_LEASE_TIME'} = '60';
	$dhcpsettings{'MAX_LEASE_TIME'} = '120';
	$dhcpsettings{'DEFAULT_ENABLE_STATIC'} = 'on';

	$dhcpsettings{'COLUMN_ONE'} = $c;
	$dhcpsettings{'ORDER_ONE'} = $o;
	$dhcpsettings{'COLUMN_TWO'} = $d;
	$dhcpsettings{'ORDER_TWO'} = $p;

	&readhash("${swroot}/dhcp/global", \%dhcpsettings);
	&readhash("${swroot}/dhcp/settings-$subnet", \%dhcpsettings);
	$dhcpsettings{'SUBNET'} = $subnet;
}

if ($display_dhcplease eq 'yes')
{
  &dhcp_lease_table
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$dhcpsettings{'ENABLE'}} = 'CHECKED';
$checked{'NIS_ENABLE'}{'on'} = '';
$checked{'NIS_ENABLE'}{'off'} = '';
$checked{'NIS_ENABLE'}{$dhcpsettings{'NIS_ENABLE'}} = 'CHECKED';
$checked{'BOOT_ENABLE'}{'on'} = '';
$checked{'BOOT_ENABLE'}{'off'} = '';
$checked{'BOOT_ENABLE'}{$dhcpsettings{'BOOT_ENABLE'}} = 'CHECKED';
$checked{'DEFAULT_ENABLE_STATIC'}{'on'} = '';
$checked{'DEFAULT_ENABLE_STATIC'}{'off'} = '';
$checked{'DEFAULT_ENABLE_STATIC'}{$dhcpsettings{'DEFAULT_ENABLE_STATIC'}} = 'CHECKED';

$selected{'SUBNET'}{'green'} = '';
$selected{'SUBNET'}{'purple'} = '';
$selected{'SUBNET'}{$dhcpsettings{'SUBNET'}} = 'SELECTED';

&openpage($tr{'dhcp configuration'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print <<END
<form method='post'>

<INPUT TYPE='hidden' NAME='CHECKSUBNET' VALUE='$dhcpsettings{'SUBNET'}'>
END
;
if (-e "${swroot}/dhcp/uptodate") {
	&openbox($tr{'note'});
	print "<FONT CLASS='base'>$tr{'there are unsaved changes'}<FONT>\n";
	print <<END;
<table class='centered'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
	&closebox();
}

&openbox('Global settings:');
print <<END
<table class='centered'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'network boot enabledc'}</td>
	<td style='width: 25%;'><input type='checkbox' name='BOOT_ENABLE' $checked{'BOOT_ENABLE'}{'on'}></td>
	<td style='width: 25%;'></td>
	<td style='width: 25%;'></td>
</tr>
<tr>
	<td class='base'>$tr{'boot serverc'}</TD>
	<td><input type='text' name='BOOT_SERVER' value='$dhcpsettings{'BOOT_SERVER'}'></td>
	<td class='base'>$tr{'boot filenamec'}</td>
	<td><input type='text' name='BOOT_FILE' value='$dhcpsettings{'BOOT_FILE'}'></td>
</tr>
<tr>
	<td class='base'>$tr{'root pathc'}</TD>
	<td colspan='3'><input type='text' name='BOOT_ROOT' size='32' value='$dhcpsettings{'BOOT_ROOT'}'></td>
</tr>
</table>
END
;

&closebox();

&openbox('Interface:');
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%'>
	<SELECT NAME='SUBNET'>
	<OPTION VALUE='green' $selected{'SUBNET'}{'green'}>GREEN
END
;
if ($netsettings{'PURPLE_DEV'}) {
	print "\t<OPTION VALUE='purple' $selected{'SUBNET'}{'purple'}>PURPLE\n"; }

print <<END
	</SELECT>
	</TD>
	<TD WIDTH='10%'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'select'}'></TD>
	<TD WIDTH='65%'>&nbsp;</TD>
</TR>
</TABLE>
END
;

&closebox();

&openbox('DHCP:');

print <<END
<table class='centered'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'start address'}</td>
	<td style='width: 25%;'><input type='text' name='START_ADDR' value='$dhcpsettings{'START_ADDR'}' id='start_addr' @{[jsvalidip('start_addr')]} ></td>
	<td class='base' style='width: 25%;'>$tr{'end address'}</td>
	<td style='width: 25%;'><input type='text' name='END_ADDR' value='$dhcpsettings{'END_ADDR'}' id='end_addr' @{[jsvalidip('end_addr')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary dns'}</td>
	<td><input type='text' name='DNS1' value='$dhcpsettings{'DNS1'}' id='dns1' @{[jsvalidip('dns1','true')]} ></td>
	<td class='base'>$tr{'secondary dns'}</TD>
	<td><input type='text' name='DNS2' value='$dhcpsettings{'DNS2'}' id='dns2' @{[jsvalidip('dns2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary ntp'}</td>
	<td><input type='text' name='NTP1' value='$dhcpsettings{'NTP1'}' id='ntp1' @{[jsvalidip('ntp1','true')]} ></td>
	<td class='base'>$tr{'secondary ntp'}</TD>
	<td><input type='text' name='NTP2' value='$dhcpsettings{'NTP2'}' id='ntp2' @{[jsvalidip('ntp2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary wins'}</td>
	<td><input type='text' name='WINS1' value='$dhcpsettings{'WINS1'}' id='wins1' @{[jsvalidip('wins1','true')]} ></td>
	<td class='base'>$tr{'secondary wins'}</td>
	<td><input type='text' name='WINS2' value='$dhcpsettings{'WINS2'}' id='wins2' @{[jsvalidip('wins2','true')]}  ></td>
</tr>
<tr>
	<td class='base'>$tr{'default lease time'}</td>
	<td><input type='text' name='DEFAULT_LEASE_TIME' value='$dhcpsettings{'DEFAULT_LEASE_TIME'}' id='default_lease_time' @{[jsvalidnumber('default_lease_time',1,400)]}></td>
	<td class='base'>$tr{'max lease time'}</td>
	<td><input type='text' name='MAX_LEASE_TIME' value='$dhcpsettings{'MAX_LEASE_TIME'}' id='max_lease_time' @{[jsvalidnumber('max_lease_time',1,400)]}></td>
</tr>
<tr>
	<td class='base'><IMG SRC='/ui/img/blob.gif' alt='*'>&nbsp;$tr{'domain name suffix'}</td>
	<td><input type='text' name='DOMAIN_NAME' value='$dhcpsettings{'DOMAIN_NAME'}' id='domain_name' @{[jsvalidregex('domain_name','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$', 'true')]} ></td>
	<td class='base'>$tr{'nis_domainc'}</TD>
	<td><input type='text' name='NIS_DOMAIN' value='$dhcpsettings{'NIS_DOMAIN'}' id='nis_domain' @{[jsvalidregex('nis_domain','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$','true')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'primary nisc'}</TD>
	<td><input type='text' name='NIS1' value='$dhcpsettings{'NIS1'}' id='nis1' @{[(jsvalidip('nis1','true'))]}></td>
	<td class='base'>$tr{'secondary nisc'}</TD>
	<td><input type='text' name='NIS2' value='$dhcpsettings{'NIS2'}' id='nis2' @{[(jsvalidip('nis2','true'))]}></td>
</tr>
<tr>
	<td class='base'>$tr{'enabled'}</td>
	<td><input type='checkbox' name='ENABLE' $checked{'ENABLE'}{'on'}></td>
	<td></td>
	<td></td>
</tr>
</table>
<BR>
<img src='/ui/img/blob.gif' alt='*' valign='top'>&nbsp; $tr{'this field may be blank'}
<br/>
<table class='centered'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
;

&closebox();

if ($display_dhcplease eq 'yes'){
  &openbox("Current dynamic leases:");

  my %render_settings =
  (
	'url'     => "/cgi-bin/dhcp.cgi?$dhcpsettings{'COLUMN_ONE'},$dhcpsettings{'ORDER_ONE'},[%COL%],[%ORD%],$subnet",
	'columns' =>
	[
    {
			column => '2',
			title  => "IP Address",
			size   => 15,
			sort   => \&ipcompare,
		},
		{
			column => '3',
			title  => "Lease Started",
			size   => 20,
			sort   => 'cmp'
		},
		{
			column => '4',
			title  => "Lease Expires",
 			size   => 20,
			align  => 'cmp',
		},
		{
			column => '5',
			title  => "MAC Address",
			size   => 20,
			align  => 'cmp',
		},
		{
			column => '6',
			title  => "Hostname",
			size   => 20,
			align  => 'cmp',
		},
		{
			column => '7',
			title  => "Active",
			size   => 10,
			tr     => 'onoff',
			align  => 'center',
		},
	]
  );

  &displaytable("$dhcptmpfile", \%render_settings, $dhcpsettings{'ORDER_TWO'}, $dhcpsettings{'COLUMN_TWO'} );
  unlink ($dhcptmpfile);

  &closebox();
}

&openbox($tr{'add a new static assignment'});
print <<END
<table class='centered'>
<tr>
	<td class='base' style='width: 25%;'>$tr{'hostnamec'}</td>
	<td style='width: 25%;'><input type='text' name='STATIC_HOST' value='$dhcpsettings{'STATIC_HOST'}' id='static_host' @{[jsvalidregex('static_host','^([a-zA-Z])+([\.a-zA-Z0-9_-])+$')]}></td>
	<td class='base' style='width: 25%;'>$tr{'descriptionc'}</td>
	<td style='width: 25%;'><input type='text' name='STATIC_DESC' value='$dhcpsettings{'STATIC_DESC'}' id='static_desc' @{[jsvalidregex('static_desc','^([a-zA-Z0-9_-]+)$','true')]} ></td>
</tr>
<tr>
	<td class='base'>$tr{'mac addressc'}</td>
	<td><input type='text' name='STATIC_MAC' value='$dhcpsettings{'STATIC_MAC'}' id='static_mac' @{[(jsvalidmac('static_mac'))]} ></td>
	<td class='base'>$tr{'ip addressc'}</td>
	<td><input type='text' name='STATIC_IP' value='$dhcpsettings{'STATIC_IP'}' id='static_ip' @{[(jsvalidip('static_ip'))]}></td>
</tr>
<tr>
	<td class='base'>$tr{'enabled'}</td>
	<td><input type='checkbox' name='DEFAULT_ENABLE_STATIC' $checked{'DEFAULT_ENABLE_STATIC'}{'on'}></td>
	<td style='text-align: right;'><input type='submit' name='ACTION' value='$tr{'add'}'></td>
	<td></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'current static assignments'});

my %render_settings =
(
	'url'     => "/cgi-bin/dhcp.cgi?[%COL%],[%ORD%],$dhcpsettings{'COLUMN_TWO'},$dhcpsettings{'ORDER_TWO'},$subnet",
	'columns' => 
	[
		{ 
			column => '1',
			title  => "$tr{'hostname'}",
			size   => 25,
			valign => 'top',
			maxrowspan => 2,
			sort   => 'cmp',
		},
		{
			column => '3',
			title  => "$tr{'ip address'}",
			size   => 25,
			sort   => \&ipcompare,
		},
		{
			column => '2',
			title  => "$tr{'mac address'}",
			size   => 20,
			sort   => 'cmp',
		},
		{
			column => '5',
			title  => "$tr{'enabledtitle'}",
			size   => 10,
			tr     => 'onoff',
			align  => 'center',
		},
		{
			title  => "$tr{'mark'}", 
			size   => 10,
			mark   => ' ',
		},
		{ 
			column => '4',
			title => "$tr{'description'}",
			break => 'line',
			spanadj => -1,
		}
	]
);

&displaytable( "${swroot}/dhcp/staticconfig-$dhcpsettings{'SUBNET'}", \%render_settings, $dhcpsettings{'ORDER_ONE'}, $dhcpsettings{'COLUMN_ONE'} );

print <<END
<table class='blank'>
<tr>
<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
<td style='text-align: center; width: 50%;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
</form>
END
;
&closebox();

if (-e "${swroot}/dhcp/uptodate") {
	&openbox($tr{'note'});
	print "<FONT CLASS='base'>$tr{'there are unsaved changes'}<FONT>\n";
	print <<END;
<table class='centered'>
<tr>
	<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'save'}'></td>
</tr>
</table>
END
	&closebox();
}

&alertbox('add','add');

&closebigbox();

&closepage();

sub ip2number
{
	my $ip = $_[0];
	
	if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
		return 0; }
	else {
		return ($1*(256*256*256))+($2*(256*256))+($3*256)+($4); }
}

sub dhcp_lease_table
{
### Simple DHCP Lease Viewer (2007-0905) put together by catastrophe
# - Borrowed "dhcpLeaseData" subroutine from dhcplease.pl v0.2.5 (DHCP Pack v1.3) for SWE2.0
# by Dane Robert Jones and Tiago Freitas Leal
# - Borrowed parts of "displaytable" subroutine from smoothtype.pm
# (SmoothWall Express "Types" Module) from SWE3.0 by the SmoothWall Team
# - Josh DeLong - 09/15/07 - Added unique filter
# - Josh DeLong - 09/16/07 - Fixed sort bug and added ability to sort columns
# - Josh DeLong - 10/1/07 - Rewrote complete dhcp.cgi to use this code
###

my $leaseCount = -1;
my $dhcpstart = substr($dhcpsettings{'START_ADDR'}, 0, rindex($dhcpsettings{'START_ADDR'}, ".") + 1);

$dhcplIPAddy = " ";
$dhcplStart = " ";
$dhcplEnd = " ";
$dhcplBinding = " ";
$dhcplMACAddy = " ";
$dhcplHostName = " ";

# Location of DHCP Lease File
my $datfile = "/usr/etc/dhcpd.leases";
@catleasesFILENAME = `cat $datfile`;
chomp (@catleasesFILENAME);
for ($i=1; $i <= $#catleasesFILENAME; $i++){
  $datLine = $catleasesFILENAME[$i];

  if ($datLine =~ /^#/) {
  # Ignores comments
  } else {
      for ($datLine) {
      # Filter out leading & training spaces, double quotes, and remove end ';'
      s/^\s+//;
      s/\s+$//;
      s/\;//;
      s/\"//g;
      }
      if ($datLine =~ /^lease/) {

        $leaseCount++;      # Found start of lease
        @lineSplit = split(/ /,$datLine);       # Extract IP Address
        $dhcplIPAddy[$leaseCount] = $lineSplit[1];

      } elsif ($datLine =~ /^starts/) {

        @lineSplit = split(/ /,$datLine);     # Extract Lease Start Date
        $dhcplStart[$leaseCount] = "$lineSplit[2] $lineSplit[3]";

      } elsif ($datLine =~ /^ends/) {

        @lineSplit = split(/ /,$datLine);     # Extract Lease End Date
        $dhcplEnd[$leaseCount] = "$lineSplit[2] $lineSplit[3]";

      } elsif ($datLine =~ /^binding state active/) {

        $dhcplBinding[$leaseCount] = "on";    # Set 'on'

      } elsif ($datLine =~ /^binding state free/) {

        $dhcplBinding[$leaseCount] = "off";    # Set 'off'

      } elsif ($datLine =~ /^hardware ethernet/) {

        @lineSplit = split(/ /,$datLine);     # Extract MAC Address
        $dhcplMACAddy[$leaseCount] = uc($lineSplit[2]); # Make MAC Address All Upper Case for page consistancy.

      } elsif ($datLine =~ /^client-hostname/ || $datLine =~ /^hostname/) {

        @lineSplit = split(/ /,$datLine);     # Extract Host Name
        $dhcplHostName[$leaseCount] = $lineSplit[1];
      }
    }
}

open(FILE, ">$dhcptmpfile") or die 'Unable to open dhcp leasesconfig file.';
flock FILE, 2;

  for ($i = $#dhcplIPAddy; $i >= 0; $i--) {
    $catLINEnumber = $i+1;
    $dhcpprintvar = "True";

    if ($i == $#dhcplIPAddy){
        push(@dhcptemparray, $dhcplIPAddy[$i]);
    }
    else {
        foreach $IP (@dhcptemparray) {
            if ($IP =~ $dhcplIPAddy[$i]) {
                $dhcpprintvar = "False";
            }
        }
    }

    if (index($dhcplIPAddy[$i], $dhcpstart) == -1 )
    {
      $dhcpprintvar = "False"
    }

    # Printing values to temp file
    if ($dhcpprintvar =~ "True"){
      my $leaseStart = UTC2LocalString($dhcplStart[$i]);
      my $leaseEnd   = UTC2LocalString($dhcplEnd[$i]);

      push(@dhcptemparray, $dhcplIPAddy[$i]);
      print FILE "$catLINEnumber,$dhcplIPAddy[$i],$leaseStart,$leaseEnd,$dhcplMACAddy[$i],$dhcplHostName[$i],$dhcplBinding[$i],\n";
    }
  }
close(FILE);
}

sub UTC2LocalString
{
  my $t = shift;

  # Return it unchanged if it does not start with a date
  return $t unless $t =~ /[0-9][0-9][0-9][0-9]\/[0-9][0-9]\/[0-9][0-9]/;

  my ($lDate, $lTime) = split(/ /,$t,2);
  my ($year, $month, $day) = split(/\//,$lDate);
  my ($hour, $minute, $sec) = split(/:/,$lTime);
  
  #  proto: $time = timegm($sec,$min,$hour,$mday,$mon,$year);
  my $UTCtime = timegm ($sec,$minute,$hour,$day,$month-1,$year);
  
  #  proto: ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =
  #          localtime(time);
  my ($lsec,$lminute,$lhour,$lmday,$lmonth,$lyear,$lwday,$lyday,$lisdst) =
            (localtime($UTCtime));
  
  $lyear += 1900;  # year is 1900 based
  $lmonth++;       # month number is zero based
  #print "isdst: $isdst\n"; #debug flag day-light-savings time
  return ( sprintf("%4.4d/%2.2d/%2.2d %2.2d:%2.2d:%2.2d",
           $lyear,$lmonth,$lmday,$lhour,$lminute,$lsec) );
}
