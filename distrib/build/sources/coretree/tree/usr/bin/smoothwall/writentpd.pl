#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) SmoothWall Ltd 2002, 2003

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %netsettings, %timesettings;

&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/time/settings", \%timesettings);

open (FILE, ">${swroot}/time/ntpd.conf");

# Listen on lo and GREEN
print FILE <<END;
listen on 127.0.0.1
listen on $netsettings{'GREEN_ADDRESS'}
END
if ($netsettings{'PURPLE_DEV'})
{
	# Listen on PURPLE
	print FILE <<END;
listen on $netsettings{'PURPLE_ADDRESS'}
END
}

# Query the upstream
	print FILE <<END;
server $timesettings{'NTP_SERVER'}
END

close (FILE);
