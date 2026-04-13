var dataset = ee.ImageCollection("COPERNICUS/DEM/GLO30");
var elevation = dataset.select("DEM").mosaic();
var elevationVis = {
  min: 0.0,
  max: 1000.0,
  palette: ["0000ff", "00ffff", "ffff00", "ff0000", "ffffff"],
};
Map.setCenter(-6.746, 46.529, 4);
Map.addLayer(elevation, elevationVis, "DEM");
Export.image.toDrive({
  crs: "EPSG:4326",
  image: elevation,
  description: "WORLD_Elevation",
  scale: 10000,
  maxPixels: 1e13,
});
