#!/usr/bin/perl
# Perl script to gather the info requested  in the UI.
# smoothinfo.pl v. 2.2b (c) Pascal Touch (nanouk) on Smoothwall forums
# smoothinfo.pl v. 2.2c © Neal Murphy (fest3er) on Smoothwall forums;
#     Roadster & SWE3.1 integration and tweaks
# Improved mods sorting routine and the list is now numbered.
# New smoothd module to make SmoothInfo more "compliant".
# Packed using Steve McNeill's Mod Build System.
# Detects mods packed with the Mod Build System.
# Added detection of several additional "non-standard" mods.
# Added IRQ's and Conntracks sections.
# Corrected "double webproxy section" bug.
# Corrected "missing opening info tag square bracket" bug in the screenshot section.
# Added verbosity to the display of firewall rules.

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use File::Find;
use File::Basename;
use Net::Netmask;

# Data::Dumper is great for displaying arrays and hashes.
#use Data::Dumper;


$SIdir="${swroot}/smoothinfo";
require "${SIdir}/about.ph";

my (%productdata, %pppsettings, %modemsettings, %netsettings, %smoothinfosettings, %defseclevelsettings, %green_dhcpsettings, %purple_dhcpsettings, %imsettings, %p3scansettings, %sipproxysettings, %proxysettings, %filteringsettings, %SSHsettings);

&readhash("${swroot}/main/productdata", \%productdata);
&readhash("${swroot}/ppp/settings", \%pppsettings);
&readhash("${swroot}/modem/settings", \%modemsettings);
&readhash("${SIdir}/etc/settings", \%smoothinfosettings);
&readhash("${swroot}/ethernet/settings", \%netsettings);
&readhash("${swroot}/main/settings", \%defseclevelsettings);
# stock services
&readhash("${swroot}/im/settings", \%imsettings);
&readhash("${swroot}/p3scan/settings", \%p3scansettings);
&readhash("${swroot}/sipproxy/settings", \%sipproxysettings);
&readhash("${swroot}/proxy/settings", \%proxysettings);
&readhash("${swroot}/snort/settings", \%snortsettings);
&readhash("${swroot}/remote/settings", \%SSHsettings);
# mod services
if (-e "${swroot}/filtering/settings") {
  &readhash("${swroot}/filtering/settings", \%filteringsettings);
}

unless (-z "${swroot}/dhcp/settings-green") {
  &readhash("${swroot}/dhcp/settings-green", \%green_dhcpsettings); }
unless (-z "${swroot}/dhcp/settings-purple") {
  &readhash("${swroot}/dhcp/settings-purple", \%purple_dhcpsettings);
}

my $outputfile = "${SIdir}/etc/report.txt";

# MEMORY
my $memory = `/usr/bin/free -ot`;
chomp ($memory);

# CPU
open (CPU,"</proc/cpuinfo") || die "Unable to open $!";
my $cpu = (grep /model\sname/, <CPU>)[0];
$cpu =~ s/model name(\t+|s+): //;
chomp ($cpu);
open (CPU,"</proc/cpuinfo") || die "Unable to open $!";
my $frequency = (grep /cpu\sMHz/, <CPU>)[0];
$frequency =~ s/cpu MHz(\t+|s+): //;
chomp ($frequency);
open (CPU,"</proc/cpuinfo") || die "Unable to open $!";
my $cache = (grep /cache\ssize/, <CPU>)[0];
$cache =~ s/cache size(\t+|s+): //;
chomp ($cache);
my $cpuCores = `/bin/cat /proc/cpuinfo | /bin/egrep "^processor[ 	]*:" | /usr/bin/wc -l`;
chomp $cpuCores;

#IRQ's
opendir (DIR, "/proc/irq");
my @IRQs = '';
my $warning = '';
my @files = sort { lc($a) > lc($b) } (grep { /^\d+$/ } readdir DIR);
foreach (@files) {
  opendir (IRQS, "/proc/irq/$_");
  $device = "";
  foreach (readdir IRQS) {
    next if /\./;
    next if /\.\./;
    next if /affinity_hint/;
    next if /node/;
    next if /smp_affinity/;
    next if /spurious/;
    print "$_\n";
    $device = "$_, ";
  }
  closedir (IRQS);
  chop ($device); chop ($device);
  if ($device) {
    if ($device =~ /,/) {
      push (@IRQs, "IRQ $_ used by $device\t<==\n");
      $warning = "There seems to be at least one shared IRQ in your system!\n";
    } else {
      push (@IRQs, "IRQ $_ used by $device\n");
    }
  }
}
closedir (DIR);

#CONNTRACKS
$conntracks = `/bin/cat /proc/net/ip_conntrack|/usr/bin/wc -l`;
$conntracks .= "\n";
$conntracks .= `/bin/cat /proc/net/ip_conntrack`;
chomp ($conntracks);

# DISKSPACE
my $diskspace = &pipeopen( '/bin/df', '-h' );
chomp $diskspace;

# ETHERNET ADAPTERS
open (LSPCI, "-|") or exec ("/usr/sbin/lspci");
my @ethernet_adapters = '';
foreach (<LSPCI>){
  if (/Ethernet/){
    $_ =~ s/^(.*)Ethernet controller: //;
    push (@ethernet_adapters, $_);
  }
}
close (LSPCI);


# IF statuses, addrs, pegs, etc.

# Get the 'real' red iface when connected
if (-e "${swroot}/red/active") {
  open (IFACE, "/var/smoothwall/red/iface")
    or warn "Could not open /var/smoothwall/red/iface: $!";
  chomp ($RED = <IFACE>);
  $netsettings{'RED_DEV'} = $RED;
  close (IFACE);
}

my @netconf;

# Get the link, addrs and stats for each active IF. GREEN must always be done first
if ($netsettings{'GREEN_DEV'})  { push (@netconf, &getLinkData($netsettings{"GREEN_DEV"}, "green")); }
if ($netsettings{'ORANGE_DEV'}) { push (@netconf, &getLinkData($netsettings{"ORANGE_DEV"}, "orange")); }
if ($netsettings{'PURPLE_DEV'}) { push (@netconf, &getLinkData($netsettings{"PURPLE_DEV"}, "purple")); }
if ($netsettings{'RED_DEV'})    { push (@netconf, &getLinkData($netsettings{"RED_DEV"}, "red")); }

# Get all IFs that have peg counts
open (DEV, "proc/net/dev");
@dev = <DEV>;
close DEV;

# Tidy up
chomp @dev;
shift @dev;
shift @dev;

# Check 'em all
foreach (@dev) {

  # Split and trim
  my @tmp = split;
  $tmp[0] =~ s/://;

  # Skip the obvious; we don't want repeats
  next if ($netsettings{'GREEN_DEV'} && $tmp[0] =~ /$netsettings{'GREEN_DEV'}/);
  next if ($netsettings{'ORANGE_DEV'} && $tmp[0] =~ /$netsettings{'ORANGE_DEV'}/);
  next if ($netsettings{'PURPLE_DEV'} && $tmp[0] =~ /$netsettings{'PURPLE_DEV'}/);
  next if ($netsettings{'RED_DEV'} && $tmp[0] =~ /$netsettings{'RED_DEV'}/);

  # If an IF saw traffic, get its info
  if ($tmp[1] > 0 || $tmp[2] > 0 || $tmp[9] > 0 || $tmp[10] > 0 ) {
    push (@netconf, &getLinkData($tmp[0], "gray"));
  }
}


# 'LIVE' NET SETTINGS

my ($line, @newarray, $block, $netmask, $bcast, $bcast_tag, $netmask_tag, @livered);

# Define the 'not used' tags that show when values in net settings are no used.
my $orange_notused = " [/b][/color][/size][size=85][color=grey][i]<not used>[/i][/color][/size][size=90][color=orange][b]";
my $purple_notused = " [/b][/color][/size][size=85][color=grey][i]<not used>[/i][/color][/size][size=90][color=purple][b]";
my $red_notused = " [/b][/color][/size][size=85][color=grey][i]<not used>[/i][/color][/size][size=90][color=red][b]";

