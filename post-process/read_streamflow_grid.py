# %%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
#%%
# %%
def get_latlon():
    flnm_f = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/outputs/ctl/Fulldom_hires.nc'
    dsf = xr.open_dataset(flnm_f)
    lat = dsf['LATITUDE']
    lon = dsf['LONGITUDE']
    return lat, lon
#%%
# ds.sel(feature_id=3800)
# ds.feature_id.max()
# ds

def read_stream_1time(flnm, lon, lat):
    ds = xr.open_dataset(flnm)
    da = ds['streamflow']
    db = xr.DataArray(
        da.values,
        coords={
            'lon':(('south_north','west_east'),lon.values),
            'lat':(('south_north','west_east'),lat.values),
            'south_north':da.y.values,
            'west_east':da.x.values,
            'time':da.time.values,
        },
        dims=['time', 'south_north', 'west_east']
    )
    return db




# %%


def save_grid():

    
    path = '/home/fengx20/project/hydro/test_ground/RUN/2002/'
    fl_list = os.popen('ls {}/*CHRTOUT_GRID1'.format(path))  # 打开一个管道
    fl_list = fl_list.read().split()
    # fl_list[0]
    lat, lon = get_latlon() 
    da_str_list = []
    for fl in fl_list:
        print(fl)
        da = read_stream_1time(fl, lat=lat, lon=lon)
        da_str_list.append(da)

    ds = xr.concat(da_str_list, dim='time')
    ds = ds.to_dataset(name='streamflow')
    flnm_stream = '/home/fengx20/project/hydro/data/output/'+'streamflow_grid.nc'
    ds.to_netcdf(flnm_stream)
# %%
def save_domain():

    
    path = '/home/fengx20/project/hydro/test_ground/RUN/2002/'
    fl_list = os.popen('ls {}/*CHRTOUT_DOMAIN1'.format(path))  # 打开一个管道
    fl_list = fl_list.read().split()
    # fl_list[0]
    lat, lon = get_latlon() 
    da_str_list = []
    for fl in fl_list:
        print(fl)
        dsd = xr.open_dataset(fl)
        db = xr.Dataset()
        db['stramflow'] = dsd['streamflow']
        db['q_lateral'] = dsd['q_lateral']
        db['time'] = dsd['time']
        da_str_list.append(db)

    ds = xr.concat(da_str_list, dim='time')
    # ds = ds.to_dataset(name='streamflow')
    flnm_stream = '/home/fengx20/project/hydro/data/output/'+'streamflow_domain.nc'
    ds.to_netcdf(flnm_stream)
# %%
if __name__ == "__main__":
    save_domain()
    # save_grid()
    
# %%
def get_restart_accsumrain():
    path = '/home/fengx20/project/hydro/test_ground/RUN/2002/'
    keyvar = 'RESTART.2002*DOMAIN1'
    fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
    fl_list= fl_list.read().split()
    fl_list
    ds_list = []
    for fl in fl_list:
        ds = xr.open_dataset(fl)
        ds = ds['ACCPRCP']
        strtime = fl.split('/')[-1].split('.')[-1].split('_')[0]
        t = pd.to_datetime(strtime, format="%Y%m%d%H")
        ds.coords['time'] = t
        ds_list.append(ds)
    ds2 = xr.concat(ds_list, dim='time')
    db = ds2.mean(dim=['south_north', 'west_east'])
    return db
#%%
db = get_restart_accsumrain()
db.plot()