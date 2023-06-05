# %%
import numpy as np
import pandas as pd
from datetime import datetime
from netCDF4 import Dataset
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
from matplotlib.colors import ListedColormap
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import shapely.geometry as sgeom
import cmaps
from glob import glob
from copy import copy
from wrf import to_np, getvar,get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords

import warnings
warnings.filterwarnings('ignore')
# %%
# ds = xr.open_dataset('/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc')
# ds.LANDUSEF
# landuse = ds.LU_INDEX
ncfile = Dataset('/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc')
landuse = getvar(ncfile, 'LU_INDEX')
lats, lons = latlon_coords(landuse)
cart_proj = get_cartopy(landuse)
# cm, labels = LU_MODIS21()
# %%
fig = plt.figure(figsize=(12,8))

# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Use the data extent
ax.set_xlim(cartopy_xlim(landuse))
ax.set_ylim(cartopy_ylim(landuse))

# Plot data
im = plt.pcolormesh(to_np(lons), to_np(lats), to_np(landuse), vmin=1, vmax=len(labels)+1, 
                    cmap=cm, transform=ccrs.PlateCarree())

cbar = plt.colorbar(ax=ax, shrink=1)
cbar.set_ticks(np.arange(1.5,len(labels)+1))
cbar.ax.set_yticklabels(labels)

# Add the gridlines
ax.gridlines(color="black", linestyle="dotted")

# add xticks and yticks
xticks = list(np.arange(100,155,5))
yticks = list(np.arange(10,55,5))
fig.canvas.draw()
ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
lambert_xticks(ax, xticks)
lambert_yticks(ax, yticks)
# Set the labelsize
plt.tick_params(labelsize=15)
# Add title
plt.title('LAND USE', fontsize=15)
print('土地利用绘制完毕')