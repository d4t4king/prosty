#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# SmoothInfo MOD v. 2.2b by Pascal Touch  (nanouk) on Smoothwall forums (2008).
# SmoothInstall compatible
# Packed using Steve McNeill's Mod Build System

# debugging
my $border = 0;

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw(:standard);

require "$swroot/smoothinfo/about.ph";

$MODDIR = "$swroot/smoothinfo/etc";

my (%smoothinfosettings, %checked);
my $version = $modinfo{'MOD_LONG_NAME'} . " v. " . $modinfo{'MOD_VERSION'};
my $filename = "$MODDIR/report.txt";
my $settingsfile = "$MODDIR/settings";
my @chains = ('All chains');
my @items = ('MEMORY', 'TOP', 'LOADEDMODULES', 'CPU', 'IRQs', 'DISKSPACE', 'CONNTYPE', 'ADAPTERS', 'NETCONF1', 'NETCONF2', 'ROUTE', 'CONNTRACKS', 'MODLIST', 'DHCPINFO', 'PORTFW', 'OUTGOING', 'XTACCESS', 'PINHOLES', 'CONFIG', 'DMESG', 'APACHE', 'MESSAGES', 'SERVICES', 'MODSERVICES', 'SQUID');
my @ASCII_items = ('SWITCH1', 'SWITCH2', 'SWITCH3', 'WAP1', 'WAP2', 'WAP3', 'WAP4', 'WAP5', 'WAP6', 'MODEM', 'ROUTER');
my $errormessage = '';

# Prepare @items for use as a JavaScript array
my $JSitems = "[\n";
foreach (@items){
  $JSitems .= "  '$_',\n";
}
chop($JSitems);chop($JSitems);
$JSitems .= "\n]";

unless (-e "$settingsfile") { system ("/bin/touch","$settingsfile"); }
unless (-e "$filename") { system ("/bin/touch","$filename"); }

my $success = message('smoothinfogetchains');

if (not defined $success) {
$errormessage .= $tr{'smoothd failure'}. "<br />\n";
}

open (FILE, "<$MODDIR/chains");
my @chains = (@chains,<FILE>);
chomp @chains;

# Prepare @chains for use as a JavaScript array
my $JSchains = "[\n";
foreach (@chains) {
  next if /All chains/;
  $JSchains .= "  '$_',\n";
}
chop($JSchains);chop($JSchains);
$JSchains .= "\n]";

$smoothinfosettings{'ACTION'} = '';

foreach (@items) {
  $smoothinfosettings{$_} = 'off';
}

foreach (@ASCII_items) {
  $smoothinfosettings{$_} = 'off';
}

$smoothinfosettings{'HEADORTAIL'} = 'TAIL';
$smoothinfosettings{'HEADORTAIL2'} = 'TAIL2';
$smoothinfosettings{'HEADORTAIL3'} ='TAIL3';
$smoothinfosettings{'LINES'} = '';
$smoothinfosettings{'LINES2'} = '';
$smoothinfosettings{'WRAP'} = '100';
$smoothinfosettings{'NOSELECT'} = 'off';

&getcgihash(\%smoothinfosettings);

foreach (@chains) {
  $checked{$_}{'off'} = '';
  $checked{$_}{'on'} = '';
  $checked{$_}{$smoothinfosettings{$_}} = 'CHECKED';
}

