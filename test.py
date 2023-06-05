# %%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from draw_stream_distribution import draw_stream
import cmaps
%load_ext autoreload
%autoreload 2

# %%
# flnm = ''
flnm1 = '/home/fengx20/project/hydro/test_ground/WPS/geo_em.d01.nc'
flnm2 = '/home/fengx20/project/hydro/test_ground/WPS/geo_em.d01.nc.back_soil_type'
ds1 = xr.open_dataset(flnm1)
ds2 = xr.open_dataset(flnm2)
# %%
# da = ds['SOILCTOP'].isel(soil_cat=2)
# da1 = ds1['SOILCBOT'].isel(soil_cat=10)
da2 = ds2['SOILCBOT'].isel(soil_cat=8)
# da
# da.max()
# da1.plot()
# da1.plot(levels=[1,])
da2.plot()
# %%
# da2
def get_cat(flnm2):
    ds2 = xr.open_dataset(flnm2)
    # db = ds2['SOILCBOT'].squeeze()
    db = ds2['SOILCBOT'].squeeze()
    dc = db
    for i in db.soil_cat:
        da = db.sel(soil_cat=i).squeeze()
        # print(da)
        dc[i,:,:] = da*i
    # db.plot()
    dd = dc.sum(dim='soil_cat')
    return dd
dd1 = get_cat(flnm1)
dd2 = get_cat(flnm2)
# %%
# dd2.plot(levels=np.arange(1,15), cmap=cmaps.amwg)
dd1.plot(levels=np.arange(1,15), cmap=cmaps.amwg)
# da.min()
# da.mean()
# %%


# %%
### 先看陆面模式的降水匹配不匹配
flnm_P = '/home/fengx20/project/hydro/data/output/precip_2003.nc'
dap = xr.open_dataarray(flnm_P)
dap
# %%
dap.sel(time='2003-07-31').max()
# %%
precip_sum = dap.sel(time='2003-08').sum(dim='time')
precip_sum
# %%

(precip_sum*3).plot(levels=[0, 50, 100, 200, 300, 400, 100000], colors=['white', 'green', 'blue','yellow','orange','red'])


# %%
flnm_sim1 = '/home/fengx20/project/hydro/src/data/frxst.nc'
ds = xr.open_dataset(flnm_sim1)
ds

# %%
### 陆面模式的产流和下渗
## 格点和WRF格点一样

flnm_RT = '/home/fengx20/project/hydro/test_ground/RUN/LSM/200308300000.LDASOUT_DOMAIN1'
flnm_RT0 = '/home/fengx20/project/hydro/test_ground/RUN/LSM/200307310000.LDASOUT_DOMAIN1'
ds_RT = xr.open_dataset(flnm_RT)
ds_RT0 = xr.open_dataset(flnm_RT0)
ds_RT
# %%
(ds_RT['RAINRATE']*3600).max()
# %%

# (ds_RT['ACCPRCP'].squeeze()-ds_RT0['ACCPRCP'].squeeze()).plot(levels=[0, 50, 100, 200, 300, 400])
# (ds_RT['ACCEDIR'].squeeze()-ds_RT0['ACCEDIR'].squeeze()).plot(levels=[0, 50, 100, 200, 300, 400])
def caculate_sumwater(ds):
    var_list = ['ACCECAN', 'ACCEDIR', 'ACCETRAN']
    da = 0
    for var in var_list:
        da = da+ds[var]
    return da
da0 = caculate_sumwater(ds_RT0)
da0
# %%
da1 = caculate_sumwater(ds_RT)
da1
# %%
dd = da1.squeeze()-da0.squeeze()
dd
# %%
dd.plot(levels=[0, 50, 100, 200, 300, 400, 100000], colors=['white', 'green', 'blue','yellow','orange','red'])
# %%
levels=[0, 50, 100, 200, 300, 400, 100000]
colors=['white', 'green', 'blue','yellow','orange','red']
# %%

# %%
# da0 = caculate_sumwater(ds_RT0)
# da0
(ds_RT['UGDRNOFF'].squeeze()-ds_RT0['UGDRNOFF'].squeeze()).plot(levels=levels, colors=colors)
# %%
(ds_RT['ACCPRCP'].squeeze()-ds_RT0['ACCPRCP'].squeeze()).plot(levels=levels, colors=colors)


# %%
### CHRTOUT_DOMAIN
flnm_CH = '/home/fengx20/project/hydro/test_ground/RUN/200309010000.CHRTOUT_DOMAIN1'
ds_CH = xr.open_dataset(flnm_CH)
da = ds_CH['streamflow']
lon = da.longitude
lat = da.latitude
draw_stream(da, lon, lat)

# %%
### RTOUT_DOMAIN
flnm_RT = '/home/fengx20/project/hydro/test_ground/RUN/200309150000.RTOUT_DOMAIN1'
ds_RT = xr.open_dataset(flnm_RT)
ds_RT
da = ds_RT['sfcheadsubrt'].squeeze()
da.max()
# %%
da = ds_RT['zwattablrt'].squeeze()
# %%
# flnm_wrf = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
flnm_wrf = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/Fulldom_hires.nc'
ds = xr.open_dataset(flnm_wrf)
ds
# %%
lat = ds.LATITUDE.squeeze()
lon = ds.LONGITUDE.squeeze()
# da
# %%
# da.shape
da[::10,::10].plot()
# lon.shape
# da.shape

# %%
# lon = da.longitude
# lat = da.latitude
draw_stream(da.squeeze(), lon, lat)



# %%
# flnm_save = '/home/fengx20/project/hydro/src/data/frxst1.nc'
# ds = xr.open_dataset(flnm_save)
# ds['Wu Shan'].max()
flnm_P = '/home/fengx20/project/hydro/data/output/precip_2003.nc'
dsp = xr.open_dataarray(flnm_P)
dsp
# %%
dsp.sel(time=slice('2003-09-15 00', '2003-09-16 00')).sum(dim='time').plot()
#