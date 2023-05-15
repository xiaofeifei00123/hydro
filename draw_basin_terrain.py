# %%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmaps
import netCDF4 as nc
import wrf
from matplotlib import rcParams
import cartopy.crs as ccrs
import cartopy.crs as ccrs
# import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature
import salem
# import geopandas
# import maskout
# from draw_domain_cartopy_weihe import draw_station
import netCDF4 as nc

from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}
rcParams.update(config)

# %%
# rcParams['font.family'] = 'Times New Roman'  # 设置字体
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
                    s=18, 
                    zorder =5)
            ## 给站点加注释
            ax.text(lon-0.2 ,
                    lat + 0.05,
                    sta_name,
                    transform=ccrs.PlateCarree(),
            )


# def draw_station(ax,):
#     """画站点
#     """
#     station = {
#         'WeiJiabao': {
#             'lat': 34.289957,
#             'lon': 107.72644,
#             'abbreviation':'魏家堡'
#         },
#         'lintong': {
#             'lat': 34.430699,
#             'lon': 109.20191,
#             'abbreviation':'临潼'
#         },
#         'huaxian': {
#             'lat': 34.582697,
#             'lon': 109.76097,
#             'abbreviation':'华县'
#         },
#         # 'zhangjiashan': {
#         #     'lat': 34.6333,
#         #     'lon': 105.6,
#         #     # 'abbreviation':'zhanghjiashan'
#         #     'abbreviation':'张家山',
#         # },
#         'zhuangtou': {
#             'lat': 35.005,
#             'lon': 109.839,
#             'abbreviation':'状头'
#         },
#         'jingcun': {
#             'lat': 35.000,
#             'lon': 108.13333,
#             'abbreviation':'景村'
#         },
#     }
#     values = station.values()
#     # station_name = list(station.keys())
#     # station_name = list(station[])
#     # print(type(station_name[0]))
#     # print(station_name[0])
#     x = []
#     y = []
#     station_name = []
#     for i in values:
#         y.append(float(i['lat']))
#         x.append(float(i['lon']))
#         station_name.append(i['abbreviation'])

#     ## 标记出站点
#     ax.scatter(x,
#                y,
#                color='black',
#                transform=ccrs.PlateCarree(),
#                linewidth=1,
#                s=18, 
#                zorder =5)
#     ## 给站点加注释
#     fontdict={"family": "SimSun", "size": 10, "color": "k"}
#     for i in range(len(x)):
#     # for i,j in zip(len(x), values):
#         ax.text(x[i]-0.5 ,
#                  y[i] + 0.1,
#                  station_name[i],
#                  transform=ccrs.PlateCarree(),
#                  fontdict=fontdict
#         )
# %%
def draw_river_basin(fig, ax):
    # flnm = '/home/fengx20/project/hydro/test3/RUN/grid_new_sta/DOMAIN/Fulldom_hires.nc'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/DOMAIN/Fulldom_hires.nc'
    flnm = '/home/fengx20/project/hydro/test3/DATA/gis_100m/outputs/test/Fulldom_hires.nc'
    ds = xr.open_dataset(flnm)
    ds
    dd = ds['basn_msk']
    # db = xr.where(dd==-9999, np.nan,dd)
    db = xr.where(dd==-9999, 0,dd)
    da = ds['FLOWACC']

    # flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/test.nc'
    flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
    # flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon.nc'
    # flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon_rtout.nc'
    ds_latlon = xr.open_dataset(flnm_latlon)
    ds_latlon
    # lat = ds_latlon['LATITUDE']
    # lon = ds_latlon['LONGITUDE']
    lat = ds_latlon['LATITUDE'][::-1, :]
    lon = ds_latlon['LONGITUDE'][:, ::-1]
    # lon
    # lon.shape
    # lat = ds['LONGITUDE'].values

    proj = ccrs.PlateCarree()  # 创建坐标系
    # fig = plt.figure(figsize=(4,3), dpi=300)
    # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
    # colordict = ['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']
    colordict = ['green', 'red', 'blue', 'blue', 'black']
    # crs = ax.contourf(lon,lat,da.values, cmap=cmaps.WhiteBlue, levels=[1*10**5, 5*10**5, 1*10**6, 1*10**7],colors=colordict,  zorder=2)
    # crs = ax.contourf(lon,lat,da.values, levels=[1*10**5, 5*10**5, 1*10**6, 1*10**7],colors=colordict,  zorder=2)
    # crs = ax.contour(lon,lat,da.values, levels=[1*10**5, 5*10**5, 1*10**6, 1*10**7],  zorder=2)

    ###画流域分布
    ax.contour(lon, lat, db, levels=10, colors='orange', transform=ccrs.PlateCarree(), linewidths=0.9, alpha=0.7)
    draw_station(ax)  #标记站点

    
    

    # ax.set_title('Times')
    # crs = ax.contourf(lon,lat,da.values, cmap=cmaps.cyclic, levels=1)
    # crs = ax.contourf(lon,lat,da.values)

    # crs = ax.scatter(lon,lat,da.values, color='blue')
    # ax.scatter(lon,lat)
    # fig.colorbar(crs)
