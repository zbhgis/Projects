var dataset = ee.ImageCollection(
  "projects/sat-io/open-datasets/gebco/gebco_grid",
);
var elevation = dataset.select("b1").mosaic();
var elevationVis = {
  min: -7000.0,
  max: 5000.0,
  palette: ["0000ff", "00ffff", "ffff00", "ff0000", "ffffff"],
};
Map.setCenter(-37.62, 25.8, 2);
Map.addLayer(elevation, elevationVis, "b1");

Export.image.toDrive({
  crs: "EPSG:4326",
  image: elevation,
  description: "GEBCO_Elevation",
  scale: 10000,
  maxPixels: 1e13,
});