if ($smoothinfosettings{'ACTION'} eq $tr{'smoothinfo-generate'}) {
  # ERROR CHECKING
  my $msgOnce = 0;
  if ($smoothinfosettings{'LINES2'} eq '' &&
      $smoothinfosettings{'STRING2'} eq '' &&
      $smoothinfosettings{'APACHE'} eq 'on') {

    $msgOnce = 1;
    $errormessage .= $tr{'smoothinfo-define-number-of-lines'}. "<br />\n";
  }

  if ($smoothinfosettings{'LINES3'} eq '' &&
      $smoothinfosettings{'STRING3'} eq '' &&
      $smoothinfosettings{'MESSAGES'} eq 'on') {

    if ($msgOnce == 0)
    {
      $errormessage .= $tr{'smoothinfo-define-number-of-lines'}. "<br />\n";
    }
  }

  if ($smoothinfosettings{'SCREENSHOTS'} =~ /a href/i) {
    $errormessage .= $tr{'smoothinfo-bad-link'}. "<br />\n";
  }

  unlink ("$MODDIR/schematic");

  if ($smoothinfosettings{'SWITCH1'} eq 'on' ||
      $smoothinfosettings{'SWITCH2'} eq 'on' ||
      $smoothinfosettings{'SWITCH3'} eq 'on' ||
      $smoothinfosettings{'WAP1'} eq 'on' ||
      $smoothinfosettings{'WAP2'} eq 'on' ||
      $smoothinfosettings{'WAP3'} eq 'on' ||
      $smoothinfosettings{'WAP4'} eq 'on' ||
      $smoothinfosettings{'WAP5'} eq 'on' ||
      $smoothinfosettings{'WAP6'} eq 'on' ||
      $smoothinfosettings{'MODEM'} eq 'on' ||
      $smoothinfosettings{'ROUTER'} eq 'on') {

    system("/bin/touch $MODDIR/schematic");
  }

  unless ($smoothinfosettings{'MEMORY'} eq 'on' &&
          $smoothinfosettings{'LOADEDMODULES'} eq 'on' &&
          $smoothinfosettings{'TOP'} eq 'on' &&
          $smoothinfosettings{'CPU'} eq 'on' &&
          $smoothinfosettings{'DISKSPACE'} eq 'on' &&
          $smoothinfosettings{'CONNTYPE'} eq 'on' &&
          $smoothinfosettings{'ADAPTERS'} eq 'on' &&
          $smoothinfosettings{'NETCONF1'} eq 'on' &&
          $smoothinfosettings{'NETCONF2'} eq 'on' &&
          $smoothinfosettings{'DHCPLEASES'} eq 'on' &&
          $smoothinfosettings{'PORTFW'} eq 'on' &&
          $smoothinfosettings{'OUTGOING'} eq 'on' &&
          $smoothinfosettings{'XTACCESS'} eq 'on' &&
          $smoothinfosettings{'PINHOLES'} eq 'on' &&
          $smoothinfosettings{'SQUID'} eq 'on' &&
          $smoothinfosettings{'ROUTE'} eq 'on' &&
          $smoothinfosettings{'MODLIST'} eq 'on' &&
          $smoothinfosettings{'CONFIG'} eq 'on' &&
          $smoothinfosettings{'DMESG'} eq 'on' &&
          $smoothinfosettings{'APACHE'} eq 'on' &&
          $smoothinfosettings{'MESSAGES'} eq 'on') {

    $smoothinfosettings{'CHECKALL'} = 'off';
  }

  unless ($smoothinfosettings{'MEMORY'} eq 'on' or
          $smoothinfosettings{'LOADEDMODULES'} eq 'on' or
          $smoothinfosettings{'TOP'} eq 'on' or
          $smoothinfosettings{'CPU'} eq 'on' or
          $smoothinfosettings{'DISKSPACE'} eq 'on' or
          $smoothinfosettings{'CONNTYPE'} eq 'on' or
          $smoothinfosettings{'ADAPTERS'} eq 'on' or
          $smoothinfosettings{'NETCONF1'} eq 'on' or
          $smoothinfosettings{'NETCONF2'} eq 'on' or
          $smoothinfosettings{'DHCPLEASES'} eq 'on' or
          $smoothinfosettings{'PORTFW'} eq 'on' or
          $smoothinfosettings{'OUTGOING'} eq 'on' or
          $smoothinfosettings{'XTACCESS'} eq 'on' or
          $smoothinfosettings{'PINHOLES'} eq 'on' or
          $smoothinfosettings{'SQUID'} eq 'on' or
          $smoothinfosettings{'ROUTE'} eq 'on' or
          $smoothinfosettings{'MODLIST'} eq 'on' or
          $smoothinfosettings{'CONFIG'} eq 'on' or
          $smoothinfosettings{'DMESG'} eq 'on' or
          $smoothinfosettings{'APACHE'} eq 'on' or
          $smoothinfosettings{'MESSAGES'} eq 'on') {

    $smoothinfosettings{'NOSELECT'} = 'on';
    $errormessage .= "Nothing selected for report.<br />";
  }

  if ($smoothinfosettings{'CLIENTIP'} ne '') {
    open (TMP,">$MODDIR/clientip") || die 'Unable to open file';
    print TMP "$smoothinfosettings{'CLIENTIP'}";
    delete $smoothinfosettings{'CLIENTIP'};
    close (TMP);
  } else {
    unlink ("$MODDIR/clientip");
  }

  open (OUT, ">",\$smoothinfosettings{'CHAINS'});
  foreach (@chains) {
    if ($smoothinfosettings{$_} eq 'on') {
    print OUT "$_,";}
  }

  if ($smoothinfosettings{'OTHER'} ne '') {
    if ($smoothinfosettings{'SECTIONTITLE'} eq '') {
      $errormessage .= $tr{'smoothinfo-no-section-title'}. "<br />\n";
    }
    open (TMP,">$MODDIR/otherinfo") || die 'Unable to open file';
    print TMP "$smoothinfosettings{'SECTIONTITLE'}\n";
    print TMP "$smoothinfosettings{'OTHER'}";
    delete $smoothinfosettings{'SECTIONTITLE'};
    delete $smoothinfosettings{'OTHER'};
    close (TMP);
  } else {
    unlink ("$MODDIR/otherinfo");
  }

  unless ($errormessage) {
    delete ($smoothinfosettings{'data'});
    delete ($smoothinfosettings{'CHECKALL'});
    delete ($smoothinfosettings{'CHECKDEFAULT'});
    foreach (@chains) { delete ($smoothinfosettings{$_}) }
    &writehash("$settingsfile", \%smoothinfosettings);

   unless ($smoothinfosettings{'NOSELECT'} eq 'on') {
    my $success = message('smoothinfogenerate');

    if (not defined $success) {
      $errormessage .= $tr{'smoothd failure'}. "<br />\n";
    }
   }
  }

  if ($smoothinfosettings{'NOSELECT'} eq 'on') {
    open(FILE, ">/var/smoothwall/smoothinfo/etc/report.txt") or warn "Unable to open report file.";
    close FILE;
  }
}

&readhash("$settingsfile", \%smoothinfosettings);

undef $smoothinfosettings{'LINES'};
undef $smoothinfosettings{'LINES2'};
undef $smoothinfosettings{'LINES3'};
undef $smoothinfosettings{'STRING'};
undef $smoothinfosettings{'STRING2'};
undef $smoothinfosettings{'STRING3'};
undef $smoothinfosettings{'SCREENSHOTS'};

foreach (@items,@ASCII_items) {
  $checked{$_}{'off'} = '';
  $checked{$_}{'on'} = '';
  $checked{$_}{$smoothinfosettings{$_}} = 'CHECKED';
}

$checked{'EDIT'}{'off'} = '';
$checked{'EDIT'}{'on'} = '';
$checked{'EDIT'}{$smoothinfosettings{EDIT}} = 'CHECKED';