# %%
# proj = ccrs.PlateCarree()  # 创建坐标系
# fig = plt.figure(figsize=(4,3), dpi=300)
# ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
# draw_river_basin(fig, ax)
# %%
def create_map():
    """创建一个包含青藏高原区域的Lambert投影的底图

    Returns:
        ax: 坐标图对象
    """
    ## --创建画图空间
    flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    ncfile = nc.Dataset(flnm_90m_met)

    hgt = wrf.getvar(ncfile, "HGT_M")
    # Get the cartopy mapping object
    proj_lambert = get_cartopy(hgt)
    proj = ccrs.PlateCarree()  # 创建坐标系
    ## 创建坐标系
    cm = 1/2.54
    fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)  # 创建页面
    # ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=proj)
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.8], projection=proj_lambert)
    # ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], projection=proj_lambert)
    

    ## 读取青藏高原地形文件


    
    # Province = cfeature.ShapelyFeature(
    #     Reader('/home/fengx20/DATA/SHP/china2000/china2000.shp').geometries(),  # 快速画图的地图文件
    #     proj,
    #     edgecolor='black',
    #     lw=1.,
    #     linewidth=1.,
    #     facecolor='none',
    #     alpha=1.)
        
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
    river5 = cfeature.ShapelyFeature(
        Reader('/home/fengx20/DATA/SHP/basin_shp/river_1_5/我国五级河流.shp').geometries(),  # 快速画图的地图文件
        proj,
        edgecolor='green',
        lw=1.,
        linewidth=0.5,
        facecolor='none',
        alpha=1.)
    # weihe = cfeature.ShapelyFeature(
    #     Reader('/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp').geometries(),  # 快速画图的地图文件
    #     proj,
    #     edgecolor='green',
    #     lw=1.,
    #     linewidth=0.5,
    #     facecolor='none',
    #     alpha=1.)
    ## 将青藏高原地形文件加到地图中区
    # ax.add_feature(Province, linewidth=0.5, zorder=2, alpha=0.3)
    ax.add_feature(river23,  zorder=2, alpha=1)
    ax.add_feature(river4, zorder=2, alpha=1)
    cs = ax.add_feature(river5, zorder=2, alpha=0.7)
    # ax.add_feature(weihe, zorder=2, alpha=0.7)
    
    # shp_path = '/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp'
    # clip = maskout.shp2clip(cs, ax, shp_path, proj=proj_lambert)


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
    # ax.set_extent([104, 106, 34, 36],
                #   crs=ccrs.PlateCarree())
    ax.set_extent([104, 108, 34, 36.5],
                  crs=ccrs.PlateCarree())

    # # 标注d01, 这个位置需要根据经纬度手动调整
    # ax.text(78, # 经度
    #         45,  # 纬度
    #         'd01',
    #         transform=ccrs.PlateCarree(),
    #         fontdict={
    #             'size': 12,
    #         })
    return ax, fig
# %%
def draw_contourf_lambert(terrain, ax):

    colorlevel = np.arange(0, 4000, 200)
    cmap = cmaps.MPL_terrain
    rain = terrain
    
    cs = ax.contourf(rain.lon, 
                    rain.lat,
                    rain,
                    levels=colorlevel,
                    # colors=colordict,
                    cmap=cmap,
                    transform=ccrs.PlateCarree(), 
                    )
    

    shp_path = '/home/fengx20/project/hydro/Draw/figure/weiheshp/123.shp'
    flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    ncfile = nc.Dataset(flnm_90m_met)
    hgt = wrf.getvar(ncfile, "HGT_M")
    proj_lambert = get_cartopy(hgt)
    # clip = maskout.shp2clip(cs, ax, shp_path, proj=proj_lambert)

    
    return cs
#%%

# flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
# flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'

def main():
    ax, fig = create_map()

    draw_river_basin(fig, ax)


    flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    # met_h90 = get_hgt_met(flnm_90m_met)
    ds = xr.open_dataset(flnm_90m_met)
    hgt_m = ds['HGT_M'].squeeze()
    lat = ds['XLAT_M'].squeeze()
    lon = ds['XLONG_M'].squeeze()

    met_h90 = hgt_m.assign_coords({'lat':(['south_north', 'west_east'],lat.values),
                        'lon':(['south_north', 'west_east'],lon.values)})
    cs = draw_contourf_lambert(met_h90,  ax)
    colorlevel = np.arange(0, 4000, 200)
    # colorticks = colorlevel[1:-1][::4]
    colorticks = colorlevel[1:-1][::4]
    cb = fig.colorbar(
        cs,
        # cax=ax6,
        orientation='horizontal',
        # orientation='vertical',
        ticks=colorticks,
        # ticks = [100, 200], 
        fraction = 0.05,  # 色标大小,相对于原图的大小
        pad=0.11,  #  色标和子图间距离
    )
    fig.savefig('/home/fengx20/project/hydro/Draw/figure/domain_test.png')
if __name__ == "__main__":
    main()
# %%
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
    print(lon, lat, sta_name)
# %%
# df3.name.strip()
# df2['name'][0]
# sta_name
# lon

# ds.sel(name='华县')
# ds.sel(name='华县')
# ds.sel(id=41101600)
# df3['华县']
# df1.rename(columns={'id':'code'}, inplace=True)
#%%






