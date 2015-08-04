#!/usr/bin/perl
#
# SmoothWall CGIs
#
# (c) SmoothWall Ltd, 2005

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

my $version = "1.0.0";

my %apcupsdsettings;
my %checked; my %selected;

sub validemailaddr() {
	my ($email) = @_;

        my $okaddr = 1;
	my ($tmpnam, $tmphst) = split ("@", $email);
        if ($tmpnam !~ /[a-zA-Z0-9._+-]*/ ) { $okaddr = 0; }
        if (! (&validhostname ($tmphst) or &validip($tmphst))) { $okaddr = 0; }
	return $okaddr;
}

&showhttpheaders();

$apcupsdsettings{'ACTION'} = '';
$apcupsdsettings{'ALERTADDR'} = '';
$apcupsdsettings{'ANNOY'} = '300';
$apcupsdsettings{'BATTDELAY'} = '10';
$apcupsdsettings{'BATTLEVEL'} = '15';
$apcupsdsettings{'CC1ADDR'} = '';
$apcupsdsettings{'CC2ADDR'} = '';
$apcupsdsettings{'ENABLE'} = 'off';
$apcupsdsettings{'ENABLEALERTS'} = 'off';
$apcupsdsettings{'FROMADDR'} = '';
$apcupsdsettings{'KILLPOWER'} = 'off';
$apcupsdsettings{'MAILSVR'} = '';
$apcupsdsettings{'MSGANNOY'} = 'off';
$apcupsdsettings{'MSGBATTATTACH'} = 'off';
$apcupsdsettings{'MSGBATTDETACH'} = 'off';
$apcupsdsettings{'MSGCHANGEME'} = 'off';
$apcupsdsettings{'MSGCOMMFAILURE'} = 'off';
$apcupsdsettings{'MSGCOMMOK'} = 'off';
$apcupsdsettings{'MSGDOSHUTDOWN'} = 'off';
$apcupsdsettings{'MSGEMERGENCY'} = 'off';
$apcupsdsettings{'MSGENDSELFTEST'} = 'off';
$apcupsdsettings{'MSGFAILING'} = 'off';
$apcupsdsettings{'MSGKILLPOWER'} = 'off';
$apcupsdsettings{'MSGLOADLIMIT'} = 'off';
$apcupsdsettings{'MSGOFFBATTERY'} = 'off';
$apcupsdsettings{'MSGONBATTERY'} = 'off';
$apcupsdsettings{'MSGPOWERBACK'} = 'off';
$apcupsdsettings{'MSGPOWEROUT'} = 'off';
$apcupsdsettings{'MSGREMOTEDOWN'} = 'off';
$apcupsdsettings{'MSGRUNLIMIT'} = 'off';
$apcupsdsettings{'MSGSTARTSELFTEST'} = 'off';
$apcupsdsettings{'MSGTIMEOUT'} = 'off';
$apcupsdsettings{'NISPORT'} = '3551';
$apcupsdsettings{'POLLTIME'} = '60';
$apcupsdsettings{'RTMIN'} = '10';
$apcupsdsettings{'STANDALONE'} = '';
$apcupsdsettings{'TESTING'} = 'off';
$apcupsdsettings{'TO'} = '0';
$apcupsdsettings{'UPSAUTH'} = '';
$apcupsdsettings{'UPSIP'} = '';
$apcupsdsettings{'UPSMODE'} = '';
$apcupsdsettings{'UPSNAME'} = '';
$apcupsdsettings{'UPSPORT'} = '';
$apcupsdsettings{'UPSUSER'} = '';
$apcupsdsettings{'VALID'} = '';

&getcgihash(\%apcupsdsettings);

my $errormessage = '';