# Define the actual values on a pppoX connected system
my ($dns1_tag, $dns2_tag, $redIP_tag, $remoteIP_tag, $bcast_tag, $netmask_tag);
if (($netsettings{'RED_TYPE'} eq 'DHCP' || 
     $netsettings{'RED_TYPE'} eq 'PPPOE') && 
    (-e "${swroot}/red/active")) {
  open (DNS1, "</var/smoothwall/red/dns1")
    or warn "Could not open /var/smoothwall/red/dns1: $!";
  chomp($redDNS1 = <DNS1>);
  if ($netsettings{'DNS1'} ne $redDNS1) { $dns1_tag = "$red_notused"; }
  $netsettings{'DNS1'} = $redDNS1;
  open (DNS2, "</var/smoothwall/red/dns2")
    or warn "Could not open /var/smoothwall/red/dns2: $!";
  chomp($redDNS2 = <DNS2>);
  if ($netsettings{'DNS2'} ne $redDNS2 || $netsettings{'DNS2'} eq "" ) { $dns2_tag = "$red_notused"; }
  $netsettings{'DNS2'} = $redDNS2;
  close (DNS1); close (DNS2);
  open (LOCALIP, "/var/smoothwall/red/local-ipaddress")
    or warn "Could not open /var/smoothwall/red/local-ipaddress: $!";
  chomp($redIP = <LOCALIP>);
  close (LOCALIP);
  if ($netsettings{'RED_ADDRESS'} ne $redIP) { $redIP_tag = "$red_notused"; }
  $netsettings{'RED_ADDRESS'} = $redIP;
  open (REMOTEIP, "/var/smoothwall/red/remote-ipaddress")
    or warn "Could not open /var/smoothwall/red/remote-ipaddress: $!";
  chomp($remoteIP = <REMOTEIP>);
  close (REMOTEIP);
  if ($netsettings{'DEFAULT_GATEWAY'} ne $remoteIP) { $remoteIP_tag = "$red_notused"; }
  $netsettings{'DEFAULT_GATEWAY'} = $remoteIP;

  # Let's get the broadcast and netmask of the red iface when up
# IP ADDR
  open (IPADDR_RED, "-|") or exec ("/usr/sbin/ip addr show $netsettings{'RED_DEV'}");
  @temp = <IPADDR_RED>;
  close (IPADDR_RED);
  foreach $line (@temp) {
    chomp $line;
    if ($line =~ /inet /) {
      chomp $line;
      @newarray = split / /, $line;
      for (my $i=1; $i<=4; $i++) {
        shift @newarray;
      }
      $block = new Net::Netmask($newarray[1]);
      $netmask = $block->mask();
      $bcast = $newarray[3];
    }
  }
  if ($netsettings{'RED_BROADCAST'} ne $bcast) { $bcast_tag = "$red_notused"; }
  $netsettings{'RED_BROADCAST'} = $bcast;
  if ($netsettings{'RED_NETMASK'} ne $netmask) { $netmask_tag = "$red_notused"; }
  $netsettings{'RED_NETMASK'} = $netmask;
  &writehash("/tmp/livesettings", \%netsettings);
  open (LIVESETTINGS,"</tmp/livesettings");
  while (<LIVESETTINGS>) {
    if (/RED|DNS|GATEWAY/) { push (@livered, $_); }
  }
  @live_red = sort @livered;
  @live_red = ("[color=red][b]", @live_red, "[/b][/color]");
  close (LIVESETTINGS);
}

# Opening /var/smoothwall/ethernet/settings regardless of the connection state.
# This file is not updated when on pppoe and/or dhcp and when you are disconnected/reconnected,
# and possibly when you subsequently run setup.
open (NETSETTINGS,"<${swroot}/ethernet/settings") || die "Unable to open $!";
while (<NETSETTINGS>) {
  chomp;
  if (/DNS1[^_]/) { push (@red, "$_" . $dns1_tag . "\n"); }
  elsif (/DNS2[^_]/) { push (@red, "$_" . $dns2_tag . "\n"); }
  elsif (/DNS[12]_/) { push (@red, "$_\n"); }
  elsif (/GATEWAY/) { push (@red, "$_" . $remoteIP_tag . "\n"); }
  elsif (/RED_ADDRESS/) { push (@red, "$_" . $redIP_tag . "\n"); }
  elsif (/RED_BROADCAST/) { push (@red, "$_" . $bcast_tag . "\n"); }
  elsif (/RED_NETMASK/) { push (@red, "$_" . $netmask_tag . "\n"); }
  elsif (/RED_D.*/) { push (@red, "$_\n"); }
  elsif (/RED_IGNORE.*/) { push (@red, "$_\n"); }
  elsif (/RED_N.*/) { push (@red, "$_\n"); }
  elsif (/RED_T.*/) { push (@red, "$_\n"); }
  elsif (/GREEN/) { push (@green, "$_\n"); }
  elsif ($netsettings{'PURPLE_DEV'} eq "" && /PURPLE/) { push (@purple, "$_" . $purple_notused . "\n"); }
  elsif ($netsettings{'PURPLE_DEV'} ne "" && /PURPLE/) { push (@purple, "$_\n"); }
  elsif ($netsettings{'ORANGE_DEV'} eq "" && /ORANGE/) { push (@orange, "$_" . $orange_notused . "\n"); }
  elsif ($netsettings{'ORANGE_DEV'} ne "" && /ORANGE/) { push (@orange, "$_\n"); }
  else { push (@other, "$_\n\n"); }
}
close (NETSETTINGS);
@green = sort @green;
@green = ("[color=green][b]", @green, "[/b][/color]\n");
@red = sort @red;
@red = ("[color=red][b]", @red, "[/b][/color]");
@purple = sort @purple;
@purple = ("[color=purple][b]", @purple, "[/b][/color]\n");
@orange = sort @orange;
@orange = ("[color=orange][b]", @orange, "[/b][/color]\n");
@other = sort @other;
my $note = '';
if ($netsettings{'RED_TYPE'} eq 'DHCP' || $netsettings{'RED_TYPE'} eq 'PPPOE') { $note = "$tr{'smoothinfo-note'}\n\n"; }
my @ethernet_settings = ("[size=90]", @other,@green,@orange,@purple,@red, "[/size]");
my @live_settings = ("[color=\#400000][i]$note\[/i]\[/color]", "[size=90]", @other,@green,@orange,@purple,@live_red, "[/size]");

# ROUTING
my $route = &pipeopen( '/usr/sbin/ip', 'route' );

# IPTABLES CHAINS
my @chains = split (/,/,$smoothinfosettings{'CHAINS'});

# MODS
my %modlist = ();
my $modpath = "${swroot}/mods";
#find(\&list, $dir);
# Deal with some "non-standard" mods
#open (BASE, "</usr/lib/smoothwall/langs/en.pl") || die "Couldn't open $base: $!";
#my @base = <BASE>;
#close (BASE);
#open (CRONTAB, "</etc/crontab") || die "Couldn't open /etc/crontab: $!";
#my @crontab = <CRONTAB>;
#close (CRONTAB);

my ($DIR, $entry);

opendir($DIR, $modpath) or die "Cannot open directory: '$modpath': $!";

