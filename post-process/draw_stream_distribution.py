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
from cartopy.io.shapereader import Reader, natural_earth
# from draw_basin_terrain import draw_station, draw_river_basin
import cartopy.feature as cfeature
import pandas as pd
from baobao.map import Map, get_rgb

from draw_rain_distribution_24h import Draw
from matplotlib import rcParams
config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}
rcParams.update(config)

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


def draw_station(ax,):

    flnm_csv = '/home/fengx20/project/hydro/src/data/station_latlon.csv'
    df = pd.read_csv(flnm_csv)
    col = ['code', 'lat', 'lon', 'name']
    df1 = df[col]
    df2 = df1.rename(index=str, columns={'code':'id'})
    df2
    for i in df2['name']:
        print('叠加%s站点'%i.strip())
        df3 = df2[df2.name.str.contains(i)]
        lon = df3['lon'].values[0]
        lat = df3['lat'].values[0]
        sta_name = df3['name'].values[0].strip()
        sta_list = [
            '秦安',
            '林家村',
            '魏家堡',
            '武山',
        ]
        if sta_name in sta_list:
            ax.scatter(lon,
                    lat,
                    color='red',
                    transform=ccrs.PlateCarree(),
                    linewidth=1,
                    s=0.1, 
                    zorder=5,
                    )
            ## 给站点加注释
            ax.text(lon-0.2 ,
                    lat + 0.06,
                    sta_name,
                    transform=ccrs.PlateCarree(),
                    fontsize=9,
            )


