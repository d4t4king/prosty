#! /usr/bin/perl

use lib "/usr/lib/smoothwall";
use header qw( :standard );

print "Pragma: no-cache\n";
print "Cache-control: no-cache\n";
print "Connection: close\n";
print "content-type: text/plain\n\n";

my $flagfile = "${swroot}/backup/flag";

open FLAG, $flagfile;
read FLAG, $flag, 500;
close FLAG;

chomp $flag;
print $flag;
