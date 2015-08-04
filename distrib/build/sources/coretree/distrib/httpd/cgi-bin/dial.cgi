#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );

my %cgiparams;

$cgiparams{'ACTION'} = '';
&getcgihash(\%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'dial'})
{
	my $success = message('updown', 'UP');
		
	if (not defined $success)
	{
		&log("Dial failed");
	}
}
elsif ($cgiparams{'ACTION'} eq $tr{'hangup'})
{
	my $success = message('updown', 'DOWN');
		
	if (not defined $success)
	{
		&log("Hangup failed");
	}
	else
	{
		if ( -e "${swroot}/red/active" )
		{
			# If it failed silently, it might not've ever come up, so
			#   be sure it doesn't get stuck in a false up state.
			system ("/etc/ppp/ip-down");
		}
	}
}

sleep 1;

print "Status: 302 Moved\nLocation: /cgi-bin/index.cgi\n\n";
