#!/usr/bin/perl

# Nicolas JOURDEN - 2016-05-23 - GPLv2

print "Content-type: text/html\n\n";

use strict;
use CGI;
my $q = CGI->new();

# Extract the asset:
my $asset = $q->param('asset');
my $lat = $q->param('lat');
my $lon = $q->param('lon');

if (
  $asset =~ /[a-zA-Z0-9]+/g
  &&
  $lat =~ /[0-9.]+/g
  &&
  $lon =~ /[0-9.]+/g
)
{
  # Append data to local file:
  my $time = 0;
  open (LOG, ">>$asset.data") or die "HTTP/1.1 404 Not Found\r\n";
  printf LOG "%012d;%08.4f;%08.4f\n", $time, $lat, $lon;
  close(LOG);

  print "HTTP/1.1 200 OK\r\n";
}
else 
{
  print "HTTP/1.1 500 Error\r\n";
}