while ( $entry = readdir $DIR ) {
    next if $entry =~ /\A\.\.?\z/;
    next unless (-d "$modpath/$entry");
    if ($entry eq 'pgraphs') {
      open (PG, "$modpath/pgraphs/installed");
      my $pgraphsversion = <PG>;
      close (PG);
      $modlist{'pgraphs'} = "$pgraphsversion for SWE 3.1";
    }
    elsif ($entry eq 'bmm') {
      open (BMM, "$modpath/bmm/installed");
      my $bmmversion = <BMM>;
      close (BMM);
      $modlist{'bmm'} = "$bmmversion for SWE 3.1";
    }
    elsif ($entry eq 'semf') {
      open (SEMF, "$modpath/semf/version");
      my $semfversion = <SEMF>;
      close (SEMF);
      $modlist{'semf'} = $semfversion;
    }
    elsif ($entry eq 'enhanced-fw-logs') {
      $modlist{'enhanced-fw-logs'} = 'Enhanced Firewall Logs for SWE 3.1';
    }
    elsif ($entry eq 'fullfirewall') {
      $modlist{'fullfirewall'} = 'Full Firewall Control for SWE 3.1';
    }
    elsif ($entry eq 'proxy') {
      $modlist{'proxy'} = 'Enhanced Web Proxy with SSL Filtering for SWE 3.1';
    }
    elsif ($entry eq 'clearlog') {
      open (CL, "$modpath/clearlog/installed");
      my $clearlogversion = <CL>;
      close (CL);
      $modlist{'clearlog'} = $clearlogversion;
    }
    elsif ($entry eq 'clamblocklists') {
      open (VERSION,"<$modpath/clamblocklists/version");
      $clamblocklistsversion = <VERSION>;
      $modlist{'clamblocklists'} = "ClamAV Blocklists v. $clamblocklistsversion";
    }
    elsif ($entry eq 'traflog') {
      open (TL, "$modpath/traflog/version");
      my $traflogversion = <TL>;
      close (TL);
      $modlist{'traflog'} = "Traffic Log v. $traflogversion for SWE 3.1";
    }
    elsif ($entry eq 'crontool') {
      $modlist{'crontool'} = 'Crontab File Editor for SWE 3.1';
    }
    elsif ($entry eq 'adzap') {
      $modlist{'adzap'} = 'Ad Zapper for SWE 3.1';
    }
    elsif ($entry eq 'urlfilter') {
      $modlist{'urlfilter'} = 'Time Constraints and Blacklist Editor for URL Filter for SWE 3.1';
    }
    elsif ($entry eq 'bandview') {
      open (BANDVIEWX, "$modpath/bandview/installedX");
      my $bandviewxversion = <BANDVIEWX>;
      close (BANDVIEWX);
      $modlist{'bandview'} = "BandviewX v. $bandviewxversion";
    }
    elsif ($entry eq 'dglog') {
      &readhash("$modpath/dglog/DETAILS", \%dglogsettings);
      $dglogversion = "$dglogsettings{'MOD_INFO'} v. $dglogsettings{'MOD_VERSION'}";
      $modlist{'dglog'} = $dglogversion;
    }
    elsif ($entry eq 'dhcpwol') {
      $modlist{'dhcpwol'} = 'Enhanced DHCP and Wake on LAN (WOL) for SWE 3.1';
    }
    elsif ($entry eq 'cpufreq-utils') {
      $modlist{'cpufreq-utils'} = 'CPU Frequency Utilities for SWE 3.1';
    }
    elsif ($entry eq 'filtering') {
      $modlist{'filtering'} = 'E2Guardian Content Filter for SWE 3.1';
    }
    elsif ($entry eq 'zerina') {
      &readhash("$modpath/zerina/settings", \%zsettings);
      $zerinaversion = "ZERINA-$zsettings{'VERSION'} / OpenVPN v$zsettings{'OVPNVER'}";
      $modlist{'zerina'} = $zerinaversion;
    } else {
      $modlist{$entry} = "$entry for SWE 3.1";
    }
}
closedir $DIR;
# Mods not in $modpath
if (-e "/usr/bin/mc") {
  $modlist{'mc'} = 'Midnight Commander for SWE 3.1';
}

# MODULES
my $modules = &pipeopen( '/bin/lsmod' );
open (TOP, "-|") or exec ("/usr/bin/top -b -n 1");
my @top = (<TOP>);
close (TOP);
pop (@top);

# CONFIG
my ($RED, $ORANGE, $PURPLE);
my ($reddev, $orangedev, $purpledev);
open (ETHERSETTINGS,"<${swroot}/ethernet/settings") || print "Unable to open $!";
my @ethersettings = <ETHERSETTINGS>;
close (ETHERSETTINGS);
my $reddev = (grep /RED_DEV=eth/, @ethersettings)[0];
if ($netsettings{'ORANGE_DEV'}) {
  $orangedev = (grep /ORANGE_DEV=eth/, @ethersettings)[0];
}

if ($netsettings{'PURPLE_DEV'}) {
  $purpledev = (grep /PURPLE_DEV=eth/, @ethersettings)[0];
}
chomp ($reddev, $orangedev, $purpledev);


###################  Report Generation  ###################  

my $reportDate = `/bin/date +"%Y/%m/%d %H:%M:%S"`;
chomp $reportDate;
open (FILE,">$outputfile") || die 'Unable to open file';
print FILE "[size=110][color=purple][u][b]$tr{'smoothinfo-generated'}${reportDate}[/b][/u][/color][/size]\n\n";


### Smoothwall Section
print FILE "\n[u][b]Smoothwall[/b][/u]\n";

# Version
print FILE "[info=\"$tr{'smoothinfo-smoothwall-version'}\"]\[code\]Smoothwall $displayVersion\[/code\]\[/info\]";

chomp %smoothinfosettings;
if ($smoothinfosettings{'CONFIG'} eq 'on') {
  if ($reddev) {$RED = 'RED'} else { $RED = 'RED(modem)'}
  if ($orangedev) {$ORANGE = '-ORANGE'}
  if ($purpledev ne "") {$PURPLE = '-PURPLE'}
  print FILE "[info=\"$tr{'smoothinfo-firewall-config-type'}\"]\[code\]$RED-GREEN$ORANGE$PURPLE\[/code\]\[/info\]";
}

# The connection type
if ($smoothinfosettings{'CONNTYPE'} eq 'on') {
  my $conntype = '';
  if ($pppsettings{'COMPORT'} =~ /^tty/) {$conntype = 'Dial-Up';}
  elsif ($pppsettings{'COMPORT'} =~ /^isdn/) {$conntype = 'ISDN';}
  elsif ($pppsettings{'COMPORT'} eq 'pppoe') {$conntype = 'PPPOE';}
  elsif ($reddev) {$conntype = 'LAN';}
  else {$conntype = 'Cable or DSL';}
  print FILE "[info=\"$tr{'smoothinfo-connection'}\"]\[code\]$conntype\[/code\]\[/info\]";
}

# Default firewall policy
if ($smoothinfosettings{'FWPOLICY'} eq 'on') {
  if ($defseclevelsettings{'OPENNESS'} eq 'halfopen') {
    $smoothinfosettings{'SECPOLICY'} = 'Half-open';
  } elsif ($defseclevelsettings{'OPENNESS'} eq 'open') {
    $smoothinfosettings{'SECPOLICY'} = 'Open';
  } elsif ($defseclevelsettings{'OPENNESS'} eq 'closed') {
    $smoothinfosettings{'SECPOLICY'} = 'Closed';
  } else {
    $smoothinfosettings{'SECPOLICY'} = '(Unknown)';
  }
  print FILE "[info=\"$tr{'smoothinfo-default-secpol'}\"]\[code\]$tr{'smoothinfo-policy'}: $smoothinfosettings{'SECPOLICY'}\n";
    if (open (OUTGOING, "<${swroot}/outgoing/settings")) {
      foreach (<OUTGOING>) {
        if (grep /GREEN=REJECT/, $_) {
          $rule_green = "$tr{'smoothinfo-traffic-originating'} GREEN is: $tr{'smoothinfo-allowed'}"; print FILE "$rule_green\n";
        }
        if (grep /GREEN=ACCEPT/, $_) {
          $rule_green = "$tr{'smoothinfo-traffic-originating'} GREEN is: $tr{'smoothinfo-blocked'}"; print FILE "$rule_green\n";
        }
        if (grep /ORANGE=REJECT/, $_) {
          $rule_orange = "$tr{'smoothinfo-traffic-originating'} ORANGE is: $tr{'smoothinfo-allowed'}"; print FILE "$rule_orange\n";
        }
        if (grep /ORANGE=ACCEPT/, $_) {
          $rule_orange = "$tr{'smoothinfo-traffic-originating'} ORANGE is: $tr{'smoothinfo-blocked'}"; print FILE "$rule_orange\n";
        }
        if (grep /PURPLE=REJECT/, $_) {
          $rule_purple = "$tr{'smoothinfo-traffic-originating'} PURPLE is: $tr{'smoothinfo-allowed'}"; print FILE "$rule_purple\n";
        }
        if (grep /PURPLE=ACCEPT/, $_) {
          $rule_purple = "$tr{'smoothinfo-traffic-originating'} PURPLE is: $tr{'smoothinfo-blocked'}"; print FILE "$rule_purple\n";
        }
      }
      close OUTGOING;
    }
  print FILE "\[/code\]\[/info\]";
}

