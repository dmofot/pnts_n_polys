"""Points in Polygons."""

from subprocess import Popen, PIPE
from os import environ
from sys import argv
from shutil import copy
from shapefile import Reader, Writer
from shapely.geometry import Polygon, Point
from rtree import index
from tqdm import trange

# Grab inputs
sf = argv[1]
tidx = argv[2]

# Exit script if PATH doesn't contain GDAL
if 'GDAL' not in environ.get('PATH'):
    exit("Script requires GDAL.  Please install.")

# Create and/or load the shapefile of polygons and convert it to shapely polygon objects
if tidx[-4:] == '.tif':
    print("Loading rasters into tile_index_4326.shp...")
    proc = Popen(['gdaltindex', '-t_srs', 'EPSG:4326', 'tile_index_4326.shp', tidx])
    proc.communicate()
    polys_sf = Reader('tile_index_4326.shp')
else:
    print("Loading raster tile index %s..." % tidx)
    polys_sf = Reader(tidx)
polys_shp = polys_sf.shapes()
polys_rec = polys_sf.records()
polys_pnt = [q.points for q in polys_shp]
polys = [Polygon(q) for q in polys_pnt]

# Load the shapefile of points and convert it to shapely point objects
print("Loading points from %s..." % sf)
pnts_sf = Reader(sf)
pnts_shp = pnts_sf.shapes()
pnts_rec = pnts_sf.records()
pnts_xy = [q.points[0] for q in pnts_shp]
pnts = [Point(q.points[0]) for q in pnts_shp]

# Create a new shapefile in memory, copy existing pnts, and add new field
wpnts = Writer()
wpnts.fields = list(pnts_sf.fields)
wpnts.field('classification', 'F', 10, 10)

# Build a spatial index based on the bounding boxes of the polygons
print("Building spatial index...")
idx = index.Index()
count = -1
for q in polys_shp:
    count += 1
    idx.insert(count, q.bbox)

# Assign one or more matching polygons to each point
print("Checking if points are in polygons...")
for i in trange(len(pnts), desc='Progress', unit='pnts'):  # Iterate through each point
    pnts_rec[i].append(None)
    # Iterate only through the bounding boxes which contain the point
    for j in idx.intersection(pnts_xy[i]):
        # Verify that point is within the polygon itself not just the bounding box
        if pnts[i].within(polys[j]):
            result = Popen(['gdallocationinfo', '-valonly', '-wgs84',
                           str(polys_rec[j][0]), str(pnts_xy[i][0]), str(pnts_xy[i][1])],
                           stdout=PIPE)
            rout, rerr = result.communicate()
            pnts_rec[i][1] = rout
            break
        # Add record to new shapefile
        wpnts.records.append(pnts_rec[i])

# Copy geometry and save shapefile
print("Saving updates to %s_updated.shp..." % sf[:-4])
copy('%sprj' % sf[:-3], '%s_updated.prj' % sf[:-4])
wpnts._shapes.extend(pnts_sf.shapes())
wpnts.save("%s_updated.shp" % sf[:-4])
