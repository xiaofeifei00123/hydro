# %%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# import xesmf as xe
# import esmpy



# %%
flnm = '/home/fengx20/project/hydro/test3/RUN/route_new_cmorph/*CHANOBS*'
# flnm  = '/home/fengx20/project/hydro/test3/RUN/route_01/*CHANOBS*'
ds = xr.open_mfdataset(flnm)
ds.load()
# %%
ds.isel(feature_id=2)['streamflow'].plot()
# %%
flnm1 = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/output_files/202207100000.PRECIP_FORCING.nc'
flnm2 = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/200812100000.PRECIP_FORCING.nc'
ds1 = xr.open_dataset(flnm1)
ds2 = xr.open_dataset(flnm2)
#%%
ds1['precip'].Time






# %%  原始的降水数据
# flnm = 

flnm = '/home/fengx20/project/hydro/test3/DATA/rain/data/Z_NAFP_C_BABJ_20220714020018_P_CLDAS_NRT_ASI_0P0625_HOR-PRE-2022071202.nc'
ds = xr.open_dataset(flnm)
ds['PRCP'].max()

# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/input_files/GLDAS_NOAH025_3H.A20220714.0100.021.nc4'
ds = xr.open_dataset(flnm)
ds['PRCP'].lon.values[4] - ds['PRCP'].lon.values[3]

# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/output_files/2022071407.PRECIP_FORCING.nc'
ds = xr.open_dataset(flnm)
ds['precip_rate'].shape


# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/input_files_new/GLDAS_NOAH025_3H.A20220710.0100.021.nc4'
ds = xr.open_dataset(flnm)
ds['PRCP'].lat
# ds.drop_vars(names='*')
# (ds.data_vars.values)

# %%
flnm_gldas_input = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
ds_gldas_input = xr.open_dataset(flnm_gldas_input)
ds_gldas_input['Rainf_f_tavg']

flnm_gldas_output = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/output_files/2022071000.LDASIN_DOMAIN1'
ds_gldas_output = xr.open_dataset(flnm_gldas_output)
ds_gldas_output['RAINRATE']

## forcing precip output
flnm3 = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/2008121000.LDASIN_DOMAIN1'
ds_precip_output = xr.open_dataset(flnm3)
ds_precip_output['RAINRATE']

## forcing precip output
# flnm = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/200812100000.PRECIP_FORCING.nc'
# %%
flnm_precip = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/200812100300.PRECIP_FORCING.nc'
ds_precip = xr.open_dataset(flnm_precip)
ds_precip['precip'].shape
# ds['precip']

# %%
# flnm = '/home/fengx20/project/hydro/test3/DATA/rain/data/Z_NAFP_C_BABJ_20220712000038_P_CLDAS_NRT_ASI_0P0625_HOR-PRE-2022071000.nc'
# ds = xr.open_dataset(flnm)
# ds#['']

# %%

# %%
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/output_files/2022071009.LDASIN_DOMAIN1'
# ds = xr.open_dataset(flnm)
# # %%
# ds['RAINRATE']

# # %%
# flnm_in = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files/GLDAS_NOAH025_3H.A20220710.0600.021.nc4'
# ds_gldas = xr.open_dataset(flnm_in)
# # %%
# (ds_in['Rainf_f_tavg']*3600).plot()
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/GLDAS2WRFHydro_weight_bilinear.nc'
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/GLDAS2WRFHydro_weight_bilinear.nc'
ds = xr.open_dataset(flnm)
# ds['yc_a'].max()
ds.max()

# %%
flnm_rain = '/home/fengx20/project/hydro/test3/DATA/rain/data/Z_NAFP_C_BABJ_20220712010255_P_CLDAS_NRT_ASI_0P0625_HOR-PRE-2022071001.nc'
flnm_rain = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
ds_rain = xr.open_dataset(flnm_rain)
# ds_rain['PRCP'].isel(time=10).lat.values[10]
# ds_rain['PRCP'].LAT.values[10]
### 60 - 160 , 0-65


# # %%
# def regrid_xesmf(dataset, area):
#     """利用xESMF库，将非标准格点的数据，插值到标准格点上去, wrf插值到latlon
#     注意：dataset的coords, lat,lon 必须同时是一维或是二维的
#     Args:
#         dataset ([type]): Dataset格式的数据, 多变量，多时次，多层次
#         area, 需要插值的网格点范围, 即latlon坐标的经纬度范围
#         rd: 数据保留的小数位
#     """
#     ## 创建ds_out, 利用函数创建,这个东西相当于掩膜一样
#     ds_regrid = xe.util.grid_2d(area['lon1']-area['interval']/2, 
#                                 area['lon2'], 
#                                 area['interval'], 
#                                 area['lat1']-area['interval']/2, 
#                                 area['lat2'],
#                                 area['interval'])
#     #ds_regrid = xe.util.grid_2d(area['lon1'], area['lon2'], area['interval'], area['lat1'], area['lat2'], area['interval'])
#     # ds_regrid = xe.util.grid_2d(110, 116, 0.05, 32, 37, 0.05)
#     regridder = xe.Regridder(dataset, ds_regrid, 'bilinear')  # 好像是创建了一个掩膜一样
#     ds_out = regridder(dataset)  # 返回插值后的变量

