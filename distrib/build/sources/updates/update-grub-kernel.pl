#! /usr/bin/perl

# Copyright Neal P. Murphy, July 2015
#
# This program is licensed under the terms of the GNU Public License, version 2.


# Grab the kernel versions from the command line
my ($oldkern, $newkern) = @ARGV;
shift @ARGV;
shift @ARGV;

# Open the grub conf files
open presentConf, "</boot/grub/grub.conf";
open newConf, ">/boot/grub/newkernel.conf";
open oldConf, ">/boot/grub/oldkernel.conf";

# Dump the first lines to each destination
while ((<presentConf>))
{
  print newConf;
  print oldConf;

  # Only down to the 'background' line
  last if ($_ =~ /^background=.*/);
}

# Do the rest of the lines
while ((<presentConf>))
{
  # If it's present, forget the previous 'old kernel'; we only do two.
  last if ($_ =~ /^## Old Kernel/);

  $newLine = $_;

  # Adjust for the new kernel
  $newLine =~ s/$oldkern/$newkern/g;
  print newConf $newLine;

  # Relabel for the old kernel
  $_ =~ s/using/old Linux ($oldkern) using/g;
  $_ =~ s/(Console|Hardware)\)/\1, old [$oldkern] kernel)/g;
  print oldConf;
}

# Close so it can be replaced
close(presentConf);

# Let the admin choose the old kernel if desired
print newConf "## Old Kernel\ntitle Boot Old kernel [$oldkern]\nfile /boot/grub/oldkernel.conf\n";

rename "/boot/grub/newkernel.conf", "/boot/grub/grub.conf";
