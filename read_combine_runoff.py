#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
将地表产流和壤中流多时次数据进行合并处理

根据x,y的坐标进行插值处理，这里的x,y的值是从-290948到290951, 不是个数
-----------------------------------------
Time             :2023/03/23 12:02:08
Author           :Forxd
Version          :1.0
'''
# %%
import xarray as xr
import os
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
# %%


class Runoff():
    def __init__(self):
        pass
        # self.path = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/'
        # self.flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
        self.path = '/home/fengx20/project/hydro/test_ground/RUN/2002/'
        # self.flnm_latlon = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/wrf_hydro_gis_preprocessor/wrfhydro_gis/latlon.nc'
        self.flnm_latlon = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/outputs/latlon.nc'
        self.path_surface = self.path+'surface_runoff.nc'
        self.path_subsurface = self.path+'subsurface_runoff.nc'

    def get_latlon(self):
        ds_latlon = xr.open_dataset(self.flnm_latlon)
        self.lat = ds_latlon['LATITUDE']
        self.lon = ds_latlon['LONGITUDE'][:,::-1]
        return self.lon, self.lat

    def read_surface_runoff_1time(self,flnm_LSM):
        ds_LSM = xr.open_dataset(flnm_LSM)
        lon, lat = self.get_latlon()
        # lon1 = lon[::10, ::10]
        # lat1 = lat[::10, ::10]
        # lon1 = lon[::4, ::4]
        # lat1 = lat[::4, ::4]
        da = ds_LSM['sfcheadrt']
        db = ds_LSM['infxsrt']
        # db = xr.DataArray(
        #     da.values,
        #     coords={
        #         'lon':(('y','x'),lon1.values),
        #         'lat':(('y','x'),lat1.values),
        #         'y':da.y.values,
        #         'x':da.x.values,
        #         'time':da.time.values,
        #     },
        #     dims=['time', 'y', 'x']
        # )
        # db = db.rename('surface_runoff')
        ds = xr.Dataset(
            {
            "surface_runoff":(['time', 'y', 'x'],da.values),
            "infiltration":(['time','y', 'x'],db.values),
            },
            coords={
                'lon':(('y','x'),lon.values),
                'lat':(('y','x'),lat.values),
                'y':da.y.values,
                'x':da.x.values,
                'time':da.time.values,
            },
            # dims=['time', 'y', 'x']
        )
        # db = db.rename('surface_runoff')
        # return db
        return ds


    def read_subsurface_runoff_1time(self,flnm_RT):
        ds_RT= xr.open_dataset(flnm_RT)
        lon, lat = self.get_latlon()

        # lon1 = lon[::4, ::4]
        # lat1 = lat[::4, ::4]


        da = ds_RT['sfcheadsubrt']
        db = xr.DataArray(
            da.values,
            coords={
                'lon':(('y','x'),lon.values),
                'lat':(('y','x'),lat.values),
                'y':da.y.values,
                'x':da.x.values,
                'time':da.time.values,
            },
            dims=['time', 'y', 'x']
        )
        db = db.rename('subsurface_runoff')
        return db
    pass


    def combine_surface_runoff(self,):
        def get_file_list(path, keyvar):
            fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
            fl_list= fl_list.read().split()
            return fl_list

        # path = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/'
        surface = '*.LSMOUT_DOMAIN1'
        fl_list_surface = get_file_list(self.path, surface)
        # fl_list_surface

        # rf = Runoff()
        dss_list = []
        for fls in fl_list_surface:
            print(fls[-20:-10])
            dss = self.read_surface_runoff_1time(fls)
            dss_list.append(dss)
        das = xr.concat(dss_list, dim='time')
        das.to_netcdf(self.path_surface)


    def combine_subsurface_runoff(self,):
        def get_file_list(path, keyvar):
            fl_list= os.popen('ls {}/{}*'.format(path, keyvar))  # 打开一个管道
            fl_list= fl_list.read().split()
            return fl_list

        # path = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/'
        subsurface = '*.RTOUT_DOMAIN1'
        fl_list = get_file_list(self.path, subsurface)
        # fl_list

        # rf = Runoff()
        ds_list = []
        for fls in fl_list:
            print(fls[-20:-10])
            dss = self.read_subsurface_runoff_1time(fls)
            ds_list.append(dss)
        das = xr.concat(ds_list, dim='time')
        das.to_netcdf(self.path_subsurface)
        return dss
    

    def regrid_coarse2fine2d(self,da, db):
        """
        将河道网格的数据插值到陆面模式网格点
        da: 需要输出的较粗的网格分辨率的数据, xr.DataArray (y:417,x:582)
        db: 输入的精细网格分辨率的数据,xr.DataArray (y:4170,x:5820)
        return :
            dc: 同da网格
        """
        data = db.values
        y = db.y.values
        x = db.x.values
        ## 输入的格点
        interp = RegularGridInterpolator((y, x), data,
                                        bounds_error=False, fill_value=None)
        ## 输出的格点
        Y,X = np.meshgrid(da.y.values, da.x.values, indexing='ij')
        ## 插值
        ii = interp((Y,X))
        # dc = xr.DataArray(ii)
        dc = xr.DataArray(
            ii,
            coords=da.coords,
            dims= da.dims,
        )
        return dc

    def regrid_coarse2fine3d(self,da_subsurface, da_surface):
        ## 输入的格点
        data = da_subsurface.values
        y = da_subsurface.y.values
        x = da_subsurface.x.values
        tt = da_subsurface.time.values
        z = np.arange(len(tt))
        ## 规则网格的值
        interp = RegularGridInterpolator((z, y, x), data,
                                        bounds_error=True, fill_value=np.nan, method='linear')
        ## 输出的格点
        Z,Y,X = np.meshgrid(z, da_surface.y.values, da_surface.x.values, indexing='ij', sparse=True)
        # Z
        ## 插值
        da = interp((Z,Y,X))
        db = xr.DataArray(
            da,
            coords={
                'lon':(('y','x'),da_surface.lon.values),
                'lat':(('y','x'),da_surface.lat.values),
                'y':da_surface.y.values,
                'x':da_surface.x.values,
                'time':da_surface.time.values,
            },
            dims=['time', 'y', 'x']
        )
        db.rename('sub_surface')
        return db
    
    def combine_runoff(self,):
        # rf = Runoff()
        # da_subsurface = xr.open_dataarray(self.path_subsurface)  # 细网格
        ds_surface = xr.open_dataset(self.path_surface)  # 细网格
        # ds = ds_surface
        ds_subsurface = xr.open_dataset(self.path_subsurface)


        # ds1 = xr.open_dataset(flnm1)
        # ds2 = xr.open_dataset(flnm2)
        da_subsurface = ds_subsurface['subsurface_runoff']
        da_surface= ds_surface['surface_runoff']
        # rf = Runoff()
        dc = self.regrid_coarse2fine3d(da_subsurface, da_surface)
        dd = dc.rename('subsurface_runoff')
        ds_surface['subsurface_runoff'] = dd



        # ds['runoff_subsurface'] = da_subsurface
        # dc = rf.regrid_coarse2fine3d(da_subsurface, da_surface)
        # ds = xr.concat([da_surface, dc], pd.Index(['runoff_surface', 'runoff_subsurface'], name="model")).to_dataset(dim='model')
        self.path_runoff = '/home/fengx20/project/hydro/data/output/runoff_small.nc'
        ds_surface.to_netcdf(self.path_runoff)
        return ds_surface
# %%
rf = Runoff()
# rf.combine_subsurface_runoff()
rf.combine_surface_runoff()
# rf.combine_runoff()
# rf.regrid_coarse2fine3d()
# dss
# %%
# flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140000.LSMOUT_DOMAIN1'
# ds = xr.open_dataset(flnm)
# ds.y.values
# ds['']
# ds['sfcheadrt'].time.values
#%%
# fl_list_subsurface
    # dds_list = []
# %%
# lon1