$selected{'HEADORTAIL'}{'HEAD'} = '';
$selected{'HEADORTAIL'}{'TAIL'} = '';
$selected{'HEADORTAIL'}{$smoothinfosettings{'HEADORTAIL'}} = 'CHECKED';

$selected{'HEADORTAIL2'}{'HEAD2'} = '';
$selected{'HEADORTAIL2'}{'TAIL2'} = '';
$selected{'HEADORTAIL2'}{$smoothinfosettings{'HEADORTAIL2'}} = 'CHECKED';

$selected{'HEADORTAIL3'}{'HEAD3'} = '';
$selected{'HEADORTAIL3'}{'TAIL3'} = '';
$selected{'HEADORTAIL3'}{$smoothinfosettings{'HEADORTAIL3'}} = 'CHECKED';

&showhttpheaders();

&openpage($tr{'smoothinfo-smoothinfo'}, 1, '', 'tools');

&openbigbox('100%', 'LEFT');
print <<END
<script language="javascript" type="text/javascript">

  function toggle(Id)
  {
    var el = document.getElementById(Id);
    if ( el.style.display != 'none' ) {
      el.style.display = 'none';
    } else {
      el.style.display = '';
    }
  }

	
  // Toggle the state of the arrow on the buttons.
  //   Down when settings are hidden.
  //   Up when they are visible.
  // Ugly I admit :-( ...

  function ToggleImage()
  {
    downUrl = "url('/ui/img/down.jpg')";
    upUrl = "url('/ui/img/up.jpg')";

    if ( document.getElementById('1').style.display == 'none' ) {
      document.myform.SCHEMATIC.style.backgroundImage = downUrl;
      document.myform.SCHEMATIC.style.backgroundPosition = '97% 50%';
      document.myform.SCHEMATIC.style.backgroundRepeat = 'no-repeat';
      document.myform.SCHEMATIC.style.backgroundColor = '#cdcdcd';
      document.myform.SCHEMATIC.style.textAlign = 'left';
    } else {
      document.myform.SCHEMATIC.style.backgroundImage = upUrl;
      document.myform.SCHEMATIC.style.backgroundPosition = '97% 50%';
      document.myform.SCHEMATIC.style.backgroundRepeat = 'no-repeat';
      document.myform.SCHEMATIC.style.backgroundColor = '#cdcdcd';
      document.myform.SCHEMATIC.style.textAlign = 'left';
    }
    if ( document.getElementById('2').style.display == 'none' ) {
      document.myform.CLIENT.style.backgroundImage = downUrl;
      document.myform.CLIENT.style.backgroundPosition = '97% 50%';
      document.myform.CLIENT.style.backgroundRepeat = 'no-repeat';
      document.myform.CLIENT.style.backgroundColor = '#cdcdcd';
      document.myform.CLIENT.style.textAlign = 'left';
    } else {
      document.myform.CLIENT.style.backgroundImage = upUrl;
      document.myform.CLIENT.style.backgroundPosition = '97% 50%';
      document.myform.CLIENT.style.backgroundRepeat = 'no-repeat';
      document.myform.CLIENT.style.backgroundColor = '#cdcdcd';
      document.myform.CLIENT.style.textAlign = 'left';
    }
    if ( document.getElementById('3').style.display == 'none' ) {
      document.myform.IPTABLES.style.backgroundImage = downUrl;
      document.myform.IPTABLES.style.backgroundPosition = '97% 50%';
      document.myform.IPTABLES.style.backgroundRepeat = 'no-repeat';
      document.myform.IPTABLES.style.backgroundColor = '#cdcdcd';
      document.myform.IPTABLES.style.textAlign = 'left';
    } else {
      document.myform.IPTABLES.style.backgroundImage = upUrl;
      document.myform.IPTABLES.style.backgroundPosition = '97% 50%';
      document.myform.IPTABLES.style.backgroundRepeat = 'no-repeat';
      document.myform.IPTABLES.style.backgroundColor = '#cdcdcd';
      document.myform.IPTABLES.style.textAlign = 'left';
    }
    if ( document.getElementById('4').style.display == 'none' ) {
      document.myform.EXTRA.style.backgroundImage = downUrl;
      document.myform.EXTRA.style.backgroundPosition = '97% 50%';
      document.myform.EXTRA.style.backgroundRepeat = 'no-repeat';
      document.myform.EXTRA.style.backgroundColor = '#cdcdcd';
      document.myform.EXTRA.style.textAlign = 'left';
    } else {
      document.myform.EXTRA.style.backgroundImage = upUrl;
      document.myform.EXTRA.style.backgroundPosition = '97% 50%';
      document.myform.EXTRA.style.backgroundRepeat = 'no-repeat';
      document.myform.EXTRA.style.backgroundColor = '#cdcdcd';
      document.myform.EXTRA.style.textAlign = 'left';
    }
  }

  window.onload = function() { ToggleImage(); }

  function CheckAll()
  {
    var netState;
    var checkBoxes = ${JSitems};

    // Get the state
    var newState = document.myform.CHECKALL.checked;

    // Now set 'em all
    for (var myCheck in checkBoxes) {
      document.myform[checkBoxes[myCheck]].checked = newState;
    }

    // And turn back on the defaults, if that one's checked
    if (newState==false && document.myform.CHECKDEFAULT.checked) {
      CheckDef();
    }
  }

  function CheckDef()
  {
    var checkBoxes = ['MEMORY', 'DISKSPACE', 'CONNTYPE', 'NETCONF1', 'NETCONF2',
                    'CONFIG', 'SERVICES'];

    // Get the state
    var newState = document.myform.CHECKDEFAULT.checked;

    // Now set 'em all
    for (var myCheck in checkBoxes) {
      document.myform[checkBoxes[myCheck]].checked = newState;
    }
  }

  function CheckAllChains()
  {
    var checkBoxes = ${JSchains};

    // Get the state
    var newState = document.myform.ALLCHAINS.checked;

    for (var myChain in checkBoxes) {
      document.myform[checkBoxes[myChain]].checked = newState;
    }
  }

  function SwitchOrWAP()
  {
    var newState;
    var dmf = document.myform;
    // Schematic labels shortcuts
    var schLbls = {};
    schLbls.WAP1lbl = document.getElementById('WAP1lbl');
    schLbls.WAP2lbl = document.getElementById('WAP2lbl');
    schLbls.WAP3lbl = document.getElementById('WAP3lbl');
    schLbls.WAP4lbl = document.getElementById('WAP4lbl');
    schLbls.WAP5lbl = document.getElementById('WAP5lbl');
    schLbls.WAP6lbl = document.getElementById('WAP6lbl');
    schLbls.SWITCH1lbl = document.getElementById('SWITCH1lbl');
    schLbls.SWITCH2lbl = document.getElementById('SWITCH2lbl');
    schLbls.SWITCH3lbl = document.getElementById('SWITCH3lbl');

    // GREEN
    if (!(dmf.SWITCH1.checked) && !(dmf.WAP4.checked)) {
      dmf.SWITCH1.disabled = false;
      schLbls.SWITCH1lbl.style.color='#000000';
      dmf.WAP1.disabled = true;
      schLbls.WAP1lbl.style.color='#888888';
      dmf.WAP1.checked = false;
      dmf.WAP4.disabled = false;
      schLbls.WAP4lbl.style.color='#000000';
    } else if (dmf.SWITCH1.checked) {
      dmf.WAP1.disabled = false;
      schLbls.WAP1lbl.style.color='#000000';
      dmf.WAP4.disabled = true;
      schLbls.WAP4lbl.style.color='#888888';
    } else if (dmf.WAP4.checked) {
      dmf.SWITCH1.disabled = true;
      schLbls.SWITCH1lbl.style.color='#888888';
      dmf.WAP1.disabled = true;
      schLbls.WAP1lbl.style.color='#888888';
      dmf.WAP1.checked = false;
    }

    // ORANGE
    if (!(dmf.SWITCH2.checked) && !(dmf.WAP3.checked)) {
      dmf.SWITCH2.disabled = false;
      schLbls.SWITCH2lbl.style.color='#000000';
      dmf.WAP2.disabled = true;
      schLbls.WAP2lbl.style.color='#888888';
      dmf.WAP2.checked = false;
      dmf.WAP3.disabled = false;
      schLbls.WAP3lbl.style.color='#000000';
    } else if (dmf.SWITCH2.checked) {
      dmf.WAP2.disabled = false;
      schLbls.WAP2lbl.style.color='#000000';
      dmf.WAP3.disabled = true;
      schLbls.WAP3lbl.style.color='#888888';
    } else if (dmf.WAP3.checked) {
      dmf.SWITCH2.disabled = true;
      schLbls.SWITCH2lbl.style.color='#888888';
      dmf.WAP2.disabled = true;
      schLbls.WAP2lbl.style.color='#888888';
      dmf.WAP2.checked = false;
    }

    // PURPLE
    if (!(dmf.SWITCH3.checked) && !(dmf.WAP5.checked)) {
      dmf.SWITCH3.disabled = false;
      schLbls.SWITCH3lbl.style.color='#000000';
      dmf.WAP6.disabled = true;
      schLbls.WAP6lbl.style.color='#888888';
      dmf.WAP6.checked = false;
      dmf.WAP5.disabled = false;
      schLbls.WAP5lbl.style.color='#000000';
    } else if (dmf.SWITCH3.checked) {
      dmf.WAP6.disabled = false;
      schLbls.WAP6lbl.style.color='#000000';
      dmf.WAP5.disabled = true;
      schLbls.WAP5lbl.style.color='#888888';
    } else if (dmf.WAP5.checked) {
      dmf.SWITCH3.disabled = true;
      schLbls.SWITCH3lbl.style.color='#888888';
      dmf.WAP6.disabled = true;
      schLbls.WAP6lbl.style.color='#888888';
      dmf.WAP6.checked = false;
    }
  }

  function selectAll(field)
  {
    var tempval=eval("document."+field);

    tempval.focus();
    tempval.select();
  }
