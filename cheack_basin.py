# %%
import xarray as xr
import numpy as np
import pandas as pd

# %%
# flnm = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/Fulldom_hires.nc'
flnm = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/outputs/ctl/Fulldom_hires.nc'
ds = xr.open_dataset(flnm)
dd = ds['basn_msk']
db = xr.where(dd==-9999, 0,dd)
db.plot()
# %%