#     ### 重新构建经纬度坐标
#     lat = ds_out.lat.sel(x=0).values.round(3)
#     lon = ds_out.lon.sel(y=0).values.round(3)
#     # ds_1 = ds_out.drop_vars(['lat', 'lon']).round(rd)  # 可以删除variable和coords
#     ds_1 = ds_out.drop_vars(['lat', 'lon'])  # 可以删除variable和coords

#     ## 设置和dims, x, y相互依存的coords, 即lat要和y的维度一样
#     ds2 = ds_1.assign_coords({'lat':('y',lat), 'lon':('x',lon)})
#     # ## 将新的lat,lon, coords设为dims
#     ds3 = ds2.swap_dims({'y':'lat', 'x':'lon'})
#     ## 删除不需要的coords
#     # ds_return = ds3.drop_vars(['XTIME'])
#     ds_return = ds3
#     return ds_return

# %%

# ds_out = xr.Dataset(
#     {
#         "lat": (["lat"], np.arange(16, 75, 1.0), {"units": "degrees_north"}),
#         "lon": (["lon"], np.arange(200, 330, 1.5), {"units": "degrees_east"}),
#     }
# )

# %%

# flnm_in = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files/GLDAS_NOAH025_3H.A20220710.0600.021.nc4'
# ds_gldas = xr.open_dataset(flnm_in)

# # %%
# ## 60-160 , 0-65
# ds_gldas.lat.values
# # %%

# lon = np.arange(70, 150, 0.25).round(3)
# lon
# import xesmf as xe

# %%
# ds_out = xr.Dataset(
#     {
#         "lat": (["lat"], ds_gldas.lat.values, {"units": "degrees_north"}),
#         "lon": (["lon"], ds_gldas.lon.values, {"units": "degrees_east"}),
#     }
# )
# ds_out
# ds_rain
# %%
flnm_rain = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
ds_rain = xr.open_dataset(flnm_rain)
ds = ds_rain
ds_out = xe.util.grid_2d(70, 150, 0.25, 5, 60, 0.25)
# regridder = xe.Regridder(ds, ds_out, "conservative")
regridder = xe.Regridder(ds, ds_out, "bilinear")
# %%
da = regridder(ds['PRCP'])
print(da.max())
# %%
# da.max()
# da.time
# import xesmf as xe

# fl = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_old/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
# ds = xr.open_dataset(fl)
# t =ds.time
# db = da.sel(time=t)/3600
# ds['Rainf_f_tavg'].values = db.values
# ds['Rainf_f_tavg'].max()

# %%
# db.max()
# ds.to_netcdf(fl)
# da.time


# ### 插值器构建，将观测降水插值
def regrid_rain():
    flnm_gldas = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_old/GLDAS_NOAH025_3H.A20220710.0600.021.nc4'
    ds_gldas = xr.open_dataset(flnm_gldas)
    ds_gldas.lat.values.round(3)
    # ds_out = xr.Dataset(
    #     {
    #         "lat": (["lat"], ds_gldas.lat.values, {"units": "degrees_north"}),
    #         "lon": (["lon"], ds_gldas.lon.values, {"units": "degrees_east"}),
    #     }
    # )
    ds_out = xe.util.grid_2d(70, 150, 0.25, 5, 60, 0.25)
    flnm_rain = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
    ds_rain = xr.open_dataset(flnm_rain)
    ds = ds_rain
    regridder = xe.Regridder(ds, ds_out, "conservative")
    da = regridder(ds['PRCP'])

    ### 修改文件gldas文件中降水
    path_old = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_old/'
    path_new = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_new/'
    fl_list = os.popen('ls {}/*.nc4'.format(path_old))  # 打开一个管道
    fl_list = fl_list.read().split()

    for fl in fl_list:
        ds = xr.open_dataset(fl)
        t =ds.time
        db = da.sel(time=t)/3600
        ds['Rainf_f_tavg'].values = db.values
        # ds['Rainf_f_tavg'].max()
        fnew = fl.split('/')[-1]
        print(fnew)
        fl_new = path_new + fnew
        ds.to_netcdf(fl_new)
# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
ds = xr.open_dataset(flnm)
ds

# %%
# ds['Rainf_f_tavg'].max()
# db.max()
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_new/GLDAS_NOAH025_3H.A20220710.1200.021.nc4'
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/input_files/GLDAS_NOAH025_3H.A20220710.0100.021.nc4'
ds = xr.open_dataset(flnm)
ds['PRCP']
# ds
# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/output_files/2022071001.PRECIP_FORCING.nc'
ds = xr.open_dataset(flnm)
ds['precip_rate'].max()
# ds
# %%
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/geo_em.d01.nc'
ds = xr.open_dataset(flnm)
ds['HGT_M'].shape