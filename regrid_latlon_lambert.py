import xesmf as xe
import xarray as xr
import numpy as np
import os
# %%
def create_ds_latlon(ds):
    """
    将一维的lat,lon格式的数组，变为二维的lat, lon
    这里的ds不包含时间维度，是二维数组
    创建regrider 的输入ds_in
    单个变量var
    """
    ds = ds.squeeze()
    lon = ds.lon.values
    lat = ds.lat.values
    ## 将标准网格变为meshgrid网格
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    ## 输入的不规则曲线数组


    # ds_in = xr.Dataset(
    #     coords={
    #         'lon':(['south_north','west_east'], lon_grid),
    #         'lat':(['south_north','west_east'], lat_grid),
    #     },
    # )
    var = list(ds.data_vars)[0]
    ds_in = xr.Dataset(
        {
            var:(['south_north', 'west_east'], ds[var].values)
        },
        coords={
            'lon':(['south_north','west_east'], lon_grid),
            'lat':(['south_north','west_east'], lat_grid),
        },
    )
    return ds_in

def create_ds_lambert(ds_geo):
    """
    ds_geo可以是任意wrfout数据读出Dataset文件 
    只要包含XLAT_M和XLONG_M两个变量即可
    要求没有时间维度
    """
    ds_geo = ds_geo.squeeze()
    ### 准备输出的 curvilinear 网格
    xlat = ds_geo.squeeze()['XLAT_M'].values
    xlon = ds_geo.squeeze()['XLONG_M'].values
    ## 改变meshgrid网格的名称,且只要coords
    # ds_out = xr.Dataset(
    #     coords={
    #         'lon':(['y','x'], xlon),
    #         'lat':(['y','x'], xlat),
    #     }
    # )
    ds_out = xr.Dataset(
        coords={
            'lon':(['south_north','west_east'], xlon),
            'lat':(['south_north','west_east'], xlat),
        },
    )
    return ds_out

# %% 
def create_regrider(flnm_regrider, ds_in, ds_out):
    # flnm_regrider = '/home/fengx20/project/hydro/Draw/regrider.nc'
    ## 构建插值器
    if not os.path.exists(flnm_regrider):
        # 创建插值器
        regrider = xe.Regridder(ds_in, ds_out, 'bilinear')
        # 保存插值器
        regrider.to_netcdf(flnm_regrider)
    else:
        ## 重用插值器
        regrider = xe.Regridder(ds_in, ds_out, 'bilinear', weights=flnm_regrider)
    return regrider
# %%

if __name__ == "__main__":
    ### 准备input curvilinear 网格
    flnm_obs = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
    ds_obs = xr.open_dataset(flnm_obs)
    ds_obs = ds_obs.rename({'PRCP':'precip'})
    ds = ds_obs.sel(time='2022-07-15 00')
    ds_in = create_ds_latlon(ds)

    flnm_geo = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/geo_em.d01.nc'
    ds_geo = xr.open_dataset(flnm_geo)
    ds_out = create_ds_lambert(ds_geo)

    flnm_regrider = '/home/fengx20/project/hydro/Draw/regrider.nc'
    regrider = create_regrider(flnm_regrider, ds_in, ds_out)

    # dss = regrider(ds_obs)  # 含有时间维度，直接插值会快一些
    # for t in ds_obs.time:
    #     ds = ds_obs.sel(time=t)
    #     ds_in = create_ds_latlon(ds)  
    #     dss = regrider(ds_in)
    #     dss = dss.expand_dims(dim='Time')
    #     str_time = str(ds.time.dt.strftime('%Y%m%d%H%M').values)
    #     print(str_time)
    #     str_name = str_time+'.PRECIP_FORCING.nc'

    #     path_save = '/home/fengx20/project/hydro/test3/DATA/forcingdata/RAIN/'
    #     dss.to_netcdf(path_save+str_name)

    ## 插值
    dss = regrider(ds_obs)  # 含有时间维度，直接插值会快一些
    
    ## 分开保存
    for t in dss.time:
        ds1 = dss.sel(time=t)  # 单个时次的
        ds2 = ds1.expand_dims(dim='Time')  # 

        str_time = str(ds1.time.dt.strftime('%Y%m%d%H%M').values)
        print(str_time)
        str_name = str_time+'.PRECIP_FORCING.nc'
        path_save = '/home/fengx20/project/hydro/test3/DATA/forcingdata/RAIN/'
        ds2.to_netcdf(path_save+str_name)
# %%
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/RAIN/202207150000.PRECIP_FORCING.nc'
# ds = xr.open_dataset(flnm)
# %%
# ds['precip'].plot()