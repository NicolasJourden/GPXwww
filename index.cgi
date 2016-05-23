#!/usr/bin/perl

use strict;
use CGI;
use Data::Dumper;
use XML::Simple;
use File::Basename;

# List the GPX:
my @gpxs = `ls -1 /data/GPXwww/gpx/*.gpx`;
my $tablecontent;

# Display:
my $q = CGI->new;
print $q->header,
      $q->start_html('GPX on the Web');

print $q->h1("List of GPX:");

foreach my $gpx (sort(@gpxs))
{
  $gpx =~ s/\n//g;
  my $doc = XMLin($gpx, KeyAttr=>{'other_package'}) or die "Error! $!";
  my($filename, $dirs, $suffix) = fileparse($gpx);
  push @$tablecontent,  $q->td([
    $doc->{name},
    $doc->{description},
    $doc->{trk}->{trkseg}->{trkpt}[0]->{time},
    $q->a({-href=>"display.cgi?f=$filename",-target=>'_new'}, $filename ),
    $q->a({-href=>"gpx/$filename"}, "[download]" )
  ]);
}

print $q->table( { border => 0, -width => '100%'}, $q->Tr( $tablecontent), );

print $q->end_html;