# Generate the ASCII schematic (ugly but works)
my $purple;
if ($orangedev) {$orange = '(orange)';} else {$orange = '        ';}
if ($purpledev) {$purple = '(purple)';} else {$purple = '        ';}
if (-e "${SIdir}/etc/schematic") {
  print FILE "[info=\"$tr{'smoothinfo-ascii-schematic'}\"][code\]";

  # RED
  print FILE "                                  Internet\n";
  print FILE "                                     |\n";
  if ($smoothinfosettings{'MODEM'} eq 'on') {
    print FILE "                                   Modem\n";
    print FILE "                                     |\n";
  }
  if ($smoothinfosettings{'ROUTER'} eq 'on') {
    print FILE "                                   Router\n";
    print FILE "                                     |\n";
  }
  print FILE "                                   (red)\n";

  # ORANGE
  if ($smoothinfosettings{'SWITCH2'} eq 'on') {
    if ($smoothinfosettings{'WAP2'} eq 'on') {

print FILE "  WAP <=== Switch <=== $orange ";

    } else {

print FILE "           Switch <=== $orange ";

    }
    print FILE "[SMOOTHWALL] (green)";
  } elsif ($smoothinfosettings{'WAP3'} eq 'on') {

print FILE "    WLan <=== WAP <=== $orange ";

    print FILE "[SMOOTHWALL] (green)";

  } else {

print FILE "                       $orange [SMOOTHWALL] (green)";

  }


  # GREEN
  if ($smoothinfosettings{'SWITCH1'} eq 'on') {
    if ($smoothinfosettings{'WAP1'} eq 'on') {

print FILE " ===> Switch ===> WAP";

    } else {

print FILE " ===> Switch";

    }

  } elsif ($smoothinfosettings{'WAP4'} eq 'on') {
    print FILE " ===> WAP ===> WLan";
  }

  # PURPLE
  if ($smoothinfosettings{'WAP6'} eq 'on' &&
      $smoothinfosettings{'SWITCH3'} eq 'on') {
    print FILE "\n                                  $purple\n";
    print FILE "                                     |\n";
    print FILE "                                   Switch\n";
    print FILE "                                     |\n";
    print FILE "                                    WAP\n";
    print FILE "                                     |\n";
    print FILE "                                   W/LAN";
  } elsif ($smoothinfosettings{'WAP6'} ne 'on' &&
      $smoothinfosettings{'SWITCH3'} eq 'on') {
    print FILE "\n                                  $purple\n";
    print FILE "                                     |\n";
    print FILE "                         Switch";
  } elsif ($smoothinfosettings{'WAP5'} eq 'on') {
    print FILE "\n                                  $purple\n";
    print FILE "                                     |\n";
    print FILE "                                    WAP\n";
    print FILE "                                     |\n";
    print FILE "                                   W/LAN";
  }


  print FILE "\[/code\]\[/info\]";
}

# Services
if ($smoothinfosettings{'SERVICES'} eq 'on') {
  # Status of core services
  my $process_status;
  print FILE "[info=\"$tr{'smoothinfo-core-services'}\"]\[code\]";
  my @coreservices = ('cron', 'dnsmasq', 'httpd', 'klogd', 'smoothd');
  foreach my $service (@coreservices) {
    if (open(PID, "/var/run/$service.pid")) {
      $pid = <PID>; chomp $pid;
      close PID;
      if ($pid) {
        if (open(PID, "/proc/$pid/status")) {
           while (<PID>) {
             if (/^State:\W+(.*)/) {
               $status = $1;
             }
           }
           close PID;
           if ($status =~ /s|sleeping|r|running/i) {
	     $process_status = 'running';
           } else {
             $process_status = 'stopped';
           }
           if ($service =~ /cron/) { $name = 'CRON server'; }
           elsif ($service =~ /dnsmasq/) { $name = 'DNS proxy server'; }
           elsif ($service =~ /httpd/) { $name = 'Web server'; }
           elsif ($service =~ /klogd/) { $name = 'Logging server'; }
           elsif ($service =~ /smoothd/) { $name = 'SetUID Daemon'; }
           print FILE "$name ($service): $process_status\n";
        }
      }
    }
  }
  print FILE "\[/code\]\[/info\]";

  # Status of stock services
  print FILE "[info=\"$tr{'smoothinfo-services-status'}\"]\[code\]";
  if ($SSHsettings{'ENABLE_SSH'}) {
    print FILE "Remote access (SSH server): $SSHsettings{'ENABLE_SSH'}\n";
  }  
  if ($green_dhcpsettings{'ENABLE'}) {
    print FILE "DHCP server on green: $green_dhcpsettings{'ENABLE'}\n";
  }
  if ($purple_dhcpsettings{'ENABLE'}) {
    print FILE "DHCP server on purple: $purple_dhcpsettings{'ENABLE'}\n";
  }
  if ($imsettings{'ENABLE'}) {
    print FILE "IM Proxy: $imsettings{'ENABLE'}\n";
  }
  if ($p3scansettings{'ENABLE'}) {
    print FILE "Pop3 Proxy: $p3scansettings{'ENABLE'}\n";
  }
  if ($sipproxysettings{'ENABLE'}) {
    print FILE "SIP Proxy: $sipproxysettings{'ENABLE'}\n";
  }
  if ($snortsettings{'ENABLE_SNORT'}) {
    print FILE "IDS (Snort): $snortsettings{'ENABLE_SNORT'}\n";
  }
  print FILE "\[/code\]\[/info\]";
}


