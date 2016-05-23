#!/usr/bin/perl

use strict;
use CGI;
use Data::Dumper;
use XML::Simple;

# Deal with CGI:
my $q = new CGI;
my $file = $q->param('f');
$file =~ s/[^0-9a-zA-Z\._]//g;

# Parse the GPX:
my $doc = XMLin("/data/GPXwww/gpx/$file", KeyAttr=>{'other_package'}) or die "Error! $!";
my $lat = $doc->{trk}->{trkseg}->{trkpt}[0]->{lat};
my $lon = $doc->{trk}->{trkseg}->{trkpt}[0]->{lon};

# Print the header and content:
print $q->header;
print qq{
<html>
<head>
  <!-- Source: http://wiki.openstreetmap.org/wiki/Openlayers_Track_example -->
  <title>GPX Track - $file</title>
  <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
  <script src="http://www.openstreetmap.org/openlayers/OpenStreetMap.js"></script>
  <script type="text/javascript">
    var map; //complex object of type OpenLayers.Map

    function init() {
      map = new OpenLayers.Map ("map", {
        controls:[
          new OpenLayers.Control.Navigation(),
          new OpenLayers.Control.PanZoomBar(),
          new OpenLayers.Control.LayerSwitcher(),
          new OpenLayers.Control.Attribution()],
        numZoomLevels: 120,
        units: 'dd',
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326")
      } );

      // Define the map layer
      layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
      map.addLayer(layerMapnik);
      layerCycleMap = new OpenLayers.Layer.OSM.CycleMap("CycleMap");
      map.addLayer(layerCycleMap);
      layerMarkers = new OpenLayers.Layer.Markers("Markers");
      map.addLayer(layerMarkers);

      // Add the Layer with the GPX Track
      var lgpx = new OpenLayers.Layer.Vector("Lakeside cycle ride", {
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
          url: "gpx/$file",
          format: new OpenLayers.Format.GPX()
        }),
        style: {strokeColor: "purple", strokeWidth: 5, strokeOpacity: 0.5},
        projection: new OpenLayers.Projection("EPSG:4326")
      });
      map.addLayer(lgpx);

      // Start position for the map (hardcoded here for simplicity,
      // but maybe you want to get this from the URL params)
      var lat=$lat;
      var lon=$lon;
      var zoom=10;
      var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
      map.setCenter(lonLat, zoom);
    }
  </script>

</head>
<!-- body.onload is called once the page is loaded (call the 'init' function) -->
<body onload="init();">
  <!-- define a DIV into which the map will appear. Make it take up the whole window -->
  <div style="width:100%; height:100%" id="map"></div>
</body>
</html>
};
