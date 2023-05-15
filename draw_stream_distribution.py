#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
画径流的空间分布, 逐小时的径流分布

-----------------------------------------
Time             :2023/02/03 16:52:49
Author           :Forxd
Version          :1.0
'''

# %%
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import netCDF4 as nc
import wrf
import cmaps
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from draw_basin_terrain import draw_station, draw_river_basin
import pandas as pd
from baobao.map import Map, get_rgb

from draw_rain_distribution_24h import Draw

# import maskout
from wrf import get_cartopy

# %%
def save_data():
    flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHRTOUT_GRID*'
    ds = xr.open_mfdataset(flnm)
    # da = ds['streamflow']
    ds.load()
    ds.to_netcdf('/home/fengx20/project/hydro/data/output/CHRTOUT_GRID.nc')
    # flnm = '/home/fengx20/project/hydro/data/output/CHRTOUT_GRID.nc'
    # ds = xr.open_dataset(flnm)

# %%
# %%
# da.min()
def draw_stream(da, lon, lat):
    def normalization(data):
        _range = np.max(data) - np.min(data)
        return (data - np.min(data)) / _range
    def standardization(data):
        mu = np.mean(data, axis=0)
        sigma = np.std(data, axis=0)
        return (data - mu) / sigma
    # db = normalization(da)
    db = standardization(da)
    lon1 = lon.values.flatten()
    lat1 = lat.values.flatten()
    daa = da.values.flatten()

    index_nonan = ~np.isnan(daa)
    a = daa[index_nonan]
    b = lon1[index_nonan]
    c = lat1[index_nonan]

    index_small_big = np.argsort(a)
    index_small_big

    a1 = a[index_small_big]
    b1 = b[index_small_big]
    c1 = c[index_small_big]

    index_positive = a1>0
    a2 = a1[index_positive]
    b2 = b1[index_positive]
    c2 = c1[index_positive]

    d2 = normalization(a2)


    # fig = plt.figure(figsize=(4,3), dpi=300)
    # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])


    cm = 1/2.54
    proj = ccrs.PlateCarree()  # 创建坐标系
    # fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
    fig = plt.figure(figsize=(8*cm, 6*cm), dpi=300)
    # ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
    ax = fig.add_axes([0.10,0.10,0.75,0.8], projection=proj)
    dr = Draw(fig, ax)

    mp = Map()
    ax = mp.create_map(ax, dr.map_dic)
    ax.set_extent(dr.map_dic['extent'])
    from draw_basin_terrain import draw_station
    draw_station(ax)







    colordict=['white','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表
    cmap = (mpl.colors.ListedColormap(colordict))
    bounds=[0, 10, 25, 50, 100, 250, 500,  1000, 3000]#雨量等级
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cf = ax.scatter(b2, c2, s=d2, c=a2, cmap=cmap, norm=norm, alpha=1,marker='.', zorder=1)


    shp_path = '/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp'
    flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    ncfile = nc.Dataset(flnm_90m_met)
    hgt = wrf.getvar(ncfile, "HGT_M")
    # proj_lambert = get_cartopy(hgt)
    # clip = maskout.shp2clip(cf, ax, shp_path)




    fig.colorbar(cf, extend='max', 
                    fraction = 0.025,  # 色标大小,相对于原图的大小
                    # pad=0.02,  #  色标和子图间距离
                )

    str_time = str(da.time.dt.strftime('%m-%d %H:%M').values)
    ax.set_title(str_time, loc='left')
    fig_name = str(da.time.dt.strftime('stream_%m%d_%H%M').values)
    fig.savefig('/home/fengx20/project/hydro/Draw/figure/stream_distribution/'+fig_name)


# %%


# flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
# ncfile = nc.Dataset(flnm_90m_met)
# hgt = wrf.getvar(ncfile, "HGT_M")
# proj_lambert = wrf.get_cartopy(hgt)
# proj = ccrs.PlateCarree()  # 创建坐标系
# ## 创建坐标系
# cm = 1/2.54
# fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)  # 创建页面
# ax = fig.add_axes([0.1, 0.1, 0.85, 0.8], projection=proj_lambert)
# ## --设置网格属性, 不画默认的标签
# gl = ax.gridlines(draw_labels=True,
#                     dms=True,
#                     linestyle=":",
#                     linewidth=0.2,
#                     x_inline=False,
#                     y_inline=False,
#                     color='k',)
# # # gl=ax.gridlines(draw_labels=True,linestyle=":",linewidth=0.3 , auto_inline=True,x_inline=False, y_inline=False,color='k')

# ## 关闭上面和右边的经纬度显示
# gl.top_labels = False  #关闭上部经纬标签
# gl.right_labels = False
# ## 这个东西还挺重要的，对齐坐标用的
# gl.rotate_labels = None
# ## 坐标的范围
# # gl.xlocator = mticker.FixedLocator(np.arange(90, 140, 5))
# gl.xlocator = mticker.FixedLocator(np.arange(70, 150, 1))

# gl.ylocator = mticker.FixedLocator(np.arange(10, 50, 1))
# ## 坐标标签的大小
# gl.xlabel_style = {'size': 10}  #修改经纬度字体大小
# gl.ylabel_style = {'size': 10}
# ## 坐标标签样式
# gl.xformatter = LongitudeFormatter(degree_symbol="${^\circ}$")
# gl.yformatter = LatitudeFormatter(degree_symbol="${^\circ}$")

# ax.spines['geo'].set_linewidth(1.0)  #调节图片边框粗细



# ax.set_extent([103.85, 110.15, 33.55, 37.37],
#                 crs=ccrs.PlateCarree())

# da = ds['streamflow'].sel(time='2022-07-16 11')
# # crs = ax.contourf(lon, lat, da.values, levels=[0, 200,500, 1000, 2000, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
# # crs = ax.contourf(lon, lat, da.values, levels=[0, 1000, 1500, 2000,2500, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
# # crs = ax.pcolormesh(lon, lat, da.values, levels=[0, 1000, 1500, 2000,2500, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
# crs = ax.contourf(lon, lat, da.values, levels=[0, 1000, 1500, 2000,2500, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
# crs = ax.contour(lon, lat, da.values, levels=[0, 1000, 1500, 2000,2500, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
# ax.set_title('2022-07-15 00', loc='left')
# # crs = ax.scatter(lon, lat, da.values/100,  color='blue', transform=ccrs.PlateCarree())
# draw_station(ax)
# draw_river_basin(fig, ax)
# fig.colorbar(crs, orientation='horizontal', fraction=0.05, pad=0.11)
# # fig.savefig('./figure/1600.png')
save_data()

flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
ds_latlon = xr.open_dataset(flnm_latlon)
ds_latlon
lat = ds_latlon['LATITUDE']
lon = ds_latlon['LONGITUDE'][:, ::-1]

flnm = '/home/fengx20/project/hydro/data/output/CHRTOUT_GRID.nc'
ds = xr.open_dataset(flnm)

tt = pd.date_range('2022-07-14 12', '2022-07-16 12', freq='12H')
for t in tt:
    da = ds['streamflow'].sel(time=t)
    str_time = str(da.time.dt.strftime('%m-%d %H:%M').values)
    print(str_time)
    draw_stream(da, lon, lat)