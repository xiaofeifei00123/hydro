# %%
import xarray as xr
# %%
flnm = '/home/fengx20/project/hydro/test_ground/RUN/2002/*CHRTOUT_GRID1'
ds = xr.open_mfdataset(flnm)
# %%
ds.load()
# %%
# ds['streamflow'].plot()
ds['streamflow'].sum(dim='time').plot()
# %%
aa = ds['streamflow'].mean(dim='time')
print(aa)
# %%
cc = aa[::20, ::20]
cc
# %%
cc.load()
# %%
# cc.plot()
# dd = cc.values
# cc.max()