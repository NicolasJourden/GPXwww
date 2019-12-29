#!/usr/bin/perl

# Nicolas JOURDEN - 2016-05-23 - GPLv2

use CGI::Carp 'fatalsToBrowser';
use CGI;
use Data::Dumper;
use XML::Simple;
use File::Basename;

# Display:
my $q = CGI->new;
print $q->header,
      $q->start_html('GPX on the Web');

# List the GPX:
my @gpxs = `ls -1 /data/GPXwww/gpx/*.gpx`;
my $tablecontent;

print $q->h1("List of GPX:");

foreach my $gpx (sort(@gpxs))
{
  $gpx =~ s/\n//g;
  my($filename, $dirs, $suffix) = fileparse($gpx);
  $filename =~ s/.gpx//g;
  my $doc = XMLin($gpx, KeyAttr=>{'other_package'}) or die "Error! $!";

  push @$tablecontent,  $q->td([
    $q->a({-href=>"display.cgi?f=" . $q->escape($filename),-target=>'_new'}, $filename ),
    $q->a({-href=>"gpx/".$q->escape($filename).".gpx"}, "[download]" )
  ]);
}

print $q->table( { border => 0, -width => '100%'}, $q->Tr( $tablecontent), );

print $q->a({-href=>"https://github.com/NicolasJourden/GPXwww/"}, "Powered by GPXwww" );
print $q->end_html;
