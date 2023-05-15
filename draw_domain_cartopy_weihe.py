#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
read in namelist.wps , draw wrf domain and plot some station
add draw circle
-----------------------------------------
Time             :2021/03/28 17:28:59
Author           :Forxd
Version          :1.0
'''
# %%
%load_ext autoreload
%autoreload 2

import xarray as xr
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
# import geopandas
# import cmaps
import re
import pandas as pd

from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import Circle
import wrf
import netCDF4 as nc
import cmaps

from matplotlib import rcParams
config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}
rcParams.update(config)
# plt.style.use('/home/fengx20/mypy/baobao/my.mplstyle')

# %%



# %%

def ll2xy(lat, lon, info):
    # lat = 32
    # lon = 112
    x,y = wrf.ll_to_xy_proj(lat, lon, map_proj=1, 
                            truelat1=info['true_lat1'], 
                            truelat2=info['true_lat2'], 
                            stand_lon=info['stand_lon'], 
                            ref_lat=info['ref_lat'], 
                            ref_lon=info['ref_lon'], 
                            known_x=(int(info['e_we'][0])-1)/2-1,
                            known_y=(int(info['e_sn'][0])-1)/2-1,
                            dx = info['dx'],
                            dy = info['dy'],
                            )
    # info
    return x.values, y.values

def draw_screen_poly(lats, lons):
    '''
    lats: 纬度列表
    lons: 经度列表
    purpose:  画区域直线
    '''
    x, y = lons, lats
    xy = list(zip(x, y))
    print(xy)
    poly = plt.Polygon(xy, edgecolor="black", fc="none", lw=1, alpha=1)
    plt.gca().add_patch(poly)


def create_map(info):
    """创建一个包含青藏高原区域的Lambert投影的底图

    Returns:
        ax: 坐标图对象
    """
    ## --创建画图空间

    ref_lat = info['ref_lat']
    ref_lon = info['ref_lon']
    true_lat1 = info['true_lat1']
    true_lat2 = info['true_lat2']
    false_easting = (info['e_we'][0] - 1) / 2 * info['dx']
    false_northing = (info['e_sn'][0] - 1) / 2 * info['dy']

    proj_lambert = ccrs.LambertConformal(
        central_longitude=ref_lon,
        central_latitude=ref_lat,
        standard_parallels=(true_lat1, true_lat2),
        cutoff=-30,
        false_easting=false_easting,
        false_northing=false_northing,
    )

    
    # wrf.ll_to_xy_proj(32, 112, map_proj=proj_lambert)    
    
    

    # proj = ccrs.PlateCarree(central_longitude=ref_lon)  # 创建坐标系
    proj = ccrs.PlateCarree()  # 创建坐标系
    ## 创建坐标系
    cm = 1/2.54
    fig = plt.figure(figsize=(8*cm, 6*cm), dpi=300)  # 创建页面
    # ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=proj)
    ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=proj_lambert)
    # ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], projection=proj_lambert)

    ## 读取青藏高原地形文件

    Province = cfeat.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/china2000/china2000.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='black',
        lw=1.,
        linewidth=1.,
        facecolor='none',
        alpha=1.)
        
    river23 = cfeat.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国二、三级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='blue',
        lw=1.,
        linewidth=1.,
        facecolor='none',
        alpha=1.)

    river4 = cfeat.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国四级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='red',
        lw=1.,
        linewidth=1.,
        facecolor='none',
        alpha=1.)
    river5 = cfeat.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国五级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='orange',
        lw=1.,
        linewidth=1.,
        facecolor='none',
        alpha=1.)
    weihe = cfeat.ShapelyFeature(
        Reader('/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='black',
        lw=1.,
        linewidth=1.,
        facecolor='none',
        alpha=1.)
    ## 将青藏高原地形文件加到地图中区

    # ax.add_feature(Province, linewidth=0.5, zorder=2, alpha=0.3)
    ax.add_feature(river23, linewidth=0.5, zorder=2, alpha=1)
    # ax.add_feature(river4, linewidth=0.5, zorder=2, alpha=1)
    ax.add_feature(river5, linewidth=0.5, zorder=2, alpha=1)
    ax.add_feature(weihe, linewidth=0.5, zorder=2, alpha=1)




    # ax.add_feature(shanxi, linewidth=0.5, zorder=2, alpha=0.3)

    # ax.add_feature(Henan, linewidth=0.6, zorder=2)
    # ax.add_feature(city, linewidth=0.5, zorder=2)
    # ax.coastlines(linestyle=':', linewidth=1, alpha=0.7)
    # ax.coastlines()
    # import cartopy.feature as cfeature
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.river, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black')
    # ax.add_feature(cfeature.LAKES.with_scale('10m'), edgecolor='blue')
    # ax.add_feature(cfeature.RIVERS.with_scale('10m'), facecolor='None', edgecolor='b')
    # with_scale('10m')

    ## --设置网格属性, 不画默认的标签
    gl = ax.gridlines(draw_labels=True,
                      dms=True,
                      linestyle=":",
                      linewidth=0.2,
                      x_inline=False,
                      y_inline=False,
                      color='k',)
    # # gl=ax.gridlines(draw_labels=True,linestyle=":",linewidth=0.3 , auto_inline=True,x_inline=False, y_inline=False,color='k')

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

    ## 画d02
    ax.set_extent([0, false_easting * 2, 0, false_northing * 2],
                  crs=proj_lambert)

    # # 标注d01, 这个位置需要根据经纬度手动调整
    # ax.text(78, # 经度
    #         45,  # 纬度
    #         'd01',
    #         transform=ccrs.PlateCarree(),
    #         fontdict={
    #             'size': 12,
    #         })
    return ax, fig


def get_information(flnm):
    """根据namelist.wps文件，获取地图的基本信息

    Args:
        flnm ([type]): [description]

    Returns:
        [type]: [description]
    """

    ## 设置正则表达式信息
    pattern = {}
    pattern['dx'] = 'dx\s*=\s*\d*,'
    pattern['dy'] = 'dy\s*=\s*\d*,'
    pattern['max_dom'] = 'max_dom\s*=\s*\d\s*,'
    pattern[
        'parent_grid_ratio'] = 'parent_grid_ratio\s*=\s*\d,\s*\d,\s*\d,\s*\d,'
    pattern['j_parent_start'] = 'j_parent_start\s*=\s*\d,\s*\d*,\s*\d*,\s*\d*,'
    pattern['i_parent_start'] = 'i_parent_start\s*=\s*\d,\s*\d*,\s*\d*,\s*\d*,'
    pattern['e_sn'] = 'e_sn\s*=\s*\d*,\s*\d*,\s*\d*,\s*\d*'
    pattern['e_we'] = 'e_we\s*=\s*\d*,\s*\d*,\s*\d*,\s*\d*'
    pattern['ref_lat'] = 'ref_lat\s*=\s*\d*.?\d*,'
    pattern['ref_lon'] = 'ref_lon\s*=\s*\d*.?\d*,'
    pattern['true_lat1'] = 'truelat1\s*=\s*\d*.?\d*,'
    pattern['true_lat2'] = 'truelat2\s*=\s*\d*.?\d*,'
    pattern['stand_lon'] = 'stand_lon\s*=\s*\d*.?\d*,'

    f = open(flnm)
    fr = f.read()

    def get_var(var, pattern=pattern, fr=fr):
        """处理正则表达式得到的数据"""
        ff1 = re.search(pattern[var], fr, flags=0)
        # print(ff1)
        str_f1 = ff1.group(0)

        str1 = str_f1.replace('=', ',')
        aa = str1.split(',')
        bb = []
        for i in aa[1:]:
            if i != '':
                bb.append(i.strip())
        return bb

    dic_return = {}
    aa = get_var('parent_grid_ratio')

    var_list = [
        'dx',
        'dy',
        'max_dom',
        'parent_grid_ratio',
        'j_parent_start',
        'i_parent_start',
        'e_sn',
        'e_we',
        'ref_lat',
        'ref_lon',
        'true_lat1',
        'true_lat2',
        'stand_lon',
    ]

    for i in var_list:
        aa = get_var(i)
        if i in [
                'parent_grid_ratio',
                'j_parent_start',
                'i_parent_start',
                'e_we',
                'e_sn',
        ]:
            bb = aa
            bb = [float(i) for i in bb]
        else:
            bb = float(aa[0])
        dic_return[i] = bb

    return dic_return



def draw_d02(info):
    """绘制domain2

    Args:
        info ([type]): [description]
    """
    max_dom = info['max_dom']
    dx = info['dx']
    dy = info['dy']
    i_parent_start = info['i_parent_start']
    j_parent_start = info['j_parent_start']
    parent_grid_ratio = info['parent_grid_ratio']
    e_we = info['e_we']
    e_sn = info['e_sn']

    if max_dom == 1:
        ### domain 2
        # 4 corners 找到四个顶点和距离相关的坐标
        ll_lon = dx * (i_parent_start[0] - 1)
        ll_lat = dy * (j_parent_start[0] - 1)
        ur_lon = ll_lon + dx / parent_grid_ratio[0] * (e_we[0] - 1)
        ur_lat = ll_lat + dy / parent_grid_ratio[0] * (e_sn[0] - 1)

        lon = np.empty(4)
        lat = np.empty(4)

        lon[0], lat[0] = ll_lon, ll_lat  # lower left (ll)
        lon[1], lat[1] = ur_lon, ll_lat  # lower right (lr)
        lon[2], lat[2] = ur_lon, ur_lat  # upper right (ur)
        lon[3], lat[3] = ll_lon, ur_lat  # upper left (ul)

        draw_screen_poly(lat, lon)  # 画多边型

    elif max_dom >= 2:
        ### domain 2
        # 4 corners 找到四个顶点和距离相关的坐标
        ll_lon = dx * (i_parent_start[1] - 1)
        ll_lat = dy * (j_parent_start[1] - 1)
        ur_lon = ll_lon + dx / parent_grid_ratio[1] * (e_we[1] - 1)
        ur_lat = ll_lat + dy / parent_grid_ratio[1] * (e_sn[1] - 1)

        lon = np.empty(4)
        lat = np.empty(4)

        lon[0], lat[0] = ll_lon, ll_lat  # lower left (ll)
        lon[1], lat[1] = ur_lon, ll_lat  # lower right (lr)
        lon[2], lat[2] = ur_lon, ur_lat  # upper right (ur)
        lon[3], lat[3] = ll_lon, ur_lat  # upper left (ul)

        draw_screen_poly(lat, lon)  # 画多边型

        ## 标注d02
        # plt.text(lon[0] * 1+100000, lat[0] * 1. - 225000, "d02", fontdict={'size':14})
        # plt.text(lon[2] * 1 - 440000,
        # plt.text(lon[2] * 1 - 540000,
        #         #  lat[2] * 1. - 200000,
        #          lat[2] * 1. - 300000,
        #          "d02",
        #          fontdict={'size': 12})

    elif max_dom >= 3:
        ### domain 3
        ## 4 corners
        ll_lon += dx / parent_grid_ratio[1] * (i_parent_start[2] - 1)
        ll_lat += dy / parent_grid_ratio[1] * (j_parent_start[2] - 1)
        ur_lon = ll_lon + dx / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            e_we[2] - 1)
        ur_lat = ll_lat + dy / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            e_sn[2] - 1)

        ## ll
        lon[0], lat[0] = ll_lon, ll_lat
        ## lr
        lon[1], lat[1] = ur_lon, ll_lat
        ## ur
        lon[2], lat[2] = ur_lon, ur_lat
        ## ul
        lon[3], lat[3] = ll_lon, ur_lat

        draw_screen_poly(lat, lon)

        ## 标注d03
        # plt.text(lon[0] * 1+100000, lat[0] * 1. - 225000, "d02", fontdict={'size':14})
        plt.text(lon[3] * 1+50000 ,
                #  lat[3] * 1. - 200000,
                 lat[3] * 1. - 300000,
                 "d03",
                 fontdict={'size': 12})
        
    elif max_dom >= 4:

        ### domain 4
        ## 4 corners
        ll_lon += dx / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            i_parent_start[3] - 1)
        ll_lat += dy / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            j_parent_start[3] - 1)
        ur_lon = ll_lon + dx / parent_grid_ratio[1] / parent_grid_ratio[
            2] / parent_grid_ratio[3] * (e_we[3] - 1)
        ur_lat = ll_lat + dy / parent_grid_ratio[1] / parent_grid_ratio[
            2] / parent_grid_ratio[3] * (e_sn[3] - 1)

        ## ll
        lon[0], lat[0] = ll_lon, ll_lat
        ## lr
        lon[1], lat[1] = ur_lon, ll_lat
        ## ur
        lon[2], lat[2] = ur_lon, ur_lat
        ## ul
        lon[3], lat[3] = ll_lon, ur_lat
        draw_screen_poly(lat, lon)

    if max_dom >= 4:

        ### domain 5
        ## 4 corners
        ll_lon += dx / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            i_parent_start[4] - 1)
        ll_lat += dy / parent_grid_ratio[1] / parent_grid_ratio[2] * (
            j_parent_start[4] - 1)
        ur_lon = ll_lon + dx / parent_grid_ratio[1] / parent_grid_ratio[
            2] / parent_grid_ratio[3] * (e_we[4] - 1)
        ur_lat = ll_lat + dy / parent_grid_ratio[1] / parent_grid_ratio[
            2] / parent_grid_ratio[3] * (e_sn[4] - 1)

        ## ll
        lon[0], lat[0] = ll_lon, ll_lat
        ## lr
        lon[1], lat[1] = ur_lon, ll_lat
        ## ur
        lon[2], lat[2] = ur_lon, ur_lat
        ## ul
        lon[3], lat[3] = ll_lon, ur_lat
        draw_screen_poly(lat, lon)


def draw_station(ax,):

    flnm_csv = '/home/fengx20/project/hydro/Draw/station_latlon.csv'
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
        # print(lon, lat, sta_name)
        ## 标记站点
        # if sta_name in ['黑峪口', '武山']:
        # if sta_name in ['黑峪口', '武山']:
        sta_list = [
            # '罗李村',
            # '马渡王',
            # '秦渡',
            # '黑峪口',
            '秦安',
            '天水',
            # '柳林',
            # '涝峪口',
            # '耀县',
            '隆德',
            # '北道',
            # '华县',
            '林家村',
            '魏家堡',
            '武山',
            # '咸阳',
            # '淳化',
        ]
        if sta_name in sta_list:
            ax.scatter(lon,
                    lat,
                    color='black',
                    transform=ccrs.PlateCarree(),
                    linewidth=1,
                    s=12, 
                    zorder =5)
            ## 给站点加注释
            ax.text(lon-0.3 ,
                    lat + 0.05,
                    sta_name,
                    transform=ccrs.PlateCarree(),
                    fontsize=8,
                    )

def get_hgt_met(flnm):
    # 从met文件中获取海拔高度数据
    ds = xr.open_dataset(flnm)
    hgt_m = ds['HGT_M'].squeeze()
    lat = ds['XLAT_M'].squeeze()
    lon = ds['XLONG_M'].squeeze()

    hgt = hgt_m.assign_coords({'lat':(['south_north', 'west_east'],lat.values),
                        'lon':(['south_north', 'west_east'],lon.values)})
    return hgt

def draw_contourf_lambert(terrain, ax):

    """rain[lon, lat, data],离散格点的DataArray数据
    使用lambert投影画这个地形图
    Args:
        rain ([type]): [description]
    Example:
    da = xr.open_dataarray('/mnt/zfm_18T/fengxiang/HeNan/Data/OBS/rain_station.nc')
    da.max()
    rain = da.sel(time=slice('2021-07-20 00', '2021-07-20 12')).sum(dim='time')
    """
    # from nmc_met_graphics.plot import mapview
    # mb = mapview.BaseMap()
    # cm = round(1/2.54, 2)
    # fig = plt.figure(figsize=[8*cm, 8*cm], dpi=300)
    # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=ccrs.LambertConformal(central_latitude=34, central_longitude=113))
    # mp = Map()

    # colorlevel = np.arange(0, 2300, 100)
    colorlevel = np.arange(0, 4000, 200)
    cmap = cmaps.MPL_terrain
    rain = terrain
    
    cs = ax.contourf(rain.lon, 
                    rain.lat,
                    rain,
                    levels=colorlevel,
                    # colors=colordict,
                    cmap=cmap,
                    transform=ccrs.PlateCarree())
    

    station = {
        'ZhengZhou': {
            'abbreviation':'郑州',
            'lat': 34.76,
            'lon': 113.65
        },
    }
    proj = ccrs.PlateCarree()  # 创建坐标系
    # mp.add_station(ax, station, justice=True, fontsize=10, ssize=8, dely=0.2)

    # Henan = cfeat.ShapelyFeature(
    #     Reader('/mnt/zfm_18T/fengxiang/DATA/SHP/Province_shp/henan.shp').geometries(),
    #     # Reader('/mnt/zfm_18T/fengxiang/DATA/SHP/shp_henan/henan.shp').geometries(),
    #     proj,
    #     edgecolor='black',
    #     lw=1.,
    #     linewidth=1.,
    #     facecolor='none',
    #     alpha=1.)
    # ax.add_feature(cfeature.RIVERS, lw=1)
    # ax.add_feature(Henan, linewidth=1, zorder=2)
    # ax.add_feature(cfeature.LAKES, lw=1)
    
    ## 调节图片标签
    # gl = ax.gridlines(draw_labels=True,
    #                   dms=True,
    #                   linestyle=":",
    #                   linewidth=0.2,
    #                   x_inline=False,
    #                   y_inline=False,
    #                   color='k',)
    
    # gl.top_labels = False  #关闭上部经纬标签
    # gl.right_labels = False
    # ## 这个东西还挺重要的，对齐坐标用的
    # gl.rotate_labels = None
    # ## 坐标的范围
    # gl.xlocator = mticker.FixedLocator(np.arange(100, 120, 2))
    # gl.ylocator = mticker.FixedLocator(np.arange(20, 40, 2))
    # ## 坐标标签的大小
    # gl.xlabel_style = {'size': 10}  #修改经纬度字体大小
    # gl.ylabel_style = {'size': 10}
    # ## 坐标标签样式
    # gl.xformatter = LongitudeFormatter(degree_symbol="${^\circ}$")
    # gl.yformatter = LatitudeFormatter(degree_symbol="${^\circ}$")
    # ax.spines['geo'].set_linewidth(1.0)  #调节图片边框粗细


    
    # fig_path = '/mnt/zfm_18T/fengxiang/HeNan/Draw/picture_terrain/'
    # fig_name = fig_path+pic_dic['title']+'_lambert'
    # fig.savefig(fig_name, bbox_inches = 'tight')
    return cs

def draw():
    pass
    file_folder = '/home/fengx20/project/hydro/Draw/'
    # file_folder = '/home/fengx20/project/hydro/Draw/'
    file_name = "namelist.wps_weihe_upstream"
    flnm = file_folder + file_name
    print(flnm)

    info = get_information(flnm)  # 获取namelist.wps文件信息
    # print(info['ref_lat'])
    ax, fig = create_map(info)  # 在domain1区域内，添加地理信息，创建底图
    print("创建地图完毕")
    draw_d02(info)  # 绘制domain2区域
    # print("绘制完毕")

    draw_station(ax, )
    # print("标注站点完毕")


    flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    met_h90 = get_hgt_met(flnm_90m_met)
    cs = draw_contourf_lambert(met_h90,  ax)

    colorlevel = np.arange(0, 4000, 200)
    # colorticks = colorlevel[1:-1][::4]
    colorticks = colorlevel[1:-1][::4]
    # cb = fig.colorbar(
    #     cs,
    #     # cax=ax6,
    #     orientation='horizontal',
    #     # orientation='vertical',
    #     ticks=colorticks,
    #     # ticks = [100, 200], 
    #     fraction = 0.05,  # 色标大小,相对于原图的大小
    #     pad=0.11,  #  色标和子图间距离
    # )
    # cb.ax.tick_params(labelsize=10)  # 设置色标标注的大小
    


    fig_folder = '/home/fengx20/project/hydro/Draw/figure/'
    fig_name = fig_folder+'domain_weihe.png'
    plt.savefig(fig_name)



# %%

if __name__ == '__main__':
    draw()

# %%
