#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use Digest::SHA qw(sha1_hex);
use header qw( :standard );
use smoothd qw( message );

my %cgiparams;
my $errormessage;
my $death = 0;
my $rebirth = 0;
my ($lastToken, $newToken, $rtnToken);
my $tmp = "";

# Generate a new token and the previous token on each entry.
foreach $token ("1","2","3")
{
  if (open TKN,"</usr/etc/token${token}.sum")
  {
    $tmp .= <TKN>;
    close TKN;
  }
  else
  {
    $errormessage .= "Can't read token${token}.<br />";
  }
}

my $time = time;
my $life = 10;   # seconds
my $toSum = $tmp . int($time/$life) ."\n";
$newToken = sha1_hex $toSum;
$toSum = $tmp . int($time/$life - 1) ."\n";
$lastToken = sha1_hex $toSum;

# Clear these, just in case
undef $time;
undef $toSum;
undef $tmp;

$cgiparams{'ACTION'} = '';
&getcgihash(\%cgiparams);
$rtnToken = $cgiparams{'Token'};

if ($cgiparams{'ACTION'} eq $tr{'shutdown'} or $cgiparams{'ACTION'} eq $tr{'reboot'})
{
	# Validate $rtnToken, then compare it with $newToken and $lastToken
	if ($rtnToken !~ /[0-9a-f]/ or ($rtnToken != $newToken and $rtnToken != $lastToken))
	{
		$errormessage = "
Incorrect security token; returning to home page!<br /><br />
This happens when you wait too long to click an action button (Reboot/Shutdown/Save)<br />
to shut down or reboot the system or to change passwords.<br />
";
		print <<END;
Refresh: 6; url=/cgi-bin/index.cgi\r
Content-type: text/html\r
\r
END

		&openpage($tr{'shutdown control'}, 1, '', 'maintenance');
		&openbigbox('100%', 'LEFT');
		&alertbox($errormessage);
		print "<p style='margin:0'>&nbsp;</p>\n";
		&closebigbox;
		&closepage;

		exit;
	}
}

&showhttpheaders();

if ($cgiparams{'ACTION'} eq $tr{'shutdown'})
{
	$death = 1;
	
	&log($tr{'shutting down smoothwall'});
	
	my $success = message('systemshutdown');
	
	if (not defined $success)
	{
		$errormessage = $tr{'smoothd failure'};
	}
}
elsif ($cgiparams{'ACTION'} eq $tr{'reboot'})
{
	$rebirth = 1;

	&log($tr{'rebooting smoothwall'});

	my $success = message('systemrestart');

	if (not defined $success)
	{
		$errormessage = $tr{'smoothd failure'};
	}
}

if ($death == 0 && $rebirth == 0)
{
	&openpage($tr{'shutdown control'}, 1, '', 'maintenance');

	&openbigbox('100%', 'LEFT');

	&alertbox($errormessage);

	print "<form method='post'>\n";
	print "  <input type='hidden' name='Token' value='$newToken'>\n";

	&openbox($tr{'shutdown2'});
	my $myName = `hostname`;
	chomp $myName;
	$myName = " ($myName)";

	print <<END;
  <table width='100%'>
    <tr>
      <td align='center'>
        <input type='submit' name='ACTION' value='$tr{'reboot'}'
               onClick="if(confirm('Are you sure you want to reboot this Smoothwall$myName?')) {return true;} return false;">
      </td>
      <td align='center'>
        <input type='submit' name='ACTION' value='$tr{'shutdown'}'
               onClick="if(confirm('Are you sure you want to shutdown this Smoothwall$myName?')) {return true;} return false;">
      </td>
    </tr>
  </table>
END

	&closebox();

	print "</form>\n";
}
else
{
	my ($message,$title);
	if ($death)
	{
		$title = $tr{'shutting down'};
		$message = $tr{'smoothwall is shutting down'};
	}
	else
	{
		$title = $tr{'rebooting'};
		$message = $tr{'smoothwall is rebooting'};
	}
	&openpage($title, 1, '', 'shutdown');

	&openbigbox('100%', 'CENTER');
	print <<END;
<div align='center'>
  <table bgcolor='#ffffff'>
    <tr>
      <td align='center'>
        <a href='/' border='0'><img src='/ui/img/smoothwall_big.png'></a><br /><br />
END

	&alertbox($message);

	print <<END;
      </td>
    </tr>
  </table>
</div>
END
}

&alertbox('add', 'add');

&closebigbox();

&closepage();
