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
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature
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
                    s=12, 
                    zorder=5,
                    )
            ## 给站点加注释
            ax.text(lon-0.2 ,
                    lat + 0.06,
                    sta_name,
                    transform=ccrs.PlateCarree(),
                    fontsize=9,
            )

# %%
def draw_river_basin(fig, ax):
    flnm = '/home/fengx20/project/hydro/test3/DATA/gis_100m/outputs/test/Fulldom_hires.nc'
    ds = xr.open_dataset(flnm)
    dd = ds['basn_msk']
    db = xr.where(dd==-9999, 0,dd)

    flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
    ds_latlon = xr.open_dataset(flnm_latlon)
    lat = ds_latlon['LATITUDE'][::-1, :]
    lon = ds_latlon['LONGITUDE'][:, ::-1]
    proj = ccrs.PlateCarree()  # 创建坐标系
    colordict = ['green', 'red', 'blue', 'blue', 'black']

    ###画流域分布
    ax.contour(lon, lat, db, levels=10, colors='orange', transform=ccrs.PlateCarree(), linewidths=0.9, alpha=0.7)
    draw_station(ax)  #标记站点

# %%
def create_map():
    """创建一个包含青藏高原区域的Lambert投影的底图

    Returns:
        ax: 坐标图对象
    """
    ## --创建画图空间
    # flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
    flnm_90m_met = '/home/fengx20/project/hydro/test_ground/RUN/DOMAIN/geo_em.d01.nc'
    ncfile = nc.Dataset(flnm_90m_met)

    hgt = wrf.getvar(ncfile, "HGT_M")
    # Get the cartopy mapping object
    proj_lambert = get_cartopy(hgt)
    # proj = ccrs.PlateCarree()  # 创建坐标系
    ## 创建坐标系
    cm = 1/2.54
    fig = plt.figure(figsize=(8*cm, 7*cm), dpi=300)  # 创建页面
    ax = fig.add_axes([0.1, 0.11, 0.85, 0.8], projection=proj_lambert)
    

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
        


    ax.add_feature(river,  zorder=2, alpha=1)
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

    return ax, fig


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


def main():
    ax, fig = create_map()
    draw_station(ax)  #标记站点
    # draw_river_basin(fig, ax)
    # create_map(fig, ax)

    flnm_90m_met = '/home/fengx20/project/hydro/test_ground/WPS/geo_em.d01.nc'
    flnm_fd = '/home/fengx20/project/hydro/test_ground'
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
    fig.savefig('/home/fengx20/project/hydro/figure/weiheshangyou_domain.svg')


if __name__ == "__main__":
    main()


# %%
# flnm_csv = '/home/fengx20/project/hydro/Draw/station_latlon.csv'
# df = pd.read_csv(flnm_csv)
# col = ['code', 'lat', 'lon', 'name']
# df1 = df[col]
# df2 = df1.rename(index=str, columns={'code':'id'})
# df2
# for i in df2['name']:
#     print('叠加%s站点'%i.strip())
#     df3 = df2[df2.name.str.contains(i)]
#     lon = df3['lon'].values[0]
#     lat = df3['lat'].values[0]
#     sta_name = df3['name'].values[0].strip()
#     print(lon, lat, sta_name)
# # %%
# # df3.name.strip()
# # df2['name'][0]
# # sta_name
# # lon

# # ds.sel(name='华县')
# # ds.sel(name='华县')
# # ds.sel(id=41101600)
# # df3['华县']
# # df1.rename(columns={'id':'code'}, inplace=True)
# #%%






