# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
# %%
# flnm = '/home/fengx20/project/hydro/test_ground/GLDAS/GLDAS_20020101.0000'
flnm = '/home/fengx20/project/hydro/test_case/croto_ny/FORCING/2011082604.LDASIN_DOMAIN1'
ds = xr.open_dataset(flnm)
ds
#%%
flnm = '/home/fengx20/project/hydro/test_ground/ERA5/test.nc'
ds = xr.open_dataset(flnm)
ds
#%%
ds['ciwc']



# %%

### 原始的2002 
flnm = '/home/fengx20/project/hydro/test_ground/RUN/200205020000.CHANOBS_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake_0710-0720/202207101800.CHRTOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
# ds['velocity'].max()
ds
# %%
# ds['infxsrt'].max()
ds['streamflow']

# %%

def get_streamflow():
    path = '/home/fengx20/project/hydro/test_ground/RUN/2003/'
    # keyvar = '200*.CHRTOUT_DOMAIN1'
    keyvar = '2003*.CHANOBS_DOMAIN1'

    # path = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake_0710-0720/'
    # keyvar = '20*.CHRTOUT_DOMAIN1'
    

    fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
    fl_list= fl_list.read().split()
    # fl_list
    # print(fl_list)
    ds_list = []
    for fl in fl_list:
        ds = xr.open_dataset(fl)
        ds = ds['streamflow']
        # ds = ds['velocity']
        ds_list.append(ds)
    ds2 = xr.concat(ds_list, dim='time')
    # db = ds2.mean(dim=['south_north', 'west_east'])
    # return db
    # return ds_list
    return ds2

db = get_streamflow()
db
# %%
db.isel(feature_id=2).plot()
#%%
# db.max(dim='feature_id').plot()
# db.mean(dim='station').plot()
# db.time
# db
# db


flnm = '/home/fengx20/project/hydro/test_ground/RUN/2003/200301010000.LSMOUT_DOMAIN1'
ds =xr.open_dataset(flnm)
ds

#%%
# ds.reference_time
def get_infiltration():
    path = '/home/fengx20/project/hydro/test_ground/RUN/2003/'
    keyvar = '200*.LSMOUT_DOMAIN1'
    fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
    fl_list= fl_list.read().split()
    fl_list
    ds_list = []
    for fl in fl_list[0:300]:
        ds = xr.open_dataset(fl)
        # ds = ds['infxsrt']
        ds = ds['sfcheadrt']
        ds_list.append(ds)
    ds2 = xr.concat(ds_list, dim='time')
    # db = ds2.mean(dim=['south_north', 'west_east'])
    # return db
    # return ds_list
    return ds2

db = get_infiltration()
db
# %%
db.max(dim=['y','x']).plot()
# %%
# len(db)
dc =  db.mean(dim=['y', 'x'])
dc
# %%
dc.plot()

# dc = xr.concat(db, dim='time')
# db.nbytes/(1024*1024)
# db[1].time
# %%
xr.set_options(display_style="html")
flnm_geo = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/geo_em.d01.nc'
geogrid = xr.open_dataset(flnm_geo)
geogrid
# %%
geogrid.HGT_M.plot()
# %%
geogrid.LU_INDEX.plot(cmap="tab20")
# %%
geogrid.SCT_DOM.plot(cmap="tab10")
# %%
flnm_dom= '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/Fulldom_hires.nc'
fulldom = xr.open_dataset(flnm_dom)
fulldom
# %%
fulldom.TOPOGRAPHY.plot(cmap="gist_earth")
#%%
fulldom.CHANNELGRID.plot()
# %%
# fulldom.LAKEGRID.plot()
flnm_soi= '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/soil_properties.nc'
soilprop = xr.open_dataset(flnm_soi)
soilprop
#%%
soilprop.smcmax.sel(soil_layers_stag = 0).plot(vmin=0.4, vmax=0.6, cmap="BuPu")
# %%
soilprop.hvt.plot(cmap="YlGn")
# %%
flnm_obs = '/home/fengx20/project/hydro/test_ground/RUN/2002/*CHANOBS*'
chanobs = xr.open_mfdataset(flnm_obs,
                            combine='by_coords')
# %%
chanobs['streamflow'].isel(feature_id=0).plot()

