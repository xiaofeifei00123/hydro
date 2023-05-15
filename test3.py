# %%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmaps
import netCDF4 as nc
import wrf
from matplotlib import rcParams
import cartopy.crs as ccrs
import cartopy.crs as ccrs
# import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature
# from draw_domain_cartopy_weihe import draw_station
import netCDF4 as nc
# %%
flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
# flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon.nc'
# flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon_rtout.nc'
ds_latlon = xr.open_dataset(flnm_latlon)
ds_latlon
# lat = ds_latlon['LATITUDE']
# lon = ds_latlon['LONGITUDE']
lat = ds_latlon['LATITUDE'][::-1, :]
lon = ds_latlon['LONGITUDE'][:, ::-1]
# lon
# lon.shape
# lat = ds['LONGITUDE'].values

proj = ccrs.PlateCarree()  # 创建坐标系
fig = plt.figure(figsize=(4,3), dpi=300)
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], )
ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
# colordict = ['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']
colordict = ['green', 'red', 'blue', 'blue', 'black']
# crs = ax.contourf(lon,lat,da.values, cmap=cmaps.WhiteBlue, levels=[1*10**5, 5*10**5, 1*10**6, 1*10**7],colors=colordict,  zorder=2)
# crs = ax.contourf(lon,lat,da.values, levels=[1*10**5, 5*10**5, 1*10**6, 1*10**7],colors=colordict,  zorder=2)


# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/gis_100m/outputs/test2/Fulldom_hires.nc'
ds = xr.open_dataset(flnm)
ds
dd = ds['basn_msk']
db = xr.where(dd==-9999, np.nan,dd)
# db.plot(levels=6)
# db.max()

db.plot(colors=['blue', 'red', 'yellow', 'green', 'orange'], levels=5)

# crs = ax.contourf(lon,lat,db, levels=20, zorder=4, transform=ccrs.PlateCarree())
# db.plot()
# %%
flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140000.CHANOBS_DOMAIN1'
ds = xr.open_dataset(flnm)
ds.latitude.values
ds.longitude.values
#%%
flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHANOBS_DOMAIN1*'
ds = xr.open_mfdataset(flnm)
ds.load()
# %%
ds['streamflow'].isel(feature_id=1).plot()