// created by: varyabazilova 
// readme: choose the month based on cloud probability (november seems better)
//         calculate ndvi for all november images
//         take the median ndvi
//         clip with the catchment polygons
//         export the raster layer 
//         make vector file of it in qgis
//         calculate the area and polygon stats 


// ---------------------------
// ---- cloud probability ----
// ---------------------------

// choose month based on the cloud probability 
var clouds = ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY").filterBounds(hma_regions)

var clouds_oct = clouds.filter(ee.Filter.calendarRange(10, 10,'month')).median()
var clouds_nov = clouds.filter(ee.Filter.calendarRange(11, 11,'month')).median()

var clouds_diff = clouds_oct.subtract(clouds_nov)
print(clouds_diff)

// visualization
var palettes = require('users/gena/packages:palettes')
var palette = palettes.crameri.acton[10]

// Map.addLayer(clouds_oct.clip(hma_regions), {min: 0, max: 100, palette: palette}, 'cloud probability oct');
// Map.addLayer(clouds_nov.clip(hma_regions), {min: 0, max: 100, palette: palette}, 'cloud probability nov');
// Map.addLayer(clouds_diff.clip(hma_regions), {/*min: 0, max: 100, palette: palette*/}, 'cloud probability diff');


// ---------- test: import HMA regions 

print(hma_regions)




// ---------------------------
//   ---- ndvi mapping ----
//   ---- sentinel 2   ----  
// ---------------------------

// ndvi function: nir - red

var ndvi = function(img) {
  var ndvi_band = img.normalizedDifference(['B8', 'B4']).rename('ndvi');   // NIR and red - NDVI
  return img.addBands(ndvi_band); };

// sentinel 2 
var sent2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(hma_regions)
                                                             .map(ndvi)

var october  = sent2.filter(ee.Filter.calendarRange(10, 10,'month'))
var november = sent2.filter(ee.Filter.calendarRange(11, 11,'month'))

var ncc = {min: 0.0, max: 3000, bands: ['B4', 'B3', 'B2']};
var fcc = {min: 0.0, max: 3000, bands: ['B8', 'B4', 'B3']};



// ---------------------------
//      ---- visual ----
// ---------------------------

// ----- map october -----
// Map.addLayer(october.median(), ncc, 'sent2 median ncc oct')
// Map.addLayer(october.median(), fcc, 'sent2 median fcc oct')
// Map.addLayer(october.select('ndvi').median(), {min: -1, max: 1}, 'ndvi oct')

// ----- map november -----
// Map.addLayer(november.median(), ncc, 'sent2 median ncc nov')
// Map.addLayer(november.median(), fcc, 'sent2 median fcc nov')
// Map.addLayer(november.select('ndvi').median().clip(nepal), {min: -1, max: 1}, 'ndvi nov')



// ---------------------------
//  ---- vegetation mask ----
// ---------------------------

// mask out the values of ndvi lower then the threshold

var ndvi_band = november.select('ndvi').median().gte(0.2)
// var vegetation_mask = november.select('ndvi').median().select('ndvi').gt(0.24);
var vegetation = november.median().updateMask(ndvi_band)

// Map.addLayer(vegetation_mask.clip(nepal), {}, 'vegetation > 0.24 bool')
Map.addLayer(vegetation.clip(nepal), fcc, 'vegetation > 0.20')


// ---------------------------
//   ---- export raster ----
// ---------------------------

// // Export the image, specifying the CRS, transform, and region.
// Export.image.toDrive({
//   image: landsat,
//   description: 'imageToDriveExample_transform',
//   crs: projection.crs,
//   crsTransform: projection.transform,
//   region: geometry
// });

















