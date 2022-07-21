import xarray as xr
import pandas as pd
import geopandas as gpd
import glob
import os

# table and coordinates:
table = pd.read_csv('morphometrical_params.csv', index_col = 0)

# .ncs
path = '/Users/varyabazilova/Desktop/era5land/temperature2m/'
lats = table.y_wgs
lons = table.x_wgs

subset = xr.Dataset()

for f in os.listdir(path):
    # read every file: 
    ds = xr.open_dataset(os.path.join(path, f), decode_coords="all")
    # select the coordinates: 
    ds_sel = ds.sel(longitude=lons, latitude=lats, method='nearest')
    # merge all back together 
    subset = xr.merge([subset, ds_sel])
    
subset.to_netcdf('/Users/varyabazilova/Desktop/era5land/temperature2m/temp2m_1990_2021_points.nc')
