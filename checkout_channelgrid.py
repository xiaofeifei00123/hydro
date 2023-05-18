# %%
"""
河道网格, 设置可视化
"""
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmaps
import netCDF4 as nc
import wrf

# flnm = '/home/fengx20/project/hydro/test3/DATA/gis_50m/outputs/grid_nolake_20_1000/Fulldom_hires.nc'
# flnm = '/home/fengx20/project/hydro/test3/DATA/gis_100m/outputs/grid_nolake_10_200/Fulldom_hires.nc'
# flnm = '/home/fengx20/project/hydro/test3/DATA/gis_100m/outputs/grid_nolake_10_200/Fulldom_hires.nc'
# flnm = '/home/fengx20/project/hydro/src/Preprocess/HydroRouting/data/geo_em.d01.nc'
flnm = '/home/fengx20/project/hydro/src/Preprocess/HydroRouting/outputs/ctl/Fulldom_hires.nc'
# flnm = '/home/fengx20/project/hydro/src/Preprocess/HydroRouting/outputs/latlon.nc'
ds = xr.open_dataset(flnm)
db = ds['CHANNELGRID']
da = xr.where(db==-9999,np.nan, db)
dd = xr.where(da==0,0.00001, da)
da = dd


#%%
flnm_latlon = '/home/fengx20/project/hydro/src/Preprocess/HydroRouting/outputs/latlon.nc'
ds_latlon = xr.open_dataset(flnm_latlon)
lat = ds_latlon['LATITUDE'][::-1, :]
lon = ds_latlon['LONGITUDE'][:, ::-1]
# %%
fig = plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
crs = ax.scatter(lon,lat,da.values, color='blue')
fig.colorbar(crs)
fig.savefig('/home/fengx20/project/hydro/figure/channel_grid.png')