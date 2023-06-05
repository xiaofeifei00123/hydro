#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
求面平均降雨量
利用salem库的筛选数据的功能
注意的点是：
输入的强迫数据的格点不能够被salem直接识别，这里将其coords, dims, attrs替换为wrfinput中t2的格点属性
-----------------------------------------
Time             :2023/05/24 10:06:42
Author           :Forxd
Version          :1.0
'''


# %%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from baobao.map import select_area_data, select_area_data_shp
import salem
import os

# %%
def combien_precip(t2, keyvar='2003*.nc'):
    """合并多个时次的强迫降水数据,
    将它们的维度属性换为t2的

    Args:
        t2 (xr.DataArray): _description_

    Returns:
        _type_: _description_

    Example:
    flnm = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
    ds = salem.open_xr_dataset(flnm)
    t2 = ds['T2'].squeeze()
    """
    path = '/home/fengx20/project/hydro/test_ground/RainForcing/output/'
    # keyvar = '2003*.nc'
    fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
    fl_list= fl_list.read().split()
    da_list = []
    for fl in fl_list:
        ds = xr.open_dataset(fl)
        da = ds['precip_rate']
        strtime = fl.split('/')[-1].split('.')[0].split('_')[0]
        print(strtime)
        dc = xr.DataArray(
            da.squeeze().values,
            coords=t2.coords,
            dims=t2.dims,
            attrs=t2.attrs,
        )
        t = pd.to_datetime(strtime, format="%Y%m%d%H%M")
        dc.coords['time'] = t
        print(t)
        da_list.append(dc)
    ds2 = xr.concat(da_list, dim='time')
    ds2 = ds2*3600 ## 将降水从mm/s-->变为mm/h
    return ds2

def save_preicip_grid():
    flnm = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
    ds = salem.open_xr_dataset(flnm)
    t2 = ds['T2'].squeeze()

    time_list = np.arange(2004, 2012, 1)
    for i in time_list:
        key = str(i)+'*.nc'
        ds = combien_precip(t2,key)
        name = 'precip_'+str(i)+'.nc'
        flnm_save = '/home/fengx20/project/hydro/data/output/'+name
        ds.to_netcdf(flnm_save)
    

def save_precip_areamean():
    flnm_pr= '/home/fengx20/project/hydro/data/output/precip_2003.nc'
    db = xr.open_dataarray(flnm_pr)
    flnm = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
    ds = salem.open_xr_dataset(flnm)
    t2 = ds['T2'].squeeze()
    db.attrs = t2.attrs

    shp_list = ['linjiacun', 'weijiabao', 'wushan', 'qinan']
    var_list = ['Lin Jiacun', 'Wei Jiabao', 'Wu Shan', 'Qin An']
    i = 0
    ds_list = []
    for shp in shp_list:
        print(i)
        # fl_shp = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/all_basn.shp'
        fl_shp_path = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/basin/'
        fl_shp = fl_shp_path+shp+'.shp'
        tt2 = select_area_data_shp(db, fl_shp)    # t2_roi.salem.quick_map()
        da_p = tt2.mean(dim=['south_north', 'west_east'])
        da_p2 = da_p.resample(time='1d', label='left').sum()*3  # 因为之前的单位mm/h
        da_p2.name = var_list[i]
        ds_list.append(da_p2)
        i+=1

    ds = xr.merge(ds_list)
    flnm_pre = '/home/fengx20/project/hydro/src/data/precip_areamean_2003.nc'
    ds.to_netcdf(flnm_pre)
# %%
if __name__ == "__main__":
    pass
    # save_preicip_grid()
    save_precip_areamean()

