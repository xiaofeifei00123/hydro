# %%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmaps
import netCDF4 as nc
import wrf
# %%
## 可以看到基本的routing 路径
flnm = '/home/fengx20/project/hydro/test3/DATA/gis_50m/outputs/grid_nolake_20_200/Fulldom_hires.nc'
ds = xr.open_dataset(flnm)
da = ds['FLOWACC']  # 累积的格点数
da.plot()
# da.max()
# %%
### 通过Fulldomhires.nc文件生成的经纬度信息

#  Build_Spatial_Metadata_File.py
# flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon.nc'
flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon.nc'
ds_latlon = xr.open_dataset(flnm_latlon)

lat = ds_latlon['LATITUDE'][::-1, :]
lon = ds_latlon['LONGITUDE'][:, ::-1]
lon.shape
# %%

fig = plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
crs = ax.contourf(lon,lat,da.values, cmap=cmaps.WhiteBlue, levels=100)
fig.colorbar(crs)
fig.savefig('/home/fengx20/project/hydro/Draw/figure/flow_acc.png')