### Linux Section
if ($smoothinfosettings{'LOADEDMODULES'} eq 'on' or
    $smoothinfosettings{'TOP'} eq 'on' or
    $smoothinfosettings{'DMESG'} eq 'on' or
    $smoothinfosettings{'APACHE'} eq 'on' or
    $smoothinfosettings{'MESSAGES'} eq 'on' or
    $smoothinfosettings{'SREENSHOTS'} eq 'on' ) {
  print FILE "\n[u][b]Linux[/b][/u]\n";
  if ($smoothinfosettings{'LOADEDMODULES'} eq 'on') {
    my $data = do {local $/; $modules};
    # Will wrap lines longer then n characters
    $data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
    print FILE "[info=\"$tr{'smoothinfo-modules'}\"]\[code\]$data\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'TOP'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-top'}\"]\[code\]@top\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'DMESG'} eq 'on') {
    my $file = "/var/log/dmesg";
    my $dmesg;
    if ($smoothinfosettings{'LINES'} ne '' && $smoothinfosettings{'STRING'} eq '') {
      if ($smoothinfosettings{'HEADORTAIL'} eq 'HEAD') {
        open (DMESG,"<$file") || die "Unable to open $!";
        my @dmesg = (<DMESG>);
        @tmp = splice (@dmesg,0,$smoothinfosettings{'LINES'});
        open (TMP,">",\$dmesg);
        foreach (@tmp) {chomp; print TMP "$_\n";}
      } elsif ($smoothinfosettings{'HEADORTAIL'} eq 'TAIL') {
        open (DMESG,"<$file") || die "Unable to open $!";
        my @dmesg = (<DMESG>);
        $end = @dmesg;
        $start = $end - $smoothinfosettings{'LINES'};
        open (TMP,">",\$dmesg);
        $count = 0;
        foreach (@dmesg) {
          $count++;
          chomp;
          if ($count > $start && $count <= $end) {print TMP "$_\n";}
        }
      }
    } elsif ($smoothinfosettings{'LINES'} eq '' && $smoothinfosettings{'STRING'} ne '') {
      if ($smoothinfosettings{'IGNORECASE'} eq 'on') {
        open (DMESG,"<$file") || die "Unable to open $!";
        my @dmesg = (grep /$smoothinfosettings{'STRING'}/i, <DMESG>);
        open (TMP,">",\$dmesg);
        foreach (@dmesg) {chomp; print TMP "$_\n";}
      } else {
        open (DMESG,"<$file") || die "Unable to open $!";
        my @dmesg = (grep /$smoothinfosettings{'STRING'}/, <DMESG>);
        open (TMP,">",\$dmesg);
        foreach (@dmesg) {chomp; print TMP "$_\n";}
      }
    } elsif ($smoothinfosettings{'LINES'} eq '' && $smoothinfosettings{'STRING'} eq '') {
      open (DMESG,"<$file") || die "Unable to open $!";
      open (TMP,">",\$dmesg);
      foreach (<DMESG>) {chomp; print TMP "$_\n";}
    }
    
    if (!$dmesg) {
      print FILE "[info=\"$tr{'smoothinfo-dmesg2'}\"]\[code\]No search results for string '$smoothinfosettings{'STRING'}'.\[/code\]\[/info\]";
    } else {
      my $data = do {local $/; $dmesg};
      # Will wrap lines longer then n characters
      $data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
      print FILE "[info=\"$tr{'smoothinfo-dmesg2'}\"]\[code\]$data\[/code\]\[/info\]";
    }
  }

  if ($smoothinfosettings{'APACHE'} eq 'on') {
    my $file = "/var/log/httpd/error.log";
    my $apache_error_log;
    if ($smoothinfosettings{'LINES2'} ne '' && $smoothinfosettings{'STRING2'} eq '') {
      if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
        open (ERRORLOG,"<$file") || die "Unable to open $!";
        my @errorlog = (<ERRORLOG>);
        @tmp = splice (@errorlog,0,$smoothinfosettings{'LINES2'});
        open (TMP,">",\$apache_error_log);
        foreach (@tmp) {chomp; print TMP "$_\n";}
      } elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
        open (ERRORLOG,"<$file") || die "Unable to open $!";
        my @errorlog = (<ERRORLOG>);
        $end = @errorlog;
        $start = $end - $smoothinfosettings{'LINES2'};
        open (TMP,">",\$apache_error_log);
        $count = 0;
        foreach (@errorlog) {
          $count++;
          chomp;
          if ($count > $start && $count <= $end) {print TMP "$_\n";}
        }
      }
    } elsif ($smoothinfosettings{'LINES2'} eq '' && $smoothinfosettings{'STRING2'} ne '') {
      if ($smoothinfosettings{'IGNORECASE2'} eq 'on') {
        open (ERRORLOG,"<$file") || die "Unable to open $!";
        my @errorlog = (grep /$smoothinfosettings{'STRING2'}/i, <ERRORLOG>);
        open (TMP,">",\$apache_error_log);
        foreach (@errorlog) {chomp; print TMP "$_\n";}
      } else {
        open (ERRORLOG,"<$file") || die "Unable to open $!";
        my @errorlog = (grep /$smoothinfosettings{'STRING2'}/, <ERRORLOG>);
        open (TMP,">",\$apache_error_log);
        foreach (@errorlog) {chomp; print TMP "$_\n";}
      }
      close (ERRORLOG);
    } elsif ($smoothinfosettings{'LINES2'} ne '' && $smoothinfosettings{'STRING2'} ne '') {
      if ($smoothinfosettings{'IGNORECASE2'} eq 'on') {
        open (ERRORLOG,"<$file") || die "Unable to open /var/log/httpd/error_log";
        my @errorlog = (grep /$smoothinfosettings{'STRING2'}/i, <ERRORLOG>);
        open (TMP,">",\$temporary);
        foreach (@errorlog) {chomp; print TMP "$_\n";}
        close (TMP);
        if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
          open (HEAD,"<",\$temporary) || die "Unable to open $temporary";
          my @head = <HEAD>;
          @tmp = splice (@head,0,$smoothinfosettings{'LINES2'});
          open (TMP,">",\$apache_error_log);
          foreach (@tmp) {chomp; print TMP "$_\n";}
          close (TMP);
        } elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
          open (TAIL,"<",\$temporary) || die "Unable to open $var";
          my @tail = <TAIL>;
          $end = @tail;
          $start = $end - $smoothinfosettings{'LINES2'};
          open (TMP,">",\$apache_error_log);
          $count = 0;
          foreach (@tail) {
            $count++;
            chomp;
            if ($count > $start && $count <= $end) {print TMP "$_\n";}
          }
        }
      } else {
        open (ERRORLOG,"<$file") || die "Unable to open $file: $!";
        my @errorlog = (grep /$smoothinfosettings{'STRING2'}/, <ERRORLOG>);
        open (TMP,">",\$temporary);
        foreach (@errorlog) {chomp; print TMP "$_\n";}
        close (TMP);
        if ($smoothinfosettings{'HEADORTAIL2'} eq 'HEAD2') {
          open (HEAD,"<",\$temporary) || die "Unable to open $temporary";
          my @head = <HEAD>;
          @tmp = splice (@head,0,$smoothinfosettings{'LINES2'});
          open (TMP,">",\$apache_error_log);
          foreach (@tmp) {chomp; print TMP "$_\n";}
          close (TMP);
        } elsif ($smoothinfosettings{'HEADORTAIL2'} eq 'TAIL2') {
          open (TAIL,"<",\$temporary) || die "Unable to open $temporary";
          my @tail = <TAIL>;
          $end = @tail;
          $start = $end - $smoothinfosettings{'LINES2'};
          open (TMP,">",\$apache_error_log);
          $count = 0;
          foreach (@tail) {
            $count++;
            chomp;
            if ($count > $start && $count <= $end) {print TMP "$_\n";}
          }
        }
      }
    }

    if (!$apache_error_log) {
      print FILE "[info=\"$tr{'smoothinfo-apache-error2'}\"]\[code\]No search results for string '$smoothinfosettings{'STRING2'}'.\[/code\]\[/info\]";
    } else {
      my $data = do {local $/; $apache_error_log};
      # Will wrap lines longer than n characters
      $data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
      print FILE "[info=\"$tr{'smoothinfo-apache-error2'}\"]\[code\]$data\[/code\]\[/info\]";
    }
  }

  if ($smoothinfosettings{'MESSAGES'} eq 'on') {
    my $file = "/var/log/messages";
    my $messages_log;
    if ($smoothinfosettings{'LINES3'} ne '' && $smoothinfosettings{'STRING3'} eq '') {
      if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
        open (MESSAGES,"<$file") || die "Unable to open $!";
        my @messages = (<MESSAGES>);
        @tmp = splice (@messages,0,$smoothinfosettings{'LINES3'});
        open (TMP,">",\$messages_log);
        foreach (@tmp) {chomp; print TMP "$_\n";}
      } elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
        open (MESSAGES,"<$file") || die "Unable to open $!";
        my @messages = (<MESSAGES>);
        $end = @messages;
        $start = $end - $smoothinfosettings{'LINES3'};
        open (TMP,">",\$messages_log);
        $count = 0;
        foreach (@messages) {
          $count++;
          chomp;
          if ($count > $start && $count <= $end) {print TMP "$_\n";}
        }
      }
    } elsif ($smoothinfosettings{'LINES3'} eq '' && $smoothinfosettings{'STRING3'} ne '') {
      if ($smoothinfosettings{'IGNORECASE3'} eq 'on') {
        open (MESSAGES,"<$file") || die "Unable to open $!";
        my @messages = (grep /$smoothinfosettings{'STRING3'}/i, <MESSAGES>);
        open (TMP,">",\$messages_log);
        foreach (@messages) {chomp; print TMP "$_\n";}
      } else {
        open (MESSAGES,"<$file") || die "Unable to open $!";
        my @messages = (grep /$smoothinfosettings{'STRING3'}/, <MESSAGES>);
        open (TMP,">",\$messages_log);
        foreach (@messages) {chomp; print TMP "$_\n";}
      }
      close (MESSAGES);
    } elsif ($smoothinfosettings{'LINES3'} ne '' && $smoothinfosettings{'STRING3'} ne '') {
      if ($smoothinfosettings{'IGNORECASE3'} eq 'on') {
        open (MESSAGES,"<$file") || die "Unable to open $file: $!";
        my @messages = (grep /$smoothinfosettings{'STRING3'}/i, <MESSAGES>);
        open (TMP,">",\$temporary2);
        foreach (@messages) {chomp; print TMP "$_\n";}
        close (TMP);
        if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
          open (HEAD,"<",\$temporary2) || die "Unable to open $temporary2";
          my @head = <HEAD>;
          @tmp = splice (@head,0,$smoothinfosettings{'LINES3'});
          open (TMP,">",\$messages_log);
          foreach (@tmp) {chomp; print TMP "$_\n";}
          close (TMP);
        } elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
          open (TAIL,"<",\$temporary2) || die "Unable to open $temporary2: $!";
          my @tail = <TAIL>;
          $end = @tail;
          $start = $end - $smoothinfosettings{'LINES3'};
          open (TMP,">",\$messages_log);
          $count = 0;
          foreach (@tail) {
            $count++;
            chomp;
            if ($count > $start && $count <= $end) {print TMP "$_\n";}
          }
        }
      } else {
        open (MESSAGES,"<$file") || die "Unable to open $file: $!";
        my @messages = (grep /$smoothinfosettings{'STRING3'}/, <MESSAGES>);
        open (TMP,">",\$temporary2);
        foreach (@messages) {chomp; print TMP "$_\n";}
        close (TMP);
        if ($smoothinfosettings{'HEADORTAIL3'} eq 'HEAD3') {
          open (HEAD,"<",\$temporary2) || die "Unable to open $temporary2";
          my @head = <HEAD>;
          @tmp = splice (@head,0,$smoothinfosettings{'LINES3'});
          open (TMP,">",\$messages_log);
          foreach (@tmp) {chomp; print TMP "$_\n";}
          close (TMP);
        } elsif ($smoothinfosettings{'HEADORTAIL3'} eq 'TAIL3') {
          open (TAIL,"<",\$temporary2) || die "Unable to open $var";
          my @tail = <TAIL>;
          $end = @tail;
          $start = $end - $smoothinfosettings{'LINES3'};
          open (TMP,">",\$messages_log);
          $count = 0;
          foreach (@tail) {
            $count++;
            chomp;
            if ($count > $start && $count <= $end) {print TMP "$_\n";}
          }
        }
      }
    }


    if (!$messages_log) {
      print FILE "[info=\"$tr{'smoothinfo-system2'}\"]\[code\]No search results for string '$smoothinfosettings{'STRING3'}'.\[/code\]\[/info\]";
    } else {
      my $data = do {local $/; $messages_log};
      # Will wrap lines longer then n characters
      $data =~ s{(.{$smoothinfosettings{'WRAP'}})(?=.)}{$1\n}g;
      print FILE "[info=\"$tr{'smoothinfo-system2'}\"]\[code\]$data\[/code\]\[/info\]";
    }
  }

  if ($smoothinfosettings{'SCREENSHOTS'} ne '') {
    if ($smoothinfosettings{'SCREENSHOTS'} =~ /^(http|ftp)/) {
      $smoothinfosettings{'SCREENSHOTS'} = "\[img\]$smoothinfosettings{'SCREENSHOTS'}\[/img\]";
    }
    print FILE "[info=\"$tr{'smoothinfo-screenshots'}\"]$smoothinfosettings{'SCREENSHOTS'}\[/info\]";
  }
}