def create_map(fig, ax, proj_lambert):
    """创建一个包含青藏高原区域的Lambert投影的底图

    Returns:
        ax: 坐标图对象
    """
    # ## --创建画图空间
    # # flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    # flnm_90m_met = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/geo_em.d01.nc'
    # ncfile = nc.Dataset(flnm_90m_met)

    # hgt = wrf.getvar(ncfile, "HGT_M")
    # # Get the cartopy mapping object
    # proj_lambert = get_cartopy(hgt)
    # # proj = ccrs.PlateCarree()  # 创建坐标系
    # ## 创建坐标系
    # cm = 1/2.54
    # fig = plt.figure(figsize=(8*cm, 7*cm), dpi=300)  # 创建页面
    # ax = fig.add_axes([0.1, 0.11, 0.85, 0.8], projection=proj_lambert)
    

    river = cfeature.ShapelyFeature(
        Reader('/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/river.shp').geometries(),  # 快速画图的地图文件
        # Reader('/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/border/3333.shp').geometries(),  # 快速画图的地图文件
        proj_lambert,
        edgecolor='blue',
        linewidth=1.,
        facecolor='none',
        alpha=1.)

    # cfeature
    basin = cfeature.ShapelyFeature(
        Reader('/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/border/all_border.shp').geometries(),  # 快速画图的地图文件
        proj_lambert,
        edgecolor='black',
        # edgecolor=np.array([208,208,208])/255,
        lw=1.5,
        linewidth=1,
        facecolor='none',
        alpha=1.)

    basin0 = cfeature.ShapelyFeature(
        Reader('/home/fengx20/project/hydro/test_ground/Hydro_Routing/shp/0.shp').geometries(),  # 快速画图的地图文件
        proj_lambert,
        edgecolor='red',
        lw=1.5,
        linewidth=1,
        facecolor='none',
        alpha=1.)
        


    # ax.add_feature(river,  zorder=2, alpha=1)
    ax.add_feature(basin, zorder=2, alpha=1)
    # ax.add_feature(basin0, zorder=3, alpha=1)
    

    ## --设置网格属性, 不画默认的标签
    gl = ax.gridlines(draw_labels=True,
                      dms=True,
                      linestyle=":",
                      linewidth=0.2,
                      x_inline=False,
                      y_inline=False,
                      color='k',)

    ## 关闭上面和右边的经纬度显示
    gl.top_labels = False  #关闭上部经纬标签
    gl.right_labels = False
    ## 这个东西还挺重要的，对齐坐标用的
    gl.rotate_labels = None
    ## 坐标的范围
    # gl.xlocator = mticker.FixedLocator(np.arange(90, 140, 5))
    gl.xlocator = mticker.FixedLocator(np.arange(70, 150, 1))
    
    gl.ylocator = mticker.FixedLocator(np.arange(10, 50, 1))
    ## 坐标标签的大小
    gl.xlabel_style = {'size': 10}  #修改经纬度字体大小
    gl.ylabel_style = {'size': 10}
    ## 坐标标签样式
    gl.xformatter = LongitudeFormatter(degree_symbol="${^\circ}$")
    gl.yformatter = LatitudeFormatter(degree_symbol="${^\circ}$")

    ax.spines['geo'].set_linewidth(1.0)  #调节图片边框粗细

    ax.set_extent([103.8, 108, 33.5, 36.5],
                  crs=ccrs.PlateCarree())

    return fig, ax
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
    # shp_path = '/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp'
    flnm_90m_met = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
    ncfile = nc.Dataset(flnm_90m_met)
    hgt = wrf.getvar(ncfile, "T2")
    # flnm_wrf = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/wrfinput_d01.nc'
    proj_lambert = wrf.get_cartopy(var=hgt)
    # clip = maskout.shp2clip(cf, ax, shp_path)

    # proj = wrf.getvar()
    cm = 1/2.54

    proj = ccrs.PlateCarree()  # 创建坐标系
    # fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
    fig = plt.figure(figsize=(8.5*cm, 6*cm), dpi=300)
    # ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
    ax = fig.add_axes([0.13,0.10,0.7,0.8], projection=proj_lambert)
    fig, ax = create_map(fig, ax, proj_lambert)

    dr = Draw(fig, ax)

    mp = Map()
    # ax = mp.create_map(ax, dr.map_dic)
    ax.set_extent(dr.map_dic['extent'])
    # from draw_basin_terrain import draw_station
    draw_station(ax)







    colordict=['white','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表
    cmap = (mpl.colors.ListedColormap(colordict))
    # bounds=[0, 10, 25, 50, 100, 250, 500,  1000, 3000]#雨量等级
    bounds=[0, 1, 2.5, 5.0, 10.0, 25.0, 50.0,  300.0, 500.0]#雨量等级
    # bounds=np.linspace(0, 0.5, 9)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cf = ax.scatter(b2, c2, s=d2, c=a2, cmap=cmap, norm=norm, alpha=1,marker='.', zorder=1, transform=ccrs.PlateCarree())






    fig.colorbar(cf, extend='max', 
                    fraction = 0.035,  # 色标大小,相对于原图的大小
                    pad=0.07,  #  色标和子图间距离
                )
    label='($m^3\,s^{-1}$)'
    fig.text(0.79, 0.88, label)            

    # str_time = str(da.time.dt.strftime('%m-%d %H:%M').values)
    # ax.set_title(str_time, loc='left')
    # fig_name = str(da.time.dt.strftime('stream_%m%d_%H%M').values)
    fig_name = 'stream_distribution_2003_09_0100.png'
    fig.savefig('/home/fengx20/project/hydro/figure/'+fig_name)


# %%

# %%

if __name__ == "__main__":

    ### CHRTOUT_DOMAIN
    flnm_CH = '/home/fengx20/project/hydro/test_ground/RUN/200308050000.CHRTOUT_DOMAIN1'
    ds_CH = xr.open_dataset(flnm_CH)
    da = ds_CH['streamflow']
    lon = da.longitude
    lat = da.latitude
    draw_stream(da, lon, lat)
    

    # flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
    # ds_latlon = xr.open_dataset(flnm_latlon)
    # ds_latlon
    # lat = ds_latlon['LATITUDE']
    # lon = ds_latlon['LONGITUDE'][:, ::-1]

    # flnm = '/home/fengx20/project/hydro/data/output/CHRTOUT_GRID.nc'
    # ds = xr.open_dataset(flnm)

    # tt = pd.date_range('2022-07-14 12', '2022-07-16 12', freq='12H')
    # for t in tt:
    #     da = ds['streamflow'].sel(time=t)
    #     str_time = str(da.time.dt.strftime('%m-%d %H:%M').values)
    #     print(str_time)
    #     draw_stream(da, lon, lat)
# %%
