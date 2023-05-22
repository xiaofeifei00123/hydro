# %%
import xarray as xr
import pandas as pd

# %%


flnm = '/home/fengx20/project/hydro/test_ground/RUN/2002/200201040000.CHRTOUT_DOMAIN1'
ds = xr.open_dataset(flnm)