#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

use Socket;

my %cgiparams;
my @addrs; my @vars;
my $addr;
my $var;
my $hostname;

&getcgihash(\%cgiparams);

&showhttpheaders();

@addrs = split(/,/, $cgiparams{'IP'});
foreach $addr (@addrs)
{
	if (!&validipormask($addr) and !&validhostname($addr))
	{
		$errormessage .= $tr{'invalid addresses or names'} ."<br />";
		last;
	}
}

&openpage($tr{'ip info'}, 1, '', 'tools');

&openbigbox('100%', 'left');

&alertbox($errormessage);

print "<form method='post'>\n";

&openbox($tr{'whois lookupc'});

print <<END;
<table width='100%'>
  <tr>
    <td width='20%' class='base'>$tr{'ip addresses or domain names'}</td>
    <td width='65%'><input type='text' size='60' name='IP' value='$cgiparams{'IP'}'></td>
    <td width='15%' align='center'><input type='submit' name='ACTION' value='$tr{'run'}'></td>
  </tr>
</table>
END

&closebox();

if ($cgiparams{'ACTION'} eq $tr{'run'})
{
	unless ($errormessage)
	{
		foreach $addr (@addrs)
		{
        		$hostname = gethostbyaddr(inet_aton($addr), AF_INET);
       			if (!$hostname) { $hostname = $tr{'lookup failed'}; }
			&openbox("$addr ($hostname)");
			print "<pre style='max-width:500px'>\n";
			system('/usr/bin/whois', '--nocgi', '-s', $addr);
			print "</pre>\n";
			&closebox();
		}
	}	
}

print "</form>\n";

&alertbox('add','add');

&closebigbox();

&closepage();
