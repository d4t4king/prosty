#! /usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );

print "Pragma: no-cache\n";
print "Cache-control: no-cache\n";
print "Connection: close\n";
print "content-type: text/plain\n\n";

#print "<p>
#  <a href='/cgi-bin/txt-bu-startAdd.cgi'>StartAdd</a><br>
#  <a href='/cgi-bin/txt-bu-cancelAdd.cgi'>CancelAdd</a><br>
#  <a href='/cgi-bin/txt-bu-addflag.cgi'>View flag</a><br>
#  <a href='/cgi-bin/txt-bu-setRsp.cgi?rsp=PatTest'>Set Name (PatTest)</a><br>
#</p>\n";

# Signal the program abort
my $flagfile = "${swroot}/backup/CANCELadd";
system ("touch $flagfile");
