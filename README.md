Points In Poygons
===============================================================================

Script performs point-in-polygon (PIP) for multiple points and multiple polygons 
(raster tile index) and updates the points shapefile with the pixel value from 
the correct raster.

## Dependencies:
 * [GDAL](http://www.gdal.org/), must also be in the `PATH`
 * [libspatialindex](https://libspatialindex.github.io/)

## Install & Setup:
```
$ git clone git@github.com:dmofot/pnts_n_polys.git
$ cd pnts_n_polys
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Inputs:
 * _points_shapefile_ (in EPSG 4326) - `input_pnts.shp`
 * _input_rasters_ OR _raster_tile_index_ - `./tiles/*.tif` OR `tile_index_4326.shp`

## Outputs:
 * _points_updated_shapefile_ - `input_pnts_updated.shp`
 * _raster_tile_index_ - `tile_index_4326.shp`

## Examples:
```
$ python pnts_n_polys.py ./test/test_index_pnts_4326.shp ./test/tiles/*.tif
Loading rasters into tile_index_4326.shp...
Creating new index file...
Loading points from ./test/test_index_pnts_4326.shp...
Building spatial index...
Checking if points are in polygons...
Progress: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:01<00:00, 93.51pnts/s]
Saving updates to ./test/test_index_pnts_4326_updated.shp...
```
```
$ python pnts_n_polys.py ./test/test_index_pnts_4326.shp ./test/tile_index_4326.shp
Loading raster tile index ./test/tile_index_4326.shp...
Loading points from ./test/test_index_pnts_4326.shp...
Building spatial index...
Checking if points are in polygons...
Progress: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:01<00:00, 96.31pnts/s]
Saving updates to ./test/test_index_pnts_4326_updated.shp...
```
