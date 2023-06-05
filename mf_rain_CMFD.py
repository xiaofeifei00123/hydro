"""
利用CMFD降水数据, 制作降水强迫数据,
1. 重新插值到WRF格点上
2. 换算单位为mm/s
"""
# %%
import xarray as xr
import pandas as pd
import numpy as np
import xesmf as xe
import os

# %%


#%%
def create_regrider(ds_PR, ds_LD, fl_regrid = '/home/fengx20/project/hydro/test_ground/RainForcing/regrider.nc'):
    if os.path.exists(fl_regrid):
        print('yes')
        regridder = xe.Regridder(ds_PR, ds_LD,'bilinear',weights=fl_regrid)
    else:
        print('no exist regrider')
        regridder = xe.Regridder(ds_PR, ds_LD, "bilinear")  # 构建插值器
        regridder.to_netcdf(fl_regrid)
    return regridder




def regird_one(flnm_LD, flnm_PR):

    ds_LD = xr.open_dataset(flnm_LD)
    ds_PR = xr.open_dataset(flnm_PR)
    # ds_PR



    regrider = create_regrider(ds_PR, ds_LD)
    ds2 = regrider(ds_PR)  # 插值
    ds3 = ds2/3600
    ds3 = ds3.rename({'time':'Time', 'prec':'precip_rate'})
    path = '/home/fengx20/project/hydro/test_ground/RainForcing/output/'
    for t in ds3.Time:
        dss = ds3.sel(Time=t).expand_dims('Time')
        ft = str(t.dt.strftime('%Y%m%d%H%M.PRECIP_FORCING.nc').values)
        print(ft)
        fs = os.path.join(path, ft)  # file_save
        dss.to_netcdf(fs)

if __name__ == "__main__":
    flnm_LD = '/home/fengx20/project/hydro/test_ground/MetForcing/output_files/2000010103.LDASIN_DOMAIN1'
    # flnm_PR = '/home/fengx20/project/hydro/test_ground/RainForcing/CMFD_precip/prec_ITPCAS-CMFD_V0106_B-01_03hr_010deg_200203.nc'
    # path = '/home/fengx20/project/hydro/test_ground/RainForcing/CMFD_precip/'
    path = '/home/fengx20/project/hydro/test_ground/RainForcing/CMFD_precip/'
    keyvar = '*2003*.nc'
    fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
    fl_list= fl_list.read().split()
    for fl in fl_list:
        regird_one(flnm_LD, fl)
# fl_list
# return fl_list
#%%

# path = '/home/fengx20/project/hydro/test_ground/RainForcing/output/'
# # keyvar = '2009*'
# for keyvar in ['2010*', '2011*', '2012*']:

#     fl_list= os.popen('ls {}/{}'.format(path, keyvar))  # 打开一个管道
#     fl_list= fl_list.read().split()

#     for fl in fl_list:
#         a, b, c = fl.split('.')
#         d = 'PRECIP_FORCING'
#         newname = a+'.'+d+'.'+c
#         # print(newname)
#         os.system('mv %s %s'%(fl, newname))
#     print('yes')
#     # print(fl)
#     # regird_one(flnm_LD, fl)
#     # ft = str(t.dt.strftime('%Y%m%d%H%M.PRECIP_FORCING.nc').values)
