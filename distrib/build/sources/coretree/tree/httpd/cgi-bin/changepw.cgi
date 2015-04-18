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
use smoothtype qw( :standard );

my %cgiparams;
my $errormessage = "";
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
my $life = 30;   # seconds
my $toSum = $tmp . int($time/$life) ."\n";
$newToken = sha1_hex $toSum;
$toSum = $tmp . int($time/$life - 1) ."\n";
$lastToken = sha1_hex $toSum;

# Clear these, just in case
undef $time;
undef $toSum;
undef $tmp;

$cgiparams{'ACTION_ADMIN'} = '';
$cgiparams{'ACTION_DIAL'} = '';

&getcgihash(\%cgiparams);
$rtnToken = $cgiparams{'Token'};

if ($cgiparams{'ACTION_ADMIN'} eq $tr{'save'} or $cgiparams{'ACTION_DIAL'} eq $tr{'save'})
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

		&openpage($tr{'change passwords'}, 1, '', 'maintenance');
		&openbigbox('100%', 'LEFT');
		&alertbox($errormessage);
		print "<p style='margin:0'>&nbsp;</p>\n";
		&closebigbox;
		&closepage;

		exit;
	}
}

&showhttpheaders();

if ($cgiparams{'ACTION_ADMIN'} eq $tr{'save'})
{
	my $password1 = $cgiparams{'ADMIN_PASSWORD1'};
	my $password2 = $cgiparams{'ADMIN_PASSWORD2'};
	if ($password1 eq $password2)
	{
		if ($password1 =~ m/\s|\"/)
		{
			$errormessage .= $tr{'password contains illegal characters'} ."<br />\n";
		}
		elsif (length($password1) >= 6)
		{
			system('/usr/sbin/htpasswd', '-m', '-b', "${swroot}/auth/users", 'admin', "${password1}");
			&log($tr{'admin user password has been changed'});
		}
		else
		{
			$errormessage .= $tr{'passwords must be at least 6 characters in length'} ."<br />\n";
		}
	}
	else
	{
		$errormessage = $tr{'passwords do not match'} ."<br />\n";
	}
}

if ($cgiparams{'ACTION_DIAL'} eq $tr{'save'})
{
	my $password1 = $cgiparams{'DIAL_PASSWORD1'};
	my $password2 = $cgiparams{'DIAL_PASSWORD2'};
	if ($password1 eq $password2)
	{
		if($password1 =~ m/\s|\"/)
		{
			$errormessage = $tr{'password contains illegal characters'} ."<br />\n";
		}
		elsif (length($password1) >= 6)
		{
			system('/usr/sbin/htpasswd', '-m', '-b', "${swroot}/auth/users", 'dial', "${password1}");
			&log($tr{'dial user password has been changed'});
		}
		else
		{
			$errormessage = $tr{'passwords must be at least 6 characters in length'} ."<br />\n";
		}
	}
	else
	{
		$errormessage = $tr{'passwords do not match'} ."<br />\n";
	}
}

&openpage($tr{'change passwords'}, 1, '', 'maintenance');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<form method='post'>\n";
	print "  <input type='hidden' name='Token' value='$newToken'>\n";

&openbox($tr{'administrator user password'});
print <<END;
  <table width='100%'>
  <tr>
      <td width='15%' class='base'>$tr{'password'}</td>
      <td width='30%'>
        <input type='password' name='ADMIN_PASSWORD1' id='admin_password1'
               @{[jsvalidpassword('admin_password1','admin_password2','^([^ \|]*)$')]}>
      </td>
      <td width='15%' class='base'>$tr{'again'}</td>
      <td width='30%'>
        <input type='password' name='ADMIN_PASSWORD2' id='admin_password2'
               @{[jsvalidpassword('admin_password2','admin_password1','^([^ \|]*)$')]}>
      </td>
      <td width='10%'><input type='submit' name='ACTION_ADMIN' value='$tr{'save'}'></td>
  </tr>
  </table>
END

&closebox();

&openbox($tr{'dial user password'});
print <<END;
  <table width='100%'>
    <tr>
      <td width='15%' class='base'>$tr{'password'}</td>
      <td width='30%'>
        <input type='password' name='DIAL_PASSWORD1' id='dial_password1'
               @{[jsvalidpassword('dial_password1','dial_password2','^([^ \|]*)$')]}>
      </td>
      <td width='15%' class='base'>$tr{'again'}</td>
      <td width='30%'>
        <input type='password' name='DIAL_PASSWORD2' id='dial_password2'
               @{[jsvalidpassword('dial_password2','dial_password1','^([^ \|]*)$')]} >
      </td>
      <td width='10%'><input type='submit' name='ACTION_DIAL' value='$tr{'save'}'></td>
    </tr>
  </table>
END

&closebox();

print "</form>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();