if ($apcupsdsettings{'ACTION'} eq $tr{'save and restart'}) {
	# First, validate all entry fields for blank or valid content
	if ($apcupsdsettings{'ALERTADDR'} ne "" and ! &validemailaddr($apcupsdsettings{'ALERTADDR'})) {
		$errormessage .= $tr{"apc invalid alert addr"} ."<br />";
	}
	if ($apcupsdsettings{'ANNOY'} !~ /[0-9]+/ ) { $errormessage .= $tr{"apc invalid annoy time"} ."<br />"; }
	if ($apcupsdsettings{'BATTDELAY'} !~ /[0-9]+/ ) { $errormessage .= $tr{"apc invalid batt delay"} ."<br />"; }
	if ($apcupsdsettings{'BATTLEVEL'} !~ /[0-9]+/ ) { $errormessage .= $tr{"apc invalid batt level"} ."<br />"; }
	if ($apcupsdsettings{'CC1ADDR'} ne "" and ! &validemailaddr($apcupsdsettings{'CC1ADDR'})) {
		$errormessage .= $tr{"apc invalid cc1 addr"} ."<br />";
	}
	if ($apcupsdsettings{'CC2ADDR'} ne "" and ! &validemailaddr($apcupsdsettings{'CC2ADDR'})) {
		$errormessage .= $tr{"apc invalid cc2 addr"} ."<br />";
	}
	if ($apcupsdsettings{'FROMADDR'} ne "" and ! &validemailaddr($apcupsdsettings{'FROMADDR'})) {
		$errormessage .= $tr{"apc invalid from addr"} ."<br />";
	}
	if ($apcupsdsettings{'MAILSVR'} ne "" and !&validip($apcupsdsettings{'MAILSVR'}) and ! &validhostname($apcupsdsettings{'MAILSVR'})) {
		$errormessage .= $tr{"apc invalid svr addr"} ."<br />";
	}
	if ($apcupsdsettings{'NISPORT'} ne "" and not &validport($apcupsdsettings{'NISPORT'}) ) {
		$errormessage .= $tr{"apc invalid nis port"} ."<br />";
	}
	if ($apcupsdsettings{'POLLTIME'} ne "" and $apcupsdsettings{'POLLTIME'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid poll time"} ."<br />";
	}
	if ($apcupsdsettings{'RTMIN'} ne "" and $apcupsdsettings{'RTMIN'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid min runtime"} ."<br />";
	}
	if ($apcupsdsettings{'TO'} ne "" and $apcupsdsettings{'TO'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid time out"} ."<br />";
	}
	if ($apcupsdsettings{'UPSAUTH'} =~ /[<>]/ ) { $errormessage .= $tr{"apc invalid password"} ."<br />"; }

	my ($tmphost,$tmpport) = split(":",$apcupsdsettings{'UPSIP'});
	if ($tmphost ne "" and not &validip($tmphost) and not &validhostname($tmphost)) {
		$errormessage .= $tr{"apc invalid ups ip host"} ."<br />";
	}
	if ($tmpport ne "" and not &validport($tmpport)) {
		$errormessage .= $tr{"apc invalid ups ip port"} ."<br />";
	}
	if ($apcupsdsettings{'UPSMODE'} ne "" and $apcupsdsettings{'UPSMODE'} !~ /[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid ups mode"} ."<br />";
	}
	if ($apcupsdsettings{'UPSNAME'} =~ /[<>]/ ) { $errormessage .= $tr{"apc invalid ups name"} ."<br />"; }

	if ($apcupsdsettings{'UPSPORT'} ne "" and 
	    $apcupsdsettings{'UPSPORT'} !~ /\/dev\/ttyS[0-9]+/ and
	    $apcupsdsettings{'UPSPORT'} !~ /\/dev\/ttyUSB[0-9]+/ ) {
		$errormessage .= $tr{"apc invalid serial port"} ."<br />";
	}
	if ($apcupsdsettings{'UPSUSER'} =~ /[<>]/ ) { $errormessage .= $tr{"apc invalid username"} ."<br />"; }


	# Now warn when things don't quite line up
	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'TO'}) ne '0')
	{
	$errormessage .= $tr{"Pls Leave Shutdown After Time on Batt"} .'<br />';     
	}

	if  ((($apcupsdsettings{'UPSMODE'} eq '1') or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '5')) && ($apcupsdsettings{'UPSPORT'}) ne '' )
	 {
	$errormessage .= $tr{"Pls Leave Serial Blank USB PC"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '5' && (!(&validip($apcupsdsettings{'UPSIP'}))))
	 {
	$errormessage .= $tr{"invalid ups IP"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSUSER'} eq '' ) 
	 {
	$errormessage .= $tr{"Pls Enter Username"} .'<br />';
	}
        
	if ($apcupsdsettings{'UPSMODE'} eq '5' && $apcupsdsettings{'UPSAUTH'} eq '' )
	{
	$errormessage .= $tr{"Pls Enter Password"} .'<br />';
	}

	if (($apcupsdsettings{'UPSMODE'} eq '0')
	 or ($apcupsdsettings{'UPSMODE'} eq '2')
	 or ($apcupsdsettings{'UPSMODE'} eq '6')
	 or ($apcupsdsettings{'UPSMODE'} eq '7')
	 or ($apcupsdsettings{'UPSMODE'} eq '8')
	 or ($apcupsdsettings{'UPSMODE'} eq '9')
	 or ($apcupsdsettings{'UPSMODE'} eq '10')
	 or ($apcupsdsettings{'UPSMODE'} eq '11')
	 or ($apcupsdsettings{'UPSMODE'} eq '12')
	 or ($apcupsdsettings{'UPSMODE'} eq '13')
	 or ($apcupsdsettings{'UPSMODE'} eq '14')
	 or ($apcupsdsettings{'UPSMODE'} eq '15')
	 or ($apcupsdsettings{'UPSMODE'} eq '16')
	 or ($apcupsdsettings{'UPSMODE'} eq '17')
	 or ($apcupsdsettings{'UPSMODE'} eq '18'))
	{
	unless ($apcupsdsettings{'UPSPORT'} =~ /^\/dev\/tty[A-Z][0-9]/ )
		{
		$errormessage .= $tr{"Pls Enter Serial Port"} .'<br />';
		}
	}

	if ((($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'TO'}) <= '119')
	{
	$errormessage .= $tr{"Pls Select Shutdown Time SimpleSig"} .'<br />';
	}

	if ((($apcupsdsettings{'UPSMODE'} eq '0')
	  or ($apcupsdsettings{'UPSMODE'} eq '1')
	  or ($apcupsdsettings{'UPSMODE'} eq '2')
	  or ($apcupsdsettings{'UPSMODE'} eq '3')
	  or ($apcupsdsettings{'UPSMODE'} eq '6')
	  or ($apcupsdsettings{'UPSMODE'} eq '7')
	  or ($apcupsdsettings{'UPSMODE'} eq '8')
	  or ($apcupsdsettings{'UPSMODE'} eq '9')
	  or ($apcupsdsettings{'UPSMODE'} eq '10')
	  or ($apcupsdsettings{'UPSMODE'} eq '11')
	  or ($apcupsdsettings{'UPSMODE'} eq '12')
	  or ($apcupsdsettings{'UPSMODE'} eq '13')
	  or ($apcupsdsettings{'UPSMODE'} eq '14')
	  or ($apcupsdsettings{'UPSMODE'} eq '15')
	  or ($apcupsdsettings{'UPSMODE'} eq '16')
	  or ($apcupsdsettings{'UPSMODE'} eq '17')
	  or ($apcupsdsettings{'UPSMODE'} eq '18')) && ($apcupsdsettings{'UPSIP'}) ne '')
	{
	$errormessage .= $tr{"Pls Leave IP Blank"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSUSER'} ne '' ) 
	{
	$errormessage .= $tr{"Username Not Required"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} ne '5' && $apcupsdsettings{'UPSAUTH'} ne '' )
	{
	$errormessage .= $tr{"Password Not Required"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSPORT'}) ne '' )
	{
	$errormessage .= $tr{"Pls Leave Serial Blank Slave"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'KILLPOWER'}) eq 'on')
	{
	$errormessage .= $tr{"UPS Killpower Incompatible Slave"} .'<br />';
	}

	if ($apcupsdsettings{'UPSMODE'} eq '4' && ($apcupsdsettings{'UPSIP'}) eq '')
	{
	$errormessage .= $tr{"Pls Enter IP"} .'<br />';
	}

	if ($apcupsdsettings{'POLLTIME'} >= 301 || $apcupsdsettings{'POLLTIME'} <= 19 ) 
	{
	$errormessage .= 'Invalid Poll time, enter a value between 20 and 300<br />';
	}

	# Don't validate email addrs, etc., if notifications are not enabled
	if ($apcupsdsettings{'ENABLEALERTS'} eq 'on')
	{
		if (! &validemailaddr($apcupsdsettings{'FROMADDR'}))
		{
		$errormessage .= 'Please enter a valid From address<br />';
		}
	
		if (! &validemailaddr($apcupsdsettings{'ALERTADDR'}))
		{
		$errormessage .= 'Please enter a valid Alert address<br />';
		}
	
		if ($apcupsdsettings{'CC1ADDR'} ne '') {
			unless ($apcupsdsettings{'CC1ADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
			{
			$errormessage .= 'Please enter a valid Alert2 address<br />';
			}
		}
	
		if ($apcupsdsettings{'CC2ADDR'} ne '') {
			unless ($apcupsdsettings{'CC2ADDR'} =~ (/^[A-z0-9_\-\.]+[@][A-z0-9_\-.]+[A-z]{2,}$/))
			{
			$errormessage .= 'Please enter a valid Alert3 address<br />';
		 	}
		}
	
		if ($apcupsdsettings{'MAILSVR'} eq '')
		{
		$errormessage .= 'Please enter valid mailserver<br />';
		}
	}

	if ($apcupsdsettings{'BATTLEVEL'} >= 96 || $apcupsdsettings{'BATTLEVEL'} <= 4 )
	{
	$errormessage .= 'Please enter % of battery remaining between 5 and 95<br />';
	}

	if ($apcupsdsettings{'BATTDELAY'} >= 301 || $apcupsdsettings{'BATTDELAY'} <= -1 )
	{
	$errormessage .= 'Invalid on battery response delay, enter a value between 0 and 300<br />';
	}

	if ($apcupsdsettings{'RTMIN'} <= 4 )
	{
	$errormessage .= 'Invalid minimum runtime, enter a value of 5 or greater<br />';
	}

	if (length $apcupsdsettings{'UPSNAME'} > 8)
	{
	$errormessage .= 'Please use 8 characters or less for UPS name<br />';
	}

	if ($apcupsdsettings{'ANNOY'} eq '')
	{
	$errormessage .= 'Please enter Annoy Message Period<BR>Default is 300 Seconds<br />';
	}

ERROR:
	if ($errormessage) {
                $apcupsdsettings{'VALID'} = 'no'; }		
	else {
                $apcupsdsettings{'VALID'} = 'yes';
	}

	if ($apcupsdsettings{'VALID'} eq 'yes') {
		
		&log("APCupsd service restarted.");
	
		&writehash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
		
		my $success = message("apcupsdwrite");
		
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'} .": apcupsdwrite";
		}
		$success = message("apcupsdrestart");
		
		if (not defined $success) {
			$errormessage = $tr{'smoothd failure'} .": apcupsdrestart";
		}
	}
}

if ($apcupsdsettings{'ACTION'} eq '' )
{
	$apcupsdsettings{'ENABLE'} = 'off';
	$apcupsdsettings{'NOLOGINTYPE'} = '0';
	$apcupsdsettings{'OPMODE'} = 'testing';

	if (-e "/var/smoothwall/apcupsd/settings") {
		&readhash("/var/smoothwall/apcupsd/settings", \%apcupsdsettings);
	}
}

if ($apcupsdsettings{'ACTION'} eq $tr{'restart'})
{
	&log("APCupsd service restarted.");

	my $success = message("apcupsdrestart");
	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'};
	}
}

if ($apcupsdsettings{'ACTION'} eq $tr{'stop'})
{
	&log("APCupsd service stopped.");

	my $success = message("apcupsdstop");
	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'};
	}
}

$checked{'ENABLE'}{'off'} = '';
$checked{'ENABLE'}{'on'} = '';
$checked{'ENABLE'}{$apcupsdsettings{'ENABLE'}} = 'CHECKED';

$checked{'ENABLEALERTS'}{'off'} = '';
$checked{'ENABLEALERTS'}{'on'} = '';
$checked{'ENABLEALERTS'}{$apcupsdsettings{'ENABLEALERTS'}} = 'CHECKED';

$selected{'OPMODE'}{'testing'} = '';
$selected{'OPMODE'}{'full'} = '';
$selected{'OPMODE'}{$apcupsdsettings{'OPMODE'}} = 'SELECTED';

$checked{'STANDALONE'}{'off'} = '';
$checked{'STANDALONE'}{'on'} = '';
$checked{'STANDALONE'}{$apcupsdsettings{'STANDALONE'}} = 'CHECKED';

$checked{'SHELLLOGIN'}{'off'} = '';
$checked{'SHELLLOGIN'}{'on'} = '';
$checked{'SHELLLOGIN'}{$apcupsdsettings{'SHELLLOGIN'}} = 'CHECKED';

$checked{'KILLPOWER'}{'off'} = '';
$checked{'KILLPOWER'}{'on'} = '';
$checked{'KILLPOWER'}{$apcupsdsettings{'KILLPOWER'}} = 'CHECKED';

$selected{'UPSMODE'}{'0'} = '';
$selected{'UPSMODE'}{'1'} = '';
$selected{'UPSMODE'}{'2'} = '';
$selected{'UPSMODE'}{'3'} = '';
$selected{'UPSMODE'}{'4'} = '';
$selected{'UPSMODE'}{'5'} = '';
$selected{'UPSMODE'}{'6'} = '';
$selected{'UPSMODE'}{'7'} = '';
$selected{'UPSMODE'}{'8'} = '';
$selected{'UPSMODE'}{'9'} = '';
$selected{'UPSMODE'}{'10'} = '';
$selected{'UPSMODE'}{'11'} = '';
$selected{'UPSMODE'}{'12'} = '';
$selected{'UPSMODE'}{'13'} = '';
$selected{'UPSMODE'}{'14'} = '';
$selected{'UPSMODE'}{'15'} = '';
$selected{'UPSMODE'}{'16'} = '';
$selected{'UPSMODE'}{'17'} = '';
$selected{'UPSMODE'}{'18'} = '';
$selected{'UPSMODE'}{$apcupsdsettings{'UPSMODE'}} = 'SELECTED';

$selected{'NOLOGINTYPE'}{'0'} = '';
$selected{'NOLOGINTYPE'}{'1'} = '';
$selected{'NOLOGINTYPE'}{'2'} = '';
$selected{'NOLOGINTYPE'}{'3'} = '';
$selected{'NOLOGINTYPE'}{$apcupsdsettings{'NOLOGINTYPE'}} = 'SELECTED';

$checked{'MSGPOWEROUT'}{'off'} = '';
$checked{'MSGPOWEROUT'}{'on'} = '';
$checked{'MSGPOWEROUT'}{$apcupsdsettings{'MSGPOWEROUT'}} = 'CHECKED';

$checked{'MSGPOWERBACK'}{'off'} = '';
$checked{'MSGPOWERBACK'}{'on'} = '';
$checked{'MSGPOWERBACK'}{$apcupsdsettings{'MSGPOWERBACK'}} = 'CHECKED';

$checked{'MSGKILLPOWER'}{'off'} = '';
$checked{'MSGKILLPOWER'}{'on'} = '';
$checked{'MSGKILLPOWER'}{$apcupsdsettings{'MSGKILLPOWER'}} = 'CHECKED';

$checked{'MSGEMERGENCY'}{'off'} = '';
$checked{'MSGEMERGENCY'}{'on'} = '';
$checked{'MSGEMERGENCY'}{$apcupsdsettings{'MSGEMERGENCY'}} = 'CHECKED';

$checked{'MSGCHANGEME'}{'off'} = '';
$checked{'MSGCHANGEME'}{'on'} = '';
$checked{'MSGCHANGEME'}{$apcupsdsettings{'MSGCHANGEME'}} = 'CHECKED';

$checked{'MSGFAILING'}{'off'} = '';
$checked{'MSGFAILING'}{'on'} = '';
$checked{'MSGFAILING'}{$apcupsdsettings{'MSGFAILING'}} = 'CHECKED';

$checked{'MSGANNOY'}{'off'} = '';
$checked{'MSGANNOY'}{'on'} = '';
$checked{'MSGANNOY'}{$apcupsdsettings{'MSGANNOY'}} = 'CHECKED';

$checked{'MSGCOMMFAILURE'}{'off'} = '';
$checked{'MSGCOMMFAILURE'}{'on'} = '';
$checked{'MSGCOMMFAILURE'}{$apcupsdsettings{'MSGCOMMFAILURE'}} = 'CHECKED';

$checked{'MSGCOMMOK'}{'off'} = '';
$checked{'MSGCOMMOK'}{'on'} = '';
$checked{'MSGCOMMOK'}{$apcupsdsettings{'MSGCOMMOK'}} = 'CHECKED';

$checked{'MSGONBATTERY'}{'off'} = '';
$checked{'MSGONBATTERY'}{'on'} = '';
$checked{'MSGONBATTERY'}{$apcupsdsettings{'MSGONBATTERY'}} = 'CHECKED';

$checked{'MSGOFFBATTERY'}{'off'} = '';
$checked{'MSGOFFBATTERY'}{'on'} = '';
$checked{'MSGOFFBATTERY'}{$apcupsdsettings{'MSGOFFBATTERY'}} = 'CHECKED';

$checked{'MSGTIMEOUT'}{'off'} = '';
$checked{'MSGTIMEOUT'}{'on'} = '';
$checked{'MSGTIMEOUT'}{$apcupsdsettings{'MSGTIMEOUT'}} = 'CHECKED';

$checked{'MSGLOADLIMIT'}{'off'} = '';
$checked{'MSGLOADLIMIT'}{'on'} = '';
$checked{'MSGLOADLIMIT'}{$apcupsdsettings{'MSGLOADLIMIT'}} = 'CHECKED';

$checked{'MSGRUNLIMIT'}{'off'} = '';
$checked{'MSGRUNLIMIT'}{'on'} = '';
$checked{'MSGRUNLIMIT'}{$apcupsdsettings{'MSGRUNLIMIT'}} = 'CHECKED';

$checked{'MSGDOSHUTDOWN'}{'off'} = '';
$checked{'MSGDOSHUTDOWN'}{'on'} = '';
$checked{'MSGDOSHUTDOWN'}{$apcupsdsettings{'MSGDOSHUTDOWN'}} = 'CHECKED';

$checked{'MSGREMOTEDOWN'}{'off'} = '';
$checked{'MSGREMOTEDOWN'}{'on'} = '';
$checked{'MSGREMOTEDOWN'}{$apcupsdsettings{'MSGREMOTEDOWN'}} = 'CHECKED';

$checked{'MSGSTARTSELFTEST'}{'off'} = '';
$checked{'MSGSTARTSELFTEST'}{'on'} = '';
$checked{'MSGSTARTSELFTEST'}{$apcupsdsettings{'MSGSTARTSELFTEST'}} = 'CHECKED';

$checked{'MSGENDSELFTEST'}{'off'} = '';
$checked{'MSGENDSELFTEST'}{'on'} = '';
$checked{'MSGENDSELFTEST'}{$apcupsdsettings{'MSGENDSELFTEST'}} = 'CHECKED';

$checked{'MSGBATTATTACH'}{'off'} = '';
$checked{'MSGBATTATTACH'}{'on'} = '';
$checked{'MSGBATTATTACH'}{$apcupsdsettings{'MSGBATTATTACH'}} = 'CHECKED';

$checked{'MSGBATTDETACH'}{'off'} = '';
$checked{'MSGBATTDETACH'}{'on'} = '';
$checked{'MSGBATTDETACH'}{$apcupsdsettings{'MSGBATTDETACH'}} = 'CHECKED';

&openpage('apcupsd', 1, '', 'services');

print <<END
<FORM METHOD='POST' action='$END{'SCRIPT_NAME'}'>

<script type="text/javascript">
function ffoxSelectUpdate(elmt)
{
    if(!document.all) elmt.style.cssText = elmt.options[elmt.selectedIndex].style.cssText;
}

</script>
END
;

&alertbox($errormessage);

&openbox('APCupsd:');

print <<END
<TABLE style='width: 100%; border: none; margin:1em auto 0 auto'>
<TR>
	<TD CLASS='base' style='width: 25%;'>$tr{'enabled'}</TD>
	<TD style='width:2%'><INPUT TYPE='checkbox' NAME='ENABLE' $checked{'ENABLE'}{'on'}></TD>
	<TD CLASS='base' style='width:30%'>$tr{'Standalone UPS'}:</TD>
	<TD><INPUT style='width:2%' TYPE='checkbox' NAME='STANDALONE' $checked{'STANDALONE'}{'on'}></TD>
</TR>
<TR>
	<TD CLASS='base'></td>
	<TD></td>
	<TD CLASS='base'>$tr{'Turn off UPS on shutdown'}:</TD>
	<TD><INPUT TYPE='checkbox' NAME='KILLPOWER' $checked{'KILLPOWER'}{'on'}></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox("$tr{'On Battery Configurationc'}");

print <<END
<TABLE style='width: 100%; border: none; margin:1em auto 0 auto'>
<TR>
	<TD CLASS='base' style='width: 37%;'>$tr{'Shutdown when remaining capacity less than'}:</TD>
	<TD style='width: 13%;'><INPUT TYPE='text' style='width: 3em;' NAME='BATTLEVEL' VALUE='$apcupsdsettings{'BATTLEVEL'}'> %</TD>
	<TD CLASS='base' style='width: 37%;'>$tr{'Shutdown when remaining time less than'}:</TD>
	<TD style='width: 13%;'><INPUT TYPE='text' style='width: 3em;' NAME='RTMIN' VALUE='$apcupsdsettings{'RTMIN'}'> $tr{'min.'}</TD>
</TR>
<TR>
	<TD CLASS='base' style='width: 37%;'>$tr{'Wait before responding to On Battery alert for'}:</TD>
	<TD style='width: 13%;'><INPUT TYPE='text' style='width: 3em;' NAME='BATTDELAY' VALUE='$apcupsdsettings{'BATTDELAY'}'> $tr{'sec.'}</TD>
	<TD CLASS='base' style='width: 37%;'>$tr{'Shutdown after on battery for'}:<span style='font-size:7pt;'> (0 $tr{'Disables'})</span></TD>
	<TD style='width: 13%;'><INPUT TYPE='text' style='width: 3em;' NAME='TO' VALUE='$apcupsdsettings{'TO'}'> $tr{'sec.'}</TD>
</TR>
<TR>
	<TD CLASS='base' style='width: 37%;'>$tr{'Deny Shell Login when on battery'}:</TD>
	<TD style='width: 13%;'>
	<SELECT NAME='NOLOGINTYPE'>
	<OPTION VALUE='0' $selected{'NOLOGINTYPE'}{'0'}>$tr{'Never'}
	<OPTION VALUE='1' $selected{'NOLOGINTYPE'}{'1'}>$tr{'Percent'}
	<OPTION VALUE='2' $selected{'NOLOGINTYPE'}{'2'}>$tr{'Minutes'}
	<OPTION VALUE='3' $selected{'NOLOGINTYPE'}{'3'}>$tr{'Always'}
	</SELECT></TD>
	<TD style='width: 37%;' CLASS='base'>$tr{'Send annoy message every'}:</TD>
	<TD style='width: 13%'><INPUT TYPE='text' style='width: 3em;' NAME='ANNOY' VALUE='$apcupsdsettings{'ANNOY'}'> $tr{'sec.'}</TD>
</TR>
</TABLE>
END
;

&closebox();

&openbox("$tr{'Communication Configurationc'}");

print <<END
<TABLE style='width: 100%; border: none; margin:1em auto 0 auto'>
<TR>
	<TD CLASS='base' style='width:20%'>$tr{'UPS Type'}:</TD>
	<TD style='width:10%'>
		<SELECT NAME='UPSMODE'>
		<OPTION VALUE='0' $selected{'UPSMODE'}{'0'}>SmartUPS (Serial)
		<OPTION VALUE='1' $selected{'UPSMODE'}{'1'}>SmartUPS (USB)
		<OPTION VALUE='2' $selected{'UPSMODE'}{'2'}>Modbus (Serial)
		<OPTION VALUE='3' $selected{'UPSMODE'}{'3'}>Modbus (USB)
		<OPTION VALUE='4' $selected{'UPSMODE'}{'4'}>Ethernet (Slave)
		<OPTION VALUE='5' $selected{'UPSMODE'}{'5'}>PCNET (TCP/IP)
		<OPTION VALUE='6' $selected{'UPSMODE'}{'6'}>940-0020B $tr{'Cable'}
		<OPTION VALUE='7' $selected{'UPSMODE'}{'7'}>940-0020C $tr{'Cable'}
		<OPTION VALUE='8' $selected{'UPSMODE'}{'8'}>940-0023A $tr{'Cable'}
		<OPTION VALUE='9' $selected{'UPSMODE'}{'9'}>940-0024B $tr{'Cable'}
		<OPTION VALUE='10' $selected{'UPSMODE'}{'10'}>940-0024C $tr{'Cable'}
		<OPTION VALUE='11' $selected{'UPSMODE'}{'11'}>940-0024G $tr{'Cable'}
		<OPTION VALUE='12' $selected{'UPSMODE'}{'12'}>940-0095A $tr{'Cable'}
		<OPTION VALUE='13' $selected{'UPSMODE'}{'13'}>940-0095B $tr{'Cable'}
		<OPTION VALUE='14' $selected{'UPSMODE'}{'14'}>940-0095C $tr{'Cable'}
		<OPTION VALUE='15' $selected{'UPSMODE'}{'15'}>940-0119A $tr{'Cable'}
		<OPTION VALUE='16' $selected{'UPSMODE'}{'16'}>940-0127A $tr{'Cable'}
		<OPTION VALUE='17' $selected{'UPSMODE'}{'17'}>940-0128A $tr{'Cable'}
		<OPTION VALUE='18' $selected{'UPSMODE'}{'18'}>940-1524C $tr{'Cable'}
		</SELECT>
	</TD>
	<TD CLASS='base'>$tr{'Master Address or Hostname'}:<BR><sup>$tr{'Append'} <span style="color:red">:&lt;$tr{'port'}&gt;</span> $tr{'if not default'} (3551)</sup></TD>
	<TD><INPUT TYPE='text'NAME='UPSIP' VALUE='$apcupsdsettings{'UPSIP'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'UPS Name (8 Char Max.)'}:</TD>
	<TD><INPUT TYPE='text' maxlength='8' NAME='UPSNAME' style='width:8em' VALUE='$apcupsdsettings{'UPSNAME'}'></TD>
	<TD CLASS='base' style='width:25%'>$tr{'Serial Port'}:</TD>
	<TD style='width:20%'><INPUT TYPE='text'NAME='UPSPORT' VALUE='$apcupsdsettings{'UPSPORT'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Polling Interval'}:</TD>
	<TD><INPUT TYPE='text' NAME='POLLTIME' style='width: 3em;' VALUE='$apcupsdsettings{'POLLTIME'}'></TD>
	<TD CLASS='base'>$tr{'PCNET username'}:</TD>
	<TD><INPUT TYPE='text'NAME='UPSUSER' VALUE='$apcupsdsettings{'UPSUSER'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Network server listen port'}:<span style='font-size:7pt;'><br />$tr{'Leave blank for default'}</span></TD>
	<TD><INPUT TYPE='text' maxlength='5' NAME='NISPORT' style='width: 3em;' VALUE='$apcupsdsettings{'NISPORT'}'></TD>
	<TD CLASS='base'>$tr{'PCNET password'}:</TD>
	<TD><INPUT TYPE='text'NAME='UPSAUTH' VALUE='$apcupsdsettings{'UPSAUTH'}'></TD>
</TR>
</TABLE>
END
;

&closebox();

print <<END;

<TABLE style='width: 100%; text-align:center; border: none; margin:1em auto'>
<TR>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save and restart'}'></TD>
	<TD style='text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'restart'}'></TD>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'stop'}'></TD>
</TR>
</TABLE>
END

&openbox("$tr{'Alerts Configurationc'}");

print <<END
<TABLE style='width: 100%; border: none; margin:1em auto 0 auto'>
<TR>
	<TD CLASS='base' style='width:20%'>$tr{'Enable Alerts'}:</TD>
	<TD style='width:15%'><INPUT TYPE='checkbox' NAME='ENABLEALERTS' $checked{'ENABLEALERTS'}{'on'}></TD>
	<TD CLASS='base' style='width:30%'></td>
	<TD style='width:20%'></td>
</TR>
<TR>
	<TD CLASS='base'></td>
	<TD></td>
	<TD CLASS='base'>$tr{'Send Alerts To'}:</TD>
	<TD><INPUT TYPE='text'NAME='ALERTADDR' VALUE='$apcupsdsettings{'ALERTADDR'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Mail Server'}:</TD>
	<TD ><INPUT TYPE='text'NAME='MAILSVR' VALUE='$apcupsdsettings{'MAILSVR'}'></TD>
	<TD CLASS='base'>$tr{'And To'}:</TD>
	<TD><INPUT TYPE='text'NAME='CC1ADDR' VALUE='$apcupsdsettings{'CC1ADDR'}'></TD>
</TR>
<TR>
	<TD CLASS='base'>$tr{'Send Alerts From'}:</TD>
	<TD><INPUT TYPE='text'NAME='FROMADDR' VALUE='$apcupsdsettings{'FROMADDR'}'></TD>
	<TD CLASS='base'>$tr{'SMS Email Address'}:</TD>
	<TD><INPUT TYPE='text'NAME='CC2ADDR' VALUE='$apcupsdsettings{'CC2ADDR'}'></TD>
</TR>
</TABLE>
END
;

&openbox("$tr{'UPS Events'}:");

print <<END
<TABLE style='width: 98%; border: none; margin:1em auto .5em auto'>
<TR>
	<TD style='text-align: right;'>$tr{'apc MSGCOMMFAILURE'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGCOMMFAILURE' $checked{'MSGCOMMFAILURE'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGPOWEROUT'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGPOWEROUT' $checked{'MSGPOWEROUT'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGONBATTERY'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGONBATTERY' $checked{'MSGONBATTERY'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGTIMEOUT'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGTIMEOUT' $checked{'MSGTIMEOUT'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGDOSHUTDOWN'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGDOSHUTDOWN' $checked{'MSGDOSHUTDOWN'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGBATTATTACH'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGBATTATTACH' $checked{'MSGBATTATTACH'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGSTARTSELFTEST'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGSTARTSELFTEST' $checked{'MSGSTARTSELFTEST'}{'on'}></TD>
</TR>
<TR>
	<TD style='text-align: right;'>$tr{'apc MSGCOMMOK'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGCOMMOK' $checked{'MSGCOMMOK'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGPOWERBACK'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGPOWERBACK' $checked{'MSGPOWERBACK'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGOFFBATTERY'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGOFFBATTERY' $checked{'MSGOFFBATTERY'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGLOADLIMIT'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGLOADLIMIT' $checked{'MSGLOADLIMIT'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGREMOTEDOWN'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGREMOTEDOWN' $checked{'MSGREMOTEDOWN'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGBATTDETACH'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGBATTDETACH' $checked{'MSGBATTDETACH'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGENDSELFTEST'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGENDSELFTEST' $checked{'MSGENDSELFTEST'}{'on'}></TD>
</TR>
<TR>
	<TD style='text-align: right;'></TD><TD></TD>
	<TD style='text-align: right;'>$tr{'apc MSGANNOY'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGANNOY' $checked{'MSGANNOY'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGEMERGENCY'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGEMERGENCY' $checked{'MSGEMERGENCY'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGRUNLIMIT'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGRUNLIMIT' $checked{'MSGRUNLIMIT'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGKILLPOWER'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGKILLPOWER' $checked{'MSGKILLPOWER'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGCHANGEME'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGCHANGEME' $checked{'MSGCHANGEME'}{'on'}></TD>
	<TD style='text-align: right;'>$tr{'apc MSGFAILING'}</TD><TD><INPUT TYPE='checkbox' NAME='MSGFAILING' $checked{'MSGFAILING'}{'on'}></TD>
</TR>
</TABLE>
END
;

&closebox();

&closebox();

&openbox("$tr{'Operation Mode'}:");

my $setcolor = '#000000';
if ( $selected{'OPMODE'}{'testing'} eq 'SELECTED' ) {
	$setcolor = '#b59d00';
}

if ( $selected{'OPMODE'}{'full'} eq 'SELECTED' ) {
	$setcolor = 'green';
}

print <<END
<p style='margin:1em 1em .25em 2em'>
  <span style="color:#b59d00">
    <b>$tr{'TESTING'}</B>
  </span>
  $tr{'will simulate the response to a power failure; it will not shutdown Smoothwall or the UPS'}.
</p>
<p style='margin:.25em 1em 0 2em'>
  <span style="color:green;">
    <B>$tr{'Full Operations'}</B>
  </span>
  $tr{'will shutdown Smoothwall in response to a power failure'}.
</p>
<p style='margin:.25em 1em 0 2em'>
  <i>$tr{'Do NOT select Full Operations Mode until you know that your configuration is OK'}</i>
</p>
<p style='margin:1em 1em 0 4em'>
  $tr{'Modec'}
    <SELECT NAME='OPMODE' style='color: $setcolor;' onchange='ffoxSelectUpdate(this);'>
      <OPTION VALUE='testing' $selected{'OPMODE'}{'testing'} style='color:#b59d00'>$tr{'TESTING'}</option>
      <OPTION VALUE='full' $selected{'OPMODE'}{'full'} style='color: green;'>$tr{'Full Operations'}</option>
    </SELECT>
</p>
END
;

&closebox();

print <<END;

<TABLE style='width: 100%; border: none; margin:1em auto'>
<TR>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save and restart'}'></TD>
	<TD style='text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'restart'}'></TD>
	<TD style='width: 33%; text-align: center;'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'stop'}'></TD>
</TR>
</TABLE>
</FORM>
END

&alertbox('add', 'add');

&closepage();