</script>

END
;

&alertbox($errormessage);

print <<END
<FORM METHOD='POST' NAME='myform'>

<DIV ALIGN='CENTER'>
<BR>
<table style='width: 95%; border:solid 1px; border-color:orange; background-color:#f9f0c7; margin:0px; padding:4px;'>
  <TR>
    <TD style='font-size:120%;'>$tr{'smoothinfo-caution'}</TD>
  </TR>
</TABLE>
</DIV>
END
;

&openbox("Prepare Report");

print<<END;
    <p class='base' style='vertical-align:middle; margin:1em 1em 0 1em; padding:4px;'>
      $tr{'smoothinfo-checkdefault'}
      <input type='checkbox' name='CHECKDEFAULT' $checked{'CHECKDEFAULT'}{'on'}
             style='display:inline-block; vertical-align:middle; margin:0'
             onClick='javaScript:CheckDef();'>
      &nbsp;&nbsp;&nbsp;&nbsp;
      $tr{'smoothinfo-checkall'}
      <input type='checkbox' name='CHECKALL' $checked{'CHECKALL'}{'on'}
             style='display:inline-block; vertical-align:middle; margin:0'
             onClick='javaScript:CheckAll();'>
      <span style='margin-left:10em'>
        $tr{'smoothinfo-wrap-prefix'}
        <input type='text' name='WRAP' value='$smoothinfosettings{'WRAP'}'
               size='5' style='display:inline-block;vertical-align:middle;margin:0'>
        $tr{'smoothinfo-wrap-suffix'}
      <span>
    </p>
END

&openbox($tr{'smoothinfo-include'});

print <<END;
<TABLE WIDTH='90%' align='center' style='margin-top:1em'>
  <TR>
    <th style='width:33%; padding:2px' colspan=2>Smoothwall</th>
    <th style='width:33%; padding:2px' colspan=2>Linux</th>
    <th style='width:33%; padding:2px' colspan=2>Mods</th>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-config-tip'}'>$tr{'smoothinfo-config'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='CONFIG' VALUE='on' $checked{'CONFIG'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-modules-tip'}'>$tr{'smoothinfo-modules'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='LOADEDMODULES' $checked{'LOADEDMODULES'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base' TITLE="$tr{'smoothinfo-mod-services-status-tip'}">$tr{'smoothinfo-mod-services-status'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='MODSERVICES' $checked{'MODSERVICES'}{'on'}></TD>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-services-status-tip'}'>$tr{'smoothinfo-services-status'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='SERVICES' $checked{'SERVICES'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base' TITLE="$tr{'smoothinfo-top-tip'}">$tr{'smoothinfo-top'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='TOP' $checked{'TOP'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-mods-tip'}'>$tr{'smoothinfo-installed-mods'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='MODLIST' $checked{'MODLIST'}{'on'}></TD>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-connection-tip'}'>$tr{'smoothinfo-connection'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='CONNTYPE' VALUE='on' $checked{'CONNTYPE'}{'on'}></TD>
    <td></td>
    <td></td>
  </TR>
  <TR>
    <th style='padding:2px' colspan=6>Networking</th>
  </TR>
  <TR>
    <TD  WIDTH='30%' CLASS='base' TITLE="$tr{'smoothinfo-net settings-tip'}">$tr{'smoothinfo-net settings'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='NETCONF2' $checked{'NETCONF2'}{'on'}></TD>
    <TD  WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-dhcpinfo-tip'}'>$tr{'smoothinfo-dhcpinfo'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='DHCPINFO' $checked{'DHCPINFO'}{'on'}></TD>
    <TD  WIDTH='30%' CLASS='base'>External access:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='XTACCESS' $checked{'XTACCESS'}{'on'}></TD>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-ifconfig-tip'}'>$tr{'smoothinfo-ifconfig'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='NETCONF1' VALUE='on' $checked{'NETCONF1'}{'on'}></TD>
    <TD  WIDTH='30%' CLASS='base'>$tr{'smoothinfo-portfw'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='PORTFW' $checked{'PORTFW'}{'on'}></TD>
  </TR>
  <TR>
    <TD  WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-routes-tip'}'>$tr{'smoothinfo-routes'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='ROUTE' $checked{'ROUTE'}{'on'}></TD>
    <TD  WIDTH='30%' CLASS='base'>Outgoing exceptions:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='OUTGOING' $checked{'OUTGOING'}{'on'}></TD>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-conntracks-tip'}'>$tr{'smoothinfo-conntracks'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='CONNTRACKS' $checked{'CONNTRACKS'}{'on'}></TD>
    <TD  WIDTH='30%' CLASS='base'>Internal pinholes:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='PINHOLES' $checked{'PINHOLES'}{'on'}></TD>  </TR>
  <TR>
    <th style='width:67%; padding:2px' colspan=4>Hardware</th><th style='width:33%; padding:2px' colspan=2>Services</th>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base'>$tr{'smoothinfo-cpu'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' NAME='CPU' $checked{'CPU'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-memory-tip'}'>$tr{'smoothinfo-memory'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='MEMORY' $checked{'MEMORY'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base'>Web proxy:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='SQUID' $checked{'SQUID'}{'on'}></TD>
  </TR>
  <TR>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-irqs-tip'}'>$tr{'smoothinfo-irqs'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='IRQs' $checked{'IRQs'}{'on'}></TD>
    <TD WIDTH='30%' CLASS='base'>$tr{'smoothinfo-diskspace'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='DISKSPACE' $checked{'DISKSPACE'}{'on'}></TD>
  </TR>
  <TR>
    <td></td>
    <td></td>
    <TD WIDTH='30%' CLASS='base' TITLE='$tr{'smoothinfo-adapters-tip'}'>$tr{'smoothinfo-adapters'}:</TD>
    <TD width='3%'><INPUT TYPE='checkbox' ALIGN='LEFT' NAME='ADAPTERS' $checked{'ADAPTERS'}{'on'}></TD>
  </TR>
  <TR>
  </TR>
</TABLE>
END

&closebox();

&openbox("Include logs:&nbsp;&nbsp;&nbsp;
    <a href='#'><img src='/ui/img/help.gif' alt='?'
                     title='$tr{'smoothinfo-log-help'}'
                     valign='top'
                     onclick=\"javascript:toggle('help'); return false;\">
    </a>");

print <<END;
<TABLE WIDTH='100%' border='$border' cellpadding='0' cellspacing='0' style='margin-top:1em'>
  <TR>
    <TD class='tightbase' TITLE='$tr{'smoothinfo-dmesg-tip'}'>$tr{'smoothinfo-dmesg'}</TD>
    <TD><INPUT TYPE='checkbox' NAME='DMESG' $checked{'DMESG'}{'on'}></TD>
    <TD class='tightbase'> $tr{'smoothinfo-head'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL' VALUE='HEAD' $selected{'HEADORTAIL'}{'HEAD'}></TD>
    <TD class='tightbase'>$tr{'smoothinfo-tail'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL' VALUE='TAIL' $selected{'HEADORTAIL'}{'TAIL'}></TD>
    <TD class='tightbase'>
      <IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-lines'}
    </TD>
    <TD><INPUT TYPE='text' NAME='LINES' VALUE='$smoothinfosettings{'LINES'}'
               size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></TD>
    <TD class='tightbase'>
      <IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-search'}
    </TD>
    <TD><INPUT TYPE='text' NAME='STRING' VALUE='$smoothinfosettings{'STRING'}' size='10'></TD>
    <TD class='tightbase'>$tr{'smoothinfo-ignore-case'}</TD>
    <TD><INPUT TYPE='checkbox' NAME='IGNORECASE' $checked{'IGNORECASE'}{'on'}></TD>
  </TR>
  <TR style='background:#ecece8'>
    <TD class='tightbase' TITLE='$tr{'smoothinfo-apache-error-tip'}'>$tr{'smoothinfo-apache-error'}</TD>
        <TD><INPUT TYPE='checkbox' NAME='APACHE' $checked{'APACHE'}{'on'}></TD>
    <TD class='tightbase'>$tr{'smoothinfo-head'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL2' VALUE='HEAD2' $selected{'HEADORTAIL2'}{'HEAD2'}></TD>
        <TD class='tightbase'>$tr{'smoothinfo-tail'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL2' VALUE='TAIL2' $selected{'HEADORTAIL2'}{'TAIL2'}></TD>
    <TD class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-lines'}</TD>
    <TD><INPUT TYPE='text' NAME='LINES2' VALUE='$smoothinfosettings{'LINES2'}' size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></TD>
    <TD class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-search'}</TD>
    <TD><INPUT TYPE='text' NAME='STRING2' VALUE='$smoothinfosettings{'STRING2'}' size='10'></TD>
    <TD class='tightbase'>$tr{'smoothinfo-ignore-case'}</TD>
    <TD><INPUT TYPE='checkbox' NAME='IGNORECASE2' $checked{'IGNORECASE2'}{'on'}></TD>
  </TR>
  <TR>
    <TD class='tightbase' TITLE='$tr{'smoothinfo-system-tip'}'>$tr{'smoothinfo-system'}</TD>
        <TD><INPUT TYPE='checkbox' NAME='MESSAGES' $checked{'MESSAGES'}{'on'}></TD>
    <TD class='tightbase'>$tr{'smoothinfo-head'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL3' VALUE='HEAD3' $selected{'HEADORTAIL3'}{'HEAD3'}></TD>
        <TD class='tightbase'>$tr{'smoothinfo-tail'}</TD>
    <TD><INPUT TYPE='radio' NAME='HEADORTAIL3' VALUE='TAIL3' $selected{'HEADORTAIL3'}{'TAIL3'}></TD>
    <TD class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-lines'}</TD>
    <TD><INPUT TYPE='text' NAME='LINES3' VALUE='$smoothinfosettings{'LINES3'}' size='2' TITLE='$tr{'smoothinfo-apache-lines-tip'}'></TD>
    <TD class='tightbase'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'><IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>&nbsp;$tr{'smoothinfo-search'}</TD>
    <TD><INPUT TYPE='text' NAME='STRING3' VALUE='$smoothinfosettings{'STRING3'}' size='10'></TD>
    <TD class='tightbase'>$tr{'smoothinfo-ignore-case'}</TD>
    <TD><INPUT TYPE='checkbox' NAME='IGNORECASE3' $checked{'IGNORECASE3'}{'on'}></TD>
  </TR>
<TR>
  <TD colspan='4' >
    <p CLASS='base' style='margin:1em 0 0 1em'>
    <IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>
      &nbsp;$tr{'this field may be blank'}
    </p>
  </TD>
</TR>
<TR>
  <TD colspan='4' style='margin-left:10pt'>
    <p CLASS='base' style='margin:.25em 0 0 1em'>
    <IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>
    <IMG SRC='/ui/img/blob.gif' ALT='*' VALIGN='top'>
      &nbsp;$tr{'smoothinfo-both-fields-cannot-be-blank'}
    </p>
  </td>
</tr>
</TABLE>
END

print <<END;
<DIV ALIGN='CENTER' Id='help' style='display: none'>
<table style='width: 99%; border:dotted 1px; background-color:#ffee88; margin:0px; padding:4px;'>
<TR>
  <TD width='15%' style='font-size:100%; font-style:italic;'>$tr{'smoothinfo-dmesg'}</TD>
  <TD style='font-size:100%;'>$tr{'smoothinfo-dmesg-help'}</TD>
</TR>
<TR>
  <TD width='15%' style='font-size:100%; font-style:italic;'>$tr{'smoothinfo-apache-error'}</TD>
  <TD style='font-size:100%;'>$tr{'smoothinfo-apache-error-help1'}</TD>
</TR>
<TR>
  <TD width='15%'>&nbsp;</TD>
  <TD style='font-size:100%;'>$tr{'smoothinfo-apache-error-help2'}</TD>
</TR>
<TR>
  <TD width='15%' style='font-size:100%; font-style:italic;'>$tr{'smoothinfo-system'}</TD>
  <TD style='font-size:100%;'>$tr{'smoothinfo-system-log-help'}</TD>
</TR>
</TABLE>
</DIV>
END
;

&closebox();

&openbox("Include screenshots:");

print <<END;
  <p style='margin:1em 0 0 1em'>
    Link(s) to screenshot(s):<br />
    <input type='text' name='SCREENSHOTS' value='$smoothinfosettings{'SCREENSHOTS'}'
           style='margin:.2em 0 0 2em'
           size='80' TITLE='$tr{'smoothinfo-screenshots-tip'}'>
  </p>
END

&closebox();

&openbox("Other information:");

print<<END;
<div style='text-align:center; margin:1em 1em .2em 1em'>
  <input type='button' name='SCHEMATIC' id='schematic'
         value='$tr{'smoothinfo-schematic'}&nbsp;&nbsp;&nbsp;&nbsp;'
         style='margin:0 .1em'
         onClick="javascript:toggle('1');javascript:ToggleImage();" />
  <input type='button' name='CLIENT' id='client'
         value='$tr{'smoothinfo-clientinfo'}&nbsp;&nbsp;&nbsp;&nbsp;'
         style='margin:0 .1em'
         onClick="javascript:toggle('2');javascript:ToggleImage();" />
  <input type='button' name='IPTABLES' id='iptables'
         value='$tr{'smoothinfo-iptables'}&nbsp;&nbsp;&nbsp;&nbsp;'
         style='margin:0 .1em'
         onClick="javascript:toggle('3');javascript:ToggleImage();" />
  <input type='button' name='EXTRA' id='other'
         value='$tr{'smoothinfo-other'}&nbsp;&nbsp;&nbsp;&nbsp;'
         style='margin:0 .1em'
         onClick="javascript:toggle('4');javascript:ToggleImage();" />
</div>
END
;

print <<END
<DIV Id='1' style="display:none;">
END
;
&openbox();

#RED '#ffaaaa'; }
#"Green") {$bgcolor = "#bbffbb";}
#"Purple") {$bgcolor = "#ddaaff";}
#"Orange") {$bgcolor = "#ffaa77";}

print <<END
<b>$tr{'smoothinfo-shematic-items'}</b>

<table width='inherit' style='margin:1em 2em 0 2em'>
  <tr>
    <td rowspan='7' style='margin:0; width:8.6em; text-align:center; background-color:white; border:solid black .2em'>
      <b>SMOOTHWALL</b>
    </td>

    <td style='margin:0; padding:.3em; height:3em; background-color:#bbffbb; vertical-align:middle; border: solid black .2em'>
      <div style='vertical-align:middle; text-align:left; margin:0'>
        <span style='color:#bbffbb'><i>(GREEN)</i> &harr;</span>
        <input type='checkbox'
               name='WAP4' $checked{'WAP4'}{'on'}
               onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP4lbl'>WAP</span></b> &harr; W/Lan<br />
        <i>(GREEN)</i> &harr;
        <input type='checkbox'
               name='SWITCH1' $checked{'SWITCH1'}{'on'}
               onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH1lbl'>Switch</span></b> &harr; LAN
        &harr;
        <input type='checkbox'
               name='WAP1' $checked{'WAP1'}{'on'}
               onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP1lbl'>WAP</span></b> &harr; W/Lan
      </div>
    </td>
  </tr>

  <tr><td style='font-size:18pt'>&nbsp;</td></tr>

  <tr>
    <td style='margin:0; padding:.3em; height:3em; background-color:#ffaa77; vertical-align:middle; border: solid black .2em'>
      <div style='vertical-align:middle; text-align:left; margin:0'>
      <span style='color:#ffaa77'><i>(ORANGE)</i> &harr;</span>
      <input type='checkbox'
             name='WAP3' $checked{'WAP3'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP3lbl'>WAP</span></b> &harr; W/Lan<br />
      <i>(ORANGE)</i> &harr;
      <input type='checkbox'
             name='SWITCH2' $checked{'SWITCH2'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH2lbl'>Switch</span></b> &harr; LAN &harr;
      <input type='checkbox'
             name='WAP2' $checked{'WAP2'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP2lbl'>WAP</span></b> &harr; W/LAN
      </div>
    </td>
  </tr>

  <tr><td style='font-size:18pt'>&nbsp;</td></tr>

  <tr>
    <td style='margin:0; padding:.3em; height:3em; background-color:#ddaaff; vertical-align:middle; border: solid black .2em'>
      <div style='vertical-align:middle; text-align:left; margin:0'>
      <span style='color:#ddaaff'><i>(PURPLE)</i> &harr;</span>
      <input type='checkbox'
             name='WAP5' $checked{'WAP5'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP5lbl'>WAP</span></b> &harr; W/Lan<br />
      <i>(PURPLE)</i> &harr;
      <input type='checkbox'
             name='SWITCH3' $checked{'SWITCH3'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='SWITCH3lbl'>Switch</span></b> &harr; LAN &harr;
      <input type='checkbox'
             name='WAP6' $checked{'WAP6'}{'on'}
             onClick='javaScript:SwitchOrWAP();' /><b><span id='WAP6lbl'>WAP</span></b> &harr; W/LAN
      </div>
    </td>
  </tr>

  <tr><td style='font-size:18pt'>&nbsp;</td></tr>

  <tr>
    <td style='margin:0; padding:.3em; height:3em; background-color:#ffaaaa; vertical-align:middle; border: solid black .2em'>
      <div style='vertical-align:middle; text-align:left; margin:0'>
      <i>(RED)</i> &harr;
      <input type='checkbox'
             name='ROUTER' $checked{'ROUTER'}{'on'}><b>Router</b> &harr; LAN &harr;
      <input type='checkbox'
             name='MODEM' $checked{'MODEM'}{'on'}><b>Modem</b> &harr; Internet
      </div>
    </td>
  </tr>
</table>
<script language="javascript" type="text/javascript">
  SwitchOrWAP();
</script>
END
;
&closebox();
print <<END
</DIV>
END
;

print <<END
<DIV Id='2' style="display:none;">
END
;
&openbox();
print <<END
<b>$tr{'smoothinfo-clientIP'}</b>
<BR><BR><FONT COLOR='red'><CENTER>$tr{'smoothinfo-warn'}</CENTER></FONT>
<TABLE WIDTH='100%'>
<TR>
 <TD ALIGN='CENTER' WIDTH='50%'><TEXTAREA NAME='CLIENTIP' ROWS='10' COLS='70' WRAP='off' TITLE='$tr{'smoothinfo-clientIP-tip'}'>
</TEXTAREA></TD>
</TR>
</TABLE>
END
;
&closebox();
print <<END
</DIV>
END
;

print <<END
<DIV Id='4' style="display:none;">
END
;
&openbox("$tr{'smoothinfo-other'}:");
print <<END
<TABLE WIDTH='100%'>
<TR>
  <TD WIDTH='9%'><b>$tr{'smoothinfo-other-title'}</b></TD><TD WIDTH='91%'><INPUT TYPE='text' NAME='SECTIONTITLE' Id='sectiontitle' VALUE='$smoothinfosettings{'SECTIONTITLE'}'  @{[jsvalidregex('sectiontitle','^[a-zA-Z0-9-_., ]+$')]} size='20'>&nbsp;<i>(required)</i></TD>
</TR>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
  <TD ALIGN='CENTER' WIDTH='50%'><TEXTAREA NAME='OTHER' ROWS='10' COLS='70' WRAP='off' TITLE='$tr{'smoothinfo-other-tip'}'></TEXTAREA></TD>
</TR>
</TABLE>
END
;
&closebox();
print <<END
</DIV>
END
;

print <<END
<DIV Id='3' style="display:none;">
END
;
&openbox($tr{'smoothinfo-known-chains'});
print "$tr{'smoothinfo-chains'}";
my @rows = ();
  print "<table style='width: 100%;'>";
  $id = -1;
  foreach (@chains)
  {
    $id++;
    if (/All chains/) {
      push @rows, qq[<td style='width: 15%; color: red; font-weight: bold;'>$_</td><td style='width: 20%;'><INPUT TYPE='checkbox' NAME='ALLCHAINS' \$checked{'ALLCHAINS'}{'on'} onClick='javaScript:CheckAllChains();' /></td>\n];
    } else {
      push @rows, qq[<td style='width: 15%;'>$_</td><td style='width: 20%;'><INPUT TYPE='checkbox' NAME='$_' \$checked{'$_'}{'on'}></td>\n];
    }
  }
  # 3colums
  for(my $id = 0; $id <= $#rows; $id += 3)
  {
    $rows[$id+1] = '&nbsp;' unless defined $rows[$id+1];
    $rows[$id+2] = '&nbsp;' unless defined $rows[$id+2];
    print "<tr>" . $rows[$id] . $rows[$id+1] . $rows[$id+2] . "</tr>\n";
  }
  print "</table>";
&closebox();
print <<END
</DIV>
END
;

&closebox();

&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
 <TR>
 <TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'smoothinfo-generate'}' style="height:25px;background-color:#fdb445;font: bold 12px Arial;" onClick="if(confirm('$tr{'smoothinfo-confirm'}')) {return true;} return false;"></TD>
 </TR>
</TABLE>
</DIV>
END
;

if ($smoothinfosettings{'EDIT'} eq 'on')
{
$textarea = "<TD ALIGN='CENTER' WIDTH='50%'><TEXTAREA NAME='data' ROWS='30' COLS='85' WRAP='off'>";
$bbcodehelp = "<TD ALIGN='RIGHT'><sup><small><i><A HREF='http://community.smoothwall.org/forum/faq.php?mode=bbcode' onclick=\"window.open(this.href,'popup','height=600 ,width=800, scrollbars=yes, left=150,top=150,screenX=150,screenY=150');return false;\" TITLE='$tr{'smoothinfo-connected'}'>$tr{'smoothinfo-bbcode'}&nbsp;</a></i></small></sup></TD>";
}
else
{
$textarea = "<TD ALIGN='CENTER' WIDTH='50%'><TEXTAREA NAME='data' ROWS='30' COLS='85' WRAP='off' READONLY='yes' TITLE='$tr{'smoothinfo-report-tip'}' onclick='this.select();' style='background:#ecece8;'>";
$bbcodehelp = '';
}

&openbox($tr{'smoothinfo-report'});
print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
  <TD CLASS='base' ALIGN='LEFT' TITLE='$tr{'smoothinfo-edit-tip'}'>$tr{'smoothinfo-edit'}&nbsp;<INPUT TYPE='checkbox' NAME='EDIT' $checked{'EDIT'}{'on'}></TD>
$bbcodehelp
</TR>
</TABLE>
</DIV>
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
  <TD ALIGN='CENTER'><a href="javascript:selectAll('myform.data')" style='font-size:120%; color:red; font-weight:bold;' TITLE='$tr{'smoothinfo-selectall-tip'}'>Select All</a></TD>
</TR>
</TABLE>
</DIV>
<TABLE WIDTH='100%'>
<TR>
$textarea
END
;
open (REPORT, "<$filename") or die "unable to open report";
while (<REPORT>) {
chomp;
print "$_\n";
}
close REPORT;
print <<END
</TEXTAREA></TD>
</TR>
</TABLE>
<BR>
END
;
&closebox();

print "</FORM>\n";

&closebigbox();

&closepage();