### Hardware Section
if ($smoothinfosettings{'CPU'} eq 'on' or
    $smoothinfosettings{'MEMORY'} eq 'on'or
    $smoothinfosettings{'IRQs'} eq 'on' or
    $smoothinfosettings{'DISKSPACE'} eq 'on' or
    $smoothinfosettings{'ADAPTERS'} eq 'on' ) {
  print FILE "\n[u][b]Hardware[/b][/u]\n";
  if ($smoothinfosettings{'CPU'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-cpu'}\"]\[code\]$cpu (Freq.: $frequency MHz - Cache: $cache - Cores: $cpuCores)\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'MEMORY'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-memory-specs'}\"]\[code\]$memory\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'IRQs'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-irq'}\"]\[code\]$warning@IRQs\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'DISKSPACE'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-diskspace'}\"]\[code\]$diskspace\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'ADAPTERS'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-ethernet-reported'}\"]\[code\]@ethernet_adapters\[/code\]\[/info\]";
  }

}


### Mods Section
if ($smoothinfosettings{'MODSERVICES'} eq 'on' or
    $smoothinfosettings{'MODLIST'} eq 'on' ) {
  print FILE "\n[u][b]Mods[/b][/u]\n";
  if ($smoothinfosettings{'MODSERVICES'} eq 'on') {
    my @modservices;
    push (@modservices, "[info=\"$tr{'smoothinfo-mod-services-status'}\"]\[code\]");
    if ($filteringsettings{'DGAV'}) {
      push (@modservices, "Dansguardian Web Content Filter (DGAV): $filteringsettings{'DGAV'}\n");
    }
    if ($filteringsettings{'SEMF'}) {
      push (@modservices,  "Smoothwall Express Mail Filter (SEMF): $filteringsettings{'SEMF'}\n");
    }
    if ($snortsettings{'ENABLE_GUARD'}) {
      push (@modservices, "Guardian Active Response (GAR): $snortsettings{'ENABLE_GUARD'}\n");
    }
    push (@modservices, "\[/code\]\[/info\]");
    $test = @modservices;
    # If at least one mod is found create the section
    if ($test > 2)  { print FILE "@modservices"; }
  }
  if ($smoothinfosettings{'MODLIST'} eq 'on') {
    if (%modlist) { $number = scalar (keys(%modlist)); }
    if ($number eq 1) { $suffix = ''; } else { $suffix = 's'; }
    my $id = 0;
    if (%modlist) {
      print FILE "[info=\"$number $tr{'smoothinfo-mods2'}$suffix\"]\[code\]";
      my @sorted = sort { lc($modlist{$a}) cmp lc($modlist{$b}) } keys %modlist;
      foreach(@sorted) { $id++; chomp ($modlist{$_}); print FILE "$id - $modlist{$_}\n"; }
    } else {
      print FILE "[info=\"$tr{'smoothinfo-mods'}\"]\[code\]";
      print FILE "$tr{'smoothinfo-no-mods'}. $tr{'smoothinfo-mods-tip'}";
    }
    print FILE "\[/code\]\[/info\]";
  }
}


if ($smoothinfosettings{'SQUID'} eq 'on' and $proxysettings{'ENABLE'} eq 'on') {
  print FILE "[info=\"$tr{'smoothinfo-proxy'}\"]\[code\]";
  print FILE "Squid Web proxy\n===========================\n";
  print FILE "Transparent: $proxysettings{'TRANSPARENT'}\n";  
  print FILE "Cache size (MB): $proxysettings{'CACHE_SIZE'}\n";
  print FILE "Remote proxy: $proxysettings{'UPSTREAM_PROXY'}\n";
  print FILE "Max object size (KB): $proxysettings{'MAX_SIZE'}\n";
  print FILE "Min object size (KB): $proxysettings{'MIN_SIZE'}\n";
  print FILE "Max outgoing size (KB): $proxysettings{'MAX_OUTGOING_SIZE'}\n";
  print FILE "Max incoming size (KB): $proxysettings{'MAX_INCOMING_SIZE'}\n";
  print FILE "\[/code\]\[/info\]";
}


