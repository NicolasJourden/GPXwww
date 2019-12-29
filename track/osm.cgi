#!/usr/bin/perl

# Nicolas JOURDEN - 2016-05-23 - GPLv2

use strict;
use CGI;
my $q = CGI->new();

# Extract the asset:
my $asset = $q->param('asset');

if ($asset =~ /[a-zA-Z0-9]+/g)
{
  open (LOG, "$asset.data") or die "HTTP/1.1 404 Not Found\r\n";
  seek( LOG, -30, 2 );
  my @data = readline(LOG);
  my ($time, $lat, $lon) = split(";", $data[-1] );
  close(LOG);
  $lat =~ s/^0+//m;
  $lon =~ s/^0+//m;

#print "HTTP/1.1 200 OK\r\n";
print "Content-type: text/html\n\n";

print <<HTML;
<html>
<head>
<meta http-equiv="refresh" content="60">
<title>Tracking map of $asset</title>
    <style type="text/css">
      html, body, #basicMap {
          width: 100%;
          height: 100%;
          margin: 0;
      }
</style>
<script src="http://www.openlayers.org/api/OpenLayers.js"></script>
<script src="http://www.openstreetmap.org/openlayers/OpenStreetMap.js"></script>
<script type="text/javascript">
  var lat=$lat
  var lon=$lon
  var zoom=5
  var map; //complex object of type OpenLayers.Map

  function init() {
    map = new OpenLayers.Map ("map", {
      controls:[
        new OpenLayers.Control.Navigation(),
        new OpenLayers.Control.PanZoomBar(),
        new OpenLayers.Control.LayerSwitcher(),
        new OpenLayers.Control.Attribution()
      ],
      numZoomLevels: 19,
      units: 'm',
      projection: new OpenLayers.Projection("EPSG:900913"),
      displayProjection: new OpenLayers.Projection("EPSG:4326")
    });
 
    // Define the map layer
    layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
    map.addLayer(layerMapnik);
    layerCycleMap = new OpenLayers.Layer.OSM.CycleMap("CycleMap");
    map.addLayer(layerCycleMap);
    layerMarkers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(layerMarkers);

    var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
    map.setCenter(lonLat, zoom);
 
    var size = new OpenLayers.Size(21, 25);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon = new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png',size,offset);
    layerMarkers.addMarker(new OpenLayers.Marker(lonLat,icon));
  }
</script>
</head>
<body onload="init();">
 <div id="map"></div>
</body>
</html>
HTML
}
else {
  print "HTTP/1.1 500 Error\r\n";
}

