#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
绘制各产流过程(超渗产流， 壤中流, 蓄满产流)的产流分布
这里先把超渗产流和蓄满产流放在一起考虑
-----------------------------------------
Time             :2023/03/23 16:25:13
Author           :Forxd
Version          :1.0
'''


# %%
import xarray as xr
from draw_rain_distribution_24h import Draw
from draw_basin_terrain import draw_station
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cartopy.crs as ccrs
import netCDF4 as nc
from baobao.map import Map
import cartopy.feature as cfeature
import xesmf as xe
import scipy
from scipy.interpolate import RegularGridInterpolator
import os
from cartopy.io.shapereader import Reader, natural_earth
# plt.style.use('/home/fengx20/mypy/baobao/my.mplstyle')
%load_ext autoreload
%autoreload 2
# %%
def add_feature(ax):
    proj = ccrs.PlateCarree()
    river23 = cfeature.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国二、三级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='blue',
        # lw=1.,
        linewidth=1.5,
        facecolor='none',
        alpha=1.)

    river4 = cfeature.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国四级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='blue',
        lw=1.,
        linewidth=1,
        facecolor='none',
        alpha=1.)
    ax.add_feature(river23,  zorder=2, alpha=1)
    ax.add_feature(river4, zorder=2, alpha=1)


def regrid_coarse2fine2d(da, db):
    """
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


# %%
# %%
## LSM
class DrawStream():

    def __init__(self):
        pass
        self.colordict=['white','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表
        self.cmap = (mpl.colors.ListedColormap(self.colordict))
        self.bounds = [0, 0.01, 0.05, 0.1,0.5,  1, 2, 500]
        self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)

    def draw_runoff(self, da, lon, lat):
        cm = 1/2.54
        proj = ccrs.PlateCarree()  # 创建坐标系
        # fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
        fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
        # ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
        ax = fig.add_axes([0.10,0.20,0.85,0.75], projection=proj)
        dr = Draw(fig, ax)
        mp = Map()
        ax = mp.create_map(ax, dr.map_dic)

        dr.map_dic = {
            'proj':ccrs.PlateCarree(),
            # 'extent':[107, 108.5, 35.5, 36.5],
            'extent':[105, 110, 33.5, 37.5],
            'extent':[104, 108, 33.5, 36.5],
            'extent_interval_lat':1,
            'extent_interval_lon':2,
        }


        ax.set_extent(dr.map_dic['extent'])
        draw_station(ax)

        # colordict=['white','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表
        # cmap = (mpl.colors.ListedColormap(colordict))
        # bounds = [0, 0.01, 0.05, 0.1,0.5,  1, 2, 5]
        # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


        cs = ax.contourf(lon, lat, da.squeeze(), colors=self.colordict, levels=self.bounds)


        add_feature(ax)
        cb = dr.fig.colorbar(
            cs,
            # cax=ax6,
            orientation='horizontal',
            ticks=self.bounds[1:-1],
            fraction = 0.06,  # 色标大小,相对于原图的大小
            pad=0.11,  #  色标和子图间距离
            )

        # ticks=self.bounds[1:-1],
        tic = cb.get_ticks()
        labels = list(map(lambda x: str(x) if np.abs(x)<1 else str(int(x)), tic))  # 将colorbar的标签变为字符串
        cb.set_ticklabels(labels)  # 改变标签的格式

        return dr

# %%
flnm_latlon = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/wrf_hydro_gis_preprocessor/wrfhydro_gis/latlon.nc'
ds_latlon = xr.open_dataset(flnm_latlon)
ds_latlon

#%%
flnm_LSM = '/home/fengx20/project/hydro/test_ground/RUN/2002/200202030000.LSMOUT_DOMAIN1'
ds_LSM = xr.open_dataset(flnm_LSM)
ds_LSM
# %%
ds_LSM['sfcheadrt'].max()
# %%
def draw():
    # flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
    flnm_latlon = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/wrf_hydro_gis_preprocessor/wrfhydro_gis/latlon.nc'
    ds_latlon = xr.open_dataset(flnm_latlon)
    lat = ds_latlon['LATITUDE']
    lon = ds_latlon['LONGITUDE'][:,::-1]

    ### 绘制surface runoff
    flnm_LSM = '/home/fengx20/project/hydro/test_ground/RUN/2002/200201030000.LSMOUT_DOMAIN1'
    ds_LSM = xr.open_dataset(flnm_LSM)
    lon1 = lon[::4, ::4]
    lat1 = lat[::4, ::4]
    da = ds_LSM['sfcheadrt']
    drs = DrawStream()
    dr = drs.draw_runoff(da, lon1, lat1)

    path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
    dr.fig.savefig(path+'1412surface')

    drs = DrawStream()
    di = ds_LSM['infxsrt']
    dr = drs.draw_runoff(di, lon1, lat1)
    path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
    dr.fig.savefig(path+'1412_infil')

    ### 绘制subsurface runoff大小
    drs = DrawStream()
    # flnm_RT = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.RTOUT_DOMAIN1'
    flnm_RT = '/home/fengx20/project/hydro/test_ground/RUN/2002/200201030000.RTOUT_DOMAIN1'
    ds_RT= xr.open_dataset(flnm_RT)
    db = ds_RT['sfcheadsubrt'].squeeze()
    dc = regrid_coarse2fine2d(da.squeeze(), db.squeeze())
    # dr = drs.draw_runoff(db[::10, ::10].values-da.values, lon1, lat1)
    dr = drs.draw_runoff(dc-da, lon1, lat1)
    path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
    dr.fig.savefig(path+'1412_subsurface')


    ### 绘制壤中流比例
    drs = DrawStream()
    drs.bounds = [0, 0.1, 0.2, 0.4,0.7, 1,2,5]
    dr = drs.draw_runoff((dc-da)/da, lon1, lat1)  # 百分比
    path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
    dr.fig.savefig(path+'1412_subsurface_ratio')
draw()
# %%

# flnm = '/home/fengx20/project/hydro/data/output/runoff.nc'
# ds
flnm = '/home/fengx20/project/hydro/test_ground/RUN/2002/surface_runoff.nc'
ds = xr.open_dataset(flnm)
ds

# %%

#%%
# da = ds['surface_runoff'].sel(time='2022-07-15 00')
# db = ds['subsurface_runoff'].sel(time='2022-07-15 00')
da = ds['surface_runoff'].sum(dim='time')
# db = ds['subsurface_runoff'].sum(dim='time')
dc = ds['infiltration'].sum(dim='time')
#%%
# da.max()
# ds['surface_runoff'].max()
# ds
# dc.max()
ds['infiltration'].isel(time=3).max()
# (db-da).plot(levels=[-0.2, 0, 0.1])
# da.max()
# db.max()
# dc.max()
# (db-da).max()
#%%

lon = da.lon.values
lat = da.lat.values
## 地表径流(超渗产流+蓄满产流)
drs = DrawStream()
dr = drs.draw_runoff(dc, lon, lat)  # 百分比
pic_path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
dr.fig.savefig(pic_path+'surface_runoff_new')


# %%
## 地下径流(暴雨壤中流)
drs = DrawStream()
dr = drs.draw_runoff(da-db, lon, lat)  # 百分比
pic_path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
dr.fig.savefig(pic_path+'subsurface_runoff_new')
# %%
(db-da).min()
# %%
## 下渗
drs = DrawStream()
dr = drs.draw_runoff(dc, lon, lat)  # 百分比
pic_path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
dr.fig.savefig(pic_path+'infiltration')


# %%
## 地下径流占比
# drs = DrawStream()
# drs.colordict=['white','#A6F28F','#61BBFF','#0000FF']#颜色列表
# drs.colordict = ['white', '#58efcd','#1A51AD','#363472','#EF5350', '#f33030']
# drs.colordict = ['white', '#B2EBF2', '#4DD0E1', '#0097A7', '#006064']
# drs.colordict = ['white', 'white','#1A51AD','#EF5350']

# drs.bounds = [0, 0.1, 0.5, 0.7,1, 2]

# %%
# drs.bounds = [0, 0.1, 0.2, 0.3,0.5, 2]
drs.bounds = [0,  0.2, 0.3,0.5,1, 2]
dr = drs.draw_runoff((db-da)/dc, lon, lat)  # 百分比
# dr = drs.draw_runoff((da)/db, lon, lat)  # 百分比

# pic_path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
# strtime = str(da.time.dt.strftime('%m-%d_%H').values)
# title_time = str(da.time.dt.strftime('%m-%d %H:%M').values)
# dr.ax.set_title(title_time)
# dr.fig.savefig(pic_path+strtime+'_ratio')

# %%
# da.max()
# print(da)
# da
# db
# da[db>0]
## surface
flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/RESTART.2022071500_DOMAIN1'
ds = xr.open_dataset(flnm)
ds

# %%
# da = ds['runoff_surface']
da = ds['surface_runoff']
db = ds['subsurface_runoff']
db = da-db
dc = ds['infiltration']
da1 = xr.where(db>0, da, np.nan)
db1 = xr.where(db>0, db, np.nan)
dc1 = xr.where(db>0, dc, np.nan)
# dd
# %%
# db.min()
# ds['subsurface_runoff'].min()
# dc
# db1.min()
# da1.max()
# da1
# ds['infiltration'].max()
# %%
# %%
lon1 = ds.lon.values
lat1 = ds.lat.values


# %%
# %%
# %%
from baobao.caculate import caculate_average_wrf
area={'lat1':36, 'lat2':36.5, 'lon1':107.5, 'lon2':108.5}
# area={'lat1':35.0, 'lat2':36.5, 'lon1':107, 'lon2':108}
# area={'lat1':34, 'lat2':35, 'lon1':104, 'lon2':105}
# y1 = caculate_average_wrf(da1, area=area)
# y2 = caculate_average_wrf(db1, area=area)
# y3 = caculate_average_wrf(dc1, area=area)
y1 = caculate_average_wrf(da, area=area)
y2 = caculate_average_wrf(db, area=area)
y3 = caculate_average_wrf(dc, area=area)
# %%
# y1.sel(time=slice('2022-07-14', '2022-07-16')).plot(label='surface')
# y2.sel(time=slice('2022-07-14', '2022-07-16')).plot(label='subsurface')
# y3.sel(time=slice('2022-07-14', '2022-07-16')).plot(label='infiltration')
# plt.legend()
# plt.xlim(0, 20)
y1.plot()
y2.plot()
y3.plot()
# %%
x = y1.time.dt.strftime('%d/%H')
cm = 1/2.54
fig = plt.figure(figsize=(8*cm,6*cm))
ax = fig.add_axes([0.21, 0.2, 0.7, 0.7])
ax.plot(x,y1, label='surface', c='black')
ax.plot(x,y2, label='sub-surface',)
ax.plot(x,y3, label='infiltration',)
ax.set_xticks(x[::12])
ax.legend(edgecolor='white', loc='upper right', fontsize=8)
ax.set_xlim(0, 52)
ax.set_ylim(0, 0.5)
ax.set_ylabel('runoff (mm)')
ax.set_xlabel('Time (Day/Hour)')
fig_path = '/home/fengx20/project/hydro/Draw/figure/chanliu/'
fig.savefig(fig_path+'area_mean.png')

# %%
# db.sum(dim='time').plot(levels=[-1,  1])
# db.min()
# (da.sum(dim='time')-da.sum(dim='time')).min()
# da
# db.sum(dim='time').plot(levels=[-1, 1])
import xarray as xr
# flnm_RT = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.RTOUT_DOMAIN1'
flnm_RT = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140400.CHRTOUT_DOMAIN1'
ds= xr.open_dataset(flnm_RT)
# %%
ds['q_lateral'].min()
# %%
flnm_LSM = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.LSMOUT_DOMAIN1'
ds_LSM = xr.open_dataset(flnm_LSM)
# lon1 = lon[::10, ::10]
# lat1 = lat[::10, ::10]
da = ds_LSM['sfcheadrt']
da
# %%
# da.min()
flnm = '/home/fengx20/project/hydro/test3/RUN/test/route11/HYDRO_RST.2022-07-15_00:00_DOMAIN1'
ds = xr.open_dataset(flnm)
ds
# %%
flnm = '/home/fengx20/project/hydro/data/output/runoff.nc'
ds = xr.open_dataset(flnm)
ds
# %%
# ds['surface_runoff'].max()
a = ds['subsurface_runoff'].sum(dim='time').mean(dim=['y', 'x'])
# %%
b = ds['surface_runoff'].sum(dim='time').mean(dim=['y', 'x'])
# %%
# a
c = ds['infiltration'].sum(dim='time').mean(dim=['y', 'x'])
c
# %%
flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140100.LDASOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
ds
# %%
# (ds['QRAIN']*3600).max()
# ds['ACCEDIR'].max()
# ds['ACCETRAN'].max()
# ds['ACCET'].max()
# ds['CANWAT'].max()
# ds['UGDRNOFF'].max()
ds['ACCET']
# %%

flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141600.LSMOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
# %%
# ds['infxsrt'].max()   # 超渗产流
# ds['sfcheadrt'].max()   # 地表径流
flnm = '/home/fengx20/project/hydro/test_ground/RUN/2002/200207010000.CHRTOUT_GRID1'
ds = xr.open_dataset(flnm)
ds
# %%
ds['streamflow'].plot()