### Networking Section
if ($smoothinfosettings{'NETCONF2'} eq 'on' or
    $smoothinfosettings{'DHCPINFO'} eq 'on' or
    $smoothinfosettings{'XTACCESS'} eq 'on' or
    $smoothinfosettings{'DNS'} eq 'on' or
    $smoothinfosettings{'NETCONF1'} eq 'on' or
    $smoothinfosettings{'ROUTE'} eq 'on' or
    $smoothinfosettings{'OUTGOING'} eq 'on' or
    $smoothinfosettings{'CONNTRACKS'} eq 'on' or
    $smoothinfosettings{'PINHOLES'} eq 'on' or
    $smoothinfosettings{'PORTFW'} eq 'on' ) {
  print FILE "\n[u][b]Networking[/b][/u]\n";

  if ($smoothinfosettings{'DNS'} eq "on") {
    # Get the DNS info for Red, Green, Purple
    print FILE "[info=\"$tr{'smoothinfo-dns'}\"]\[code\]";
    open (DNS1, "</var/smoothwall/red/dns1");
    chomp($redDNS1 = (<DNS1>)[0]);
    open (DNS2, "</var/smoothwall/red/dns2");
    chomp($redDNS2 = (<DNS2>)[0]);
    print FILE "DNS servers for RED:\nDNS1: $redDNS1\nDNS2: $redDNS2\n";
    close (DNS1);
    close (DNS2);

    unless (-z "${swroot}/dhcp/settings-green") {
      print FILE "DNS servers for GREEN:\nDNS1: $green_dhcpsettings{'DNS1'}\nDNS2: $green_dhcpsettings{'DNS2'}\n";
    }
    unless (-z "${swroot}/dhcp/settings-purple") {
      print FILE "DNS servers for PURPLE:\nDNS1: $purple_dhcpsettings{'DNS1'}\nDNS2: $purple_dhcpsettings{'DNS2'}\n";
    }
    print FILE "\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'CONNTRACKS'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-conntracks'}\"]\[code\]$conntracks\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'NETCONF1'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-netsettings1'}\"]\[quote\][size=90\]@netconf_red@netconf_green@netconf_purple@netconf_orange@netconf\[/size\]\[/quote\]\[/info\]";
  }

  if ( -e "$MODDIR/etc/clientip"){
    open (CLIENTIP,"<$MODDIR/etc/clientip") || die "Unable to open $!";
    my @clientIP = (<CLIENTIP>);
    close (CLIENTIP);
    print FILE "[info=\"$tr{'smoothinfo-client-IP'}\"]";
    print FILE "\[code\]@clientIP\[/code\]\[/info\]";
    unlink ("/tmp/clientip");
  }

  if ($smoothinfosettings{'NETCONF2'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-netsettings2'}\"]\[quote\]@ethernet_settings\[/quote\]\[/info\]";
    if (($netsettings{'RED_TYPE'} eq 'DHCP' || $netsettings{'RED_TYPE'} eq 'PPPOE') && 
        (-e "${swroot}/red/active")) {
         print FILE "[info=\"$tr{'smoothinfo-livesettings'}\"]\[quote\]@live_settings\[/quote\]\[/info\]";
    }
  }

  if ($smoothinfosettings{'DHCPINFO'} eq 'on' && -e "${swroot}/dhcp/enable") {
  
    unless (-z "${swroot}/dhcp/green") {
      print FILE "[info=\"$tr{'smoothinfo-dhcpsettings'} green\"]\[code\]";
      print FILE "Range of addresses: $green_dhcpsettings{'START_ADDR'} - $green_dhcpsettings{'END_ADDR'}\n";
      print FILE "Default lease time (mins): $green_dhcpsettings{'DEFAULT_LEASE_TIME'}\n";
      print FILE "Max lease time (mins): $green_dhcpsettings{'MAX_LEASE_TIME'}\n";
      print FILE "Primary DNS: $green_dhcpsettings{'DNS1'}\n";
      print FILE "Secondary DNS: $green_dhcpsettings{'DNS2'}\n";
      print FILE "Primary NTP: $green_dhcpsettings{'NTP1'}\n";
      print FILE "Secondary NTP: $green_dhcpsettings{'NTP2'}\n";
      print FILE "Primary WINS: $green_dhcpsettings{'WINS1'}\n";
      print FILE "Secondary WINS: $green_dhcpsettings{'WINS2'}\n";
      print FILE "Domain name suffix: $green_dhcpsettings{'DOMAIN_NAME'}\n";
      print FILE "NIS domain: $green_dhcpsettings{'NIS_DOMAIN'}\n";
      print FILE "Primary NIS: $green_dhcpsettings{'NIS1'}\n";
      print FILE "Secondary NIS: $green_dhcpsettings{'NIS2'}\n";
      print FILE "\[/code\]";
    
      unless (-z "${swroot}/dhcp/staticconfig-green") {
        open (STATIC, "${swroot}/dhcp/staticconfig-green");
        @statics = <STATIC>;
        close (STATIC);
        print FILE "[b]$tr{'smoothinfo-statics'}\[/b]\[code\]";
        print FILE "@statics";
        print FILE "\[/code\]\[/info\]";
      } else {
        print FILE "\[/info\]";
      }
    }

    unless (-z "${swroot}/dhcp/purple") {
      print FILE "[info=\"$tr{'smoothinfo-dhcpsettings'} purple\"]\[code\]";
      print FILE "Range of addresses: $purple_dhcpsettings{'START_ADDR'} - $purple_dhcpsettings{'END_ADDR'}\n";
      print FILE "Default lease time (mins): $purple_dhcpsettings{'DEFAULT_LEASE_TIME'}\n";
      print FILE "Max lease time (mins): $purple_dhcpsettings{'MAX_LEASE_TIME'}\n";
      print FILE "Primary DNS: $purple_dhcpsettings{'DNS1'}\n";
      print FILE "Secondary DNS: $purple_dhcpsettings{'DNS2'}\n";
      print FILE "Primary NTP: $purple_dhcpsettings{'NTP1'}\n";
      print FILE "Secondary NTP: $purple_dhcpsettings{'NTP2'}\n";
      print FILE "Primary WINS: $purple_dhcpsettings{'WINS1'}\n";
      print FILE "Secondary WINS: $purple_dhcpsettings{'WINS2'}\n";
      print FILE "Domain name suffix: $purple_dhcpsettings{'DOMAIN_NAME'}\n";
      print FILE "NIS domain: $purple_dhcpsettings{'NIS_DOMAIN'}\n";
      print FILE "Primary NIS: $purple_dhcpsettings{'NIS1'}\n";
      print FILE "Secondary NIS: $purple_dhcpsettings{'NIS2'}\n";
      print FILE "\[/code\]";
    
      unless (-z "${swroot}/dhcp/staticconfig-purple") {
        open (STATIC, "${swroot}/dhcp/staticconfig-purple");
        @statics = <STATIC>;
        close (STATIC);
        print FILE "[b]$tr{'smoothinfo-statics'}\[/b]\[code\]";
        print FILE "@statics";
        print FILE "\[/code\]\[/info\]";
      } else {
        print FILE "\[/info\]";
      }
    }

    if (-e "/usr/etc/dhcpd.leases") {
      print FILE "[info=\"$tr{'smoothinfo-dhcpleases'}\"]\[code\]";
      # block of code borrowed from dhcp.cgi

      ### Simple DHCP Lease Viewer (2007-0905) put together by catastrophe
      # - Borrowed "dhcpLeaseData" subroutine from dhcplease.pl v0.2.5 (DHCP Pack v1.3) for SWE2.0
      # by Dane Robert Jones and Tiago Freitas Leal
      # - Borrowed parts of "displaytable" subroutine from smoothtype.pm
      # (Smoothwall Express "Types" Module) from SWE3.0 by the Smoothwall Team
      # - Josh DeLong - 09/15/07 - Added unique filter
      # - Josh DeLong - 09/16/07 - Fixed sort bug and added ability to sort columns
      # - Josh DeLong - 10/1/07 - Rewrote complete dhcp.cgi to use this code
      ###

      my $leaseCount = -1;
      my $dhcptmpfile = "${SIdir}/tempfile";

      # Location of DHCP Lease File
      my $datfile = "/usr/etc/dhcpd.leases";
      open (LEASES,"<$datfile") || die "Unable to open $!";
      @catleasesFILENAME = (<LEASES>);
      close (LEASES);
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

          } elsif ($datLine =~ /^hardware ethernet/) {

            @lineSplit = split(/ /,$datLine);     # Extract MAC Address
            $dhcplMACAddy[$leaseCount] = uc($lineSplit[2]); # Make MAC Address All Upper Case for page consistancy.

          } elsif ($datLine =~ /^client-hostname/ || $datLine =~ /^hostname/) {

            @lineSplit = split(/ /,$datLine);     # Extract Host Name
            $dhcplHostName[$leaseCount] = $lineSplit[1];
          }
        }
      }

      for ($i = $#dhcplIPAddy; $i >= 0; $i--) {
        $catLINEnumber = $i+1;
        $dhcpprintvar = "True";

        if ($i == $#dhcplIPAddy){
          push(@dhcptemparray, $dhcplIPAddy[$i]);
        } else {
          foreach $IP (@dhcptemparray) {
            if ($IP =~ $dhcplIPAddy[$i]) {
              $dhcpprintvar = "False";
            }
          }
        }

        if (index($dhcplIPAddy[$i], $dhcpstart) == -1 ) {
          $dhcpprintvar = "False"
        }

        # Printing values to temp file
        if ($dhcpprintvar =~ "True"){
          push(@dhcptemparray, $dhcplIPAddy[$i]);
          print FILE "IP: $dhcplIPAddy[$i] Lease started: $dhcplStart[$i] Ends: $dhcplEnd[$i] Mac: $dhcplMACAddy[$i] Host name: $dhcplHostName[$i]\n";
        }
      }
  
      if (!@dhcptemparray) {
        print FILE "No leases.";
      }
  
      print FILE "\[/code\]\[/info\]";
    }

  }

  if ($smoothinfosettings{'ROUTE'} eq 'on') {
    print FILE "[info=\"$tr{'smoothinfo-routes'}\"]\[code\]$route\[/code\]\[/info\]";
  }

  if (($smoothinfosettings{'PORTFW'} eq 'on') && (! -z "${swroot}/portfw/config")) {
    my @portfw = `/bin/cat /var/smoothwall/portfw/config`;
    my @rules = `/usr/sbin/iptables -nvL portfwf`;
    my @rules2 = `/usr/sbin/iptables -t nat -nvL portfw`;
  
    print FILE "[info=\"$tr{'smoothinfo-portfw'}\"]\[code\]Config File:\n @portfw\n@rules\n@rules2\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'OUTGOING'} eq 'on') {
    unless (-z "${swroot}/outgoing/config") {
      my @config = `/bin/cat /var/smoothwall/outgoing/config`;

      my @chaingreen = `/usr/sbin/iptables -nvL outgreen`;
      my @chainpurple = `/usr/sbin/iptables -nvL outpurple`;
      my @chainorange = `/usr/sbin/iptables -nvL outorange`;
      my @chainallows = `/usr/sbin/iptables -nvL allows`;
      print FILE "[info=\"Outgoing exceptions\"]\[code\]Config file:\n@config\n@chaingreen\n@chainpurple\n@chainorange\n@chainallows\[/code\]\[/info\]";
      close CONFIG;
    }
  }

  if (($smoothinfosettings{'XTACCESS'} eq 'on') && (! -z "${swroot}/xtaccess/config")) {
    my @xtaccess = `/bin/cat /var/smoothwall/xtaccess/config`;

    my @rules = `/usr/sbin/iptables -nvL xtaccess`;

    print FILE "[info=\"External access\"]\[code\]Config file:\n @xtaccess\n@rules\[/code\]\[/info\]";
  }

  if (($smoothinfosettings{'PINHOLES'} eq 'on') && (! -z "${swroot}/dmzholes/config")) {
    my @dmzholes = `/bin/cat /var/smoothwall/dmzholes/config`;

    my @rules = `/usr/sbin/iptables -nvL dmzholes`;

    print FILE "[info=\"Internal pinholes\"]\[code\]Config file:\n @dmzholes\n@rules\[/code\]\[/info\]";
  }

  if ($smoothinfosettings{'CHAINS'} ne '') {
    foreach (@chains) {
      if (/All chains/) {
        open (FIREWALL,"-|", '/usr/sbin/iptables', '-L', '-n', '-v');  last;
      } else {
        open (FIREWALL,"-|", '/usr/sbin/iptables', '-L', $_, '-n', '-v')
      }
      @firewall = <FIREWALL>;
      push (@filtering, "\n");
      @filtering = (@filtering,@firewall);
    }
    shift (@filtering);
    print FILE "[info=\"$tr{'smoothinfo-firewall'}\"]\[code\]@filtering\[/code\]\[/info\]";
  }
}

if ( -e "$MODDIR/etc/otherinfo"){
  open (EXTRA,"<$MODDIR/etc/otherinfo") || die "Unable to open $!";
  my @extrainfo = (<EXTRA>);
  close (EXTRA);
  $section_title = shift @extrainfo;
  chomp $section_title;
  $section_title =~ s/([:;)(!'"]*)//g;
  $section_title = ucfirst $section_title;
  print FILE "[color=purple]====================================================[/color]\n";
  print FILE "[info=\"$section_title\"]";
  print FILE "\[code\]@extrainfo\[/code\]\[/info\]";
}

print FILE "[color=purple][i][size=90]Smoothinfo was adapted from Pascal Touche's Smoothinfo mod for SWE3.0.[/size][/i][/color]\n";

unlink ("/tmp/livesettings");

close (FILE);

sub list {
  my $id = 0;
  next unless -d;
  next if /modfiles/;
  next if /updates/;
  next if /smoothinfo/;
  next if /patches/;
  if (-s "$File::Find::name/installed") {
    open (FILE, "$File::Find::name/installed");
    $ver = <FILE>;
    close (FILE);
    $ver =~ s/#//;
    $ver =~ s/^\s+//;
    $modlist{$_} = $ver;
  }
  if (-s "$File::Find::name/DETAILS") {
    &readhash("$File::Find::name/DETAILS", \%modinfo);
    if ($modinfo{'MOD_LONG_NAME'}){
      $modlist{basename($File::Find::name)} = ucfirst $modinfo{'MOD_LONG_NAME'} . " v. " . $modinfo{'MOD_VERSION'};
    } else {
      $modlist{basename($File::Find::name)} = ucfirst $modinfo{'MOD_NAME'} . " v. " . $modinfo{'MOD_VERSION'};
    }
  }
}



# This function fetches the link and addr info for the specified IF. It is assumed that
#   the caller has verified the IF's existence. It returns BBcode of the desired color.
#
sub getLinkData {
  my ($iface, $color) = @_;

  my (@netconf, @netconf1, @netconf2);

  # Get the link info and RX/TX counts; note that splitting loses the newlines
  @netconf1 = split(/\n/, &pipeopen( "/usr/sbin/ip", "-s", "link", "show", "$iface" ));

  # Get the ip address(es); note that splitting loses the newlines
  @netconf2 = split(/\n/, &pipeopen( "/usr/sbin/ip", "addr", "show", "$iface" ));

  my $getStats = 0;
  foreach (@netconf1, @netconf2) {

    # Make the IP addr/masks black
    $_ =~ s/(\d+\.\d+\.\d+\.\d+\/\d+)/\[\/b]\[\/color][color=#000000][b]$1\[\/b][\/color\][color=$color\][b\]/g;
    $_ =~ s/([0-9a-f:]+\/\d+)/\[\/b]\[\/color][color=#000000][b]$1\[\/b][\/color\][color=$color\][b\]/g;

    # Restore the newlines that were split out above
    $_ =~ s/$/\n/;

    # Add labels to the RX stats line
    if ($getStats == 1) {
      my @tmp = split(/ +/);
      $_ = "RX: bytes:$tmp[1] packets:$tmp[2] errors:$tmp[3] dropped:$tmp[4] overrun:$tmp[5] multicast:$tmp[6]\n";
      $getStats = 0;
    }

    # Add labels to the TX stats line
    if ($getStats == 2) {
      my @tmp = split(/ +/);
      $_ = "TX: bytes:$tmp[1] packets:$tmp[2] errors:$tmp[3] dropped:$tmp[4] carrier:$tmp[5] collisions:$tmp[6]\n";
      $getStats = 0;
    }

    # The RX: and TX: stats lines trigger the operation on the next line and 'delete' themselves
    if ($_ =~ /^ +RX:/) { $getStats = 1; $_ = undef; }
    if ($_ =~ /^ +TX:/) { $getStats = 2; $_ = undef; }
  }

  # Dump the interface 'number'
  $netconf1[0] =~ s/^[0-9]+: +//;

  # Prepare the final text (build a new list)
  # Use the first two lines of 'ip link' output, lines 2... of 'ip addr', then lines 2... of 'ip link'
  @netconf = ("[b][color=$color]", @netconf1[0..1], @netconf2[2..$#netconf2], @netconf1[2..$#netconf1], "[/color][/b]");
  #print stderr "$iface IF Info\n". Dumper @netconf;

  # oss in a newline if not the first (RED)
  if ($color ne "green" ) {
    $netconf[0] = "\n".$netconf[0];
  }

  # And return it
  return @netconf;
}
