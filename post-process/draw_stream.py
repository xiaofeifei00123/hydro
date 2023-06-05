# %%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import pandas as pd
import datetime
sys.path.append('/home/fengx20/mypy/')
from baobao.map import Map, get_rgb
import cartopy.crs as ccrs
import netCDF4 as nc
import wrf
from draw_basin_terrain import draw_station, draw_river_basin
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
# %%
# flnm = '/home/fengx20/project/hydro/heihe/RUN/route_01/201006010000.CHRTOUT_DOMAIN1'
# ds = xr.open_dataset(flnm)
# flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHRTOUT_GRID*'
flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake_0710-0720/*CHRTOUT_GRID*'
ds = xr.open_mfdataset(flnm)
# da = ds['streamflow']
ds.load()

# da
# %%
# %%
flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/latlon_big.nc'
# flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon.nc'
# flnm_latlon = '/home/fengx20/project/hydro/test3/DATA/gis_50m/wrfhydro_gis/latlon_rtout.nc'
ds_latlon = xr.open_dataset(flnm_latlon)
ds_latlon
lat = ds_latlon['LATITUDE']
# lon = ds_latlon['LONGITUDE']
# lat = ds_latlon['LATITUDE'][::-1, :]
lon = ds_latlon['LONGITUDE'][:, ::-1]
# lon.shape
# %%
# cm = 1/2.54
# fig = plt.figure(figsize=(8*cm, 6*cm), dpi=300)
# proj = ccrs.PlateCarree()
# # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], proj=proj)
# ax = fig.add_axes([0.1, 0.1, 0.85, 0.8], projection=proj)


flnm_90m_met = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/geo_em.d01.nc'
ncfile = nc.Dataset(flnm_90m_met)
hgt = wrf.getvar(ncfile, "HGT_M")
proj_lambert = wrf.get_cartopy(hgt)
proj = ccrs.PlateCarree()  # 创建坐标系
## 创建坐标系
cm = 1/2.54
fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)  # 创建页面
ax = fig.add_axes([0.1, 0.1, 0.85, 0.8], projection=proj_lambert)
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



ax.set_extent([103.85, 110.15, 33.55, 37.37],
                crs=ccrs.PlateCarree())

da = ds['streamflow'].sel(time='2022-07-16 11')
# crs = ax.contourf(lon, lat, da.values, levels=[0, 200,500, 1000, 2000, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
crs = ax.contourf(lon, lat, da.values, levels=[0, 1000, 1500, 2000,2500, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
ax.set_title('2022-07-15 00', loc='left')
# crs = ax.scatter(lon, lat, da.values/100,  color='blue', transform=ccrs.PlateCarree())
draw_station(ax)
draw_river_basin(fig, ax)
fig.colorbar(crs, orientation='horizontal', fraction=0.05, pad=0.11)
fig.savefig('./figure/1600.png')

# %%
import cmaps
da.plot(levels=30, cmap=cmaps.WhiteBlue)

# %%
# da.min()
flnm2 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHRTOUT_DOMAIN*'
ds2 = xr.open_mfdataset(flnm2)
ds2.load()
# %%

# fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)  # 创建页面
# ax = fig.add_axes([0.1, 0.1, 0.85, 0.8], projection=ccrs.PlateCarree())
# db = ds2['streamflow'].sel(time='2022-07-15 00')
# lon = db.longitude.values
# lat = db.latitude.values
# crs = ax.tricontourf(lon, lat, db.values, levels=[0, 200,500, 1000, 2000, 3000], colors=['white','green', 'blue', 'red', 'brown', ], transform=ccrs.PlateCarree())
#%%
# len(db)

# da.plot()
# %%

# %%
da.max()

#%%

cm = 1/2.54
fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
lon = da.longitude.values
lat = da.latitude.values
ax.contourf(lon, lat, da.values)


# %%
ds = xr.open_dataset(flnm)

# ds.P.max()

# %%
fn = nc.Dataset(flnm)
pre = wrf.getvar(fn,'pressure')
# %%
pre.max()
# ds
# %%
# ds['P']
pre.dims

# %%
# ds['P'][0,:,20,20].values[12]
lon = 114.5
lat = 31.5
x,y = wrf.ll_to_xy(fn, lat,lon)
z = np.abs(pre[:,y,x].values-500).argmin()
z
# x,y
# z.min()
# pre[z,y,x]
# print(x.values,y.values,z)
print(pre.dims)
print(z,y.values,x.values)
# %%
z
# %%
# ds['P'][0,z,y,x]
pre[z,y,x]

# %%
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/wrfinput_d01.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/wrfinput_d01.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_new/DOMAIN/wrfinput_d01.nc'
# flnm = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/WRF/wrfinput_d02'
flnm = '/home/fengx20/project/hydro/test3/DATA/create_wrfinput/WPS/WRF/wrfinput_d01'
ds = xr.open_dataset(flnm)
# ds.Time
ds.Times
# %%
# ds.Times

# %%
flnm8 = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/2008121000.LDASIN_DOMAIN1'
flnm9 = '/home/fengx20/project/hydro/test_case/oahui/NWM/FORCING/200812101600.PRECIP_FORCING.nc'
ds8 = xr.open_dataset(flnm8)
ds9 = xr.open_dataset(flnm9)
# ds8.load()
# ds9.load()
# %%
# ds8['lambert_conformal_conic']
# ds8['RAINRATE']
# ds9['precip']
# ds9

# ds9
# csv = './渭河流域逐日径流.xlsx'
# # df = pd.read_table(csv, sep='\s+')
# # df
# df = pd.read_excel(csv)
# # df['站名']
# df2 = df[df['站名'] == '临潼']
# df3 = df2[['时间','流量(立方米/秒)']]
# # type(df3['时间'].values).astype('pd.time64')
# xx = df3['时间'].values
# xx = xx-pd.Timedelta('8H')
# yy = df3['流量(立方米/秒)']
# cm = 1/2.54
# fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
# ax = fig.add_axes([0.17, 0.25, 0.8, 0.65])
# ax.plot(xx,yy)
# # xx
# # df3.plot()
# # yy
# # %%
# yy.max()


# %%
# flnm = '/home/fengx20/project/hydro/test3/RUN/route/*CHANOBS*'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_6/*CHANOBS*'
# flnm0 = '/home/fengx20/project/hydro/test3/RUN/route_new/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/test/route11/*CHANOBS*'
# flnm2 = '/home/fengx20/project/hydro/test3/RUN/route_01/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/heihe/RUN/route_01/back/*CHANOBS*'
flnm1 = '/home/fengx20/project/hydro/heihe/RUN/route_01/back/*CHRTOUT*'
ds1 = xr.open_mfdataset(flnm1)
# ds2 = xr.open_mfdataset(flnm2)
ds1.load()
# ds2.load()
# %%
# ds1['streamflow'][0,20,:].argmax()
da = ds1['streamflow'][0,:,23830]
# da
da.max()


# %%
da.time
#%%
# da = ds1['streamflow'].isel(feature_id=2)
fig = plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_axes([0.15, 0.15, 0.8,0.8])
tt  = da.time.values
ax.plot(tt, da.values)
ax.set_xticklabels(da.time.dt.strftime('%d'), rotation=30)
plt.show()
fig.savefig('figure/ttt.png')

#.plot()
# ds2['streamflow'].isel(feature_id=2).plot()
# %%
flnm3 = '/home/fengx20/project/hydro/test3/RUN/route_new_cmorph/*CHANOBS*'
ds3 = xr.open_mfdataset(flnm3)
ds3.load()
# %%
flnm6 = '/home/fengx20/project/hydro/test3/RUN/test/route10/*CHANOBS*'
ds6 = xr.open_mfdataset(flnm6)
ds6.load()
# %%
# ds6['streamflow'].isel(feature_id=2).plot()
ds1['streamflow'].isel(feature_id=2).plot()
ds2['streamflow'].isel(feature_id=2).plot()

# %%
flnm4 = '/home/fengx20/project/hydro/test3/RUN/test/route11_input13/*CHRTOUT*'
flnm5 = '/home/fengx20/project/hydro/test3/RUN/test/route11/*CHRTOUT*'
ds4 = xr.open_mfdataset(flnm4)
ds4.load()
ds5 = xr.open_mfdataset(flnm5)
ds5.load()
# ds1['streamflow'].isel(feature_id=2).plot()
# ds2['streamflow'].isel(feature_id=2).plot()
# ds3['streamflow'].isel(feature_id=2).plot()
# %%
# ds4['streamflow'].sel(feature_id=26842).max()
# ds5['streamflow'].sel(feature_id=26842).max()
# %%
ds3['streamflow'].isel(feature_id=2).plot()

# %%

# flnm = '/home/fengx20/project/hydro/test3/RUN/route/*CHANOBS*'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route/*CHRTOUT*'
flnm = '/home/fengx20/project/hydro/test3/RUN/route_new_cmorph/*CHANOBS*'
ds = xr.open_mfdataset(flnm)
ds.load()

# %%
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/grid_new/*CHANOBS*'
# flnm2 = '/home/fengx20/project/hydro/test3/RUN/grid_new/*CHRTOUT_DOMAIN*'
flnm2 = '/home/fengx20/project/hydro/test3/RUN/grid_new_sta/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/route_6/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/route_new/*CHRTOUT*'
# ds1 = xr.open_mfdataset(flnm1)
ds2 = xr.open_mfdataset(flnm2)
ds2.load()
# %%
ds2['streamflow'].isel(feature_id=1).max()
# ds2['streamflow'].max()
# ds2.latitude.values
# ds2.longitude.values
# flnm2 = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
# ds2 = xr.open_dataset(flnm2)
# %%

# ds3 = ds3.isel(reference_time=0)
# %%
# da.values.shape
class Draw(object):
    """画单张降水图的
    只管画图，不管标注
    Args:
        object (_type_): _description_
    """

    def __init__(self, fig, ax) -> None:
        super().__init__()
        self.fig = fig
        self.ax = ax
        # self.colorlevel=[0, 0.1, 10, 25.0, 50, 100, 250,  700]#雨量等级
        # self.colordict=['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表

        # self.colorlevel=[0, 0.1, 10, 25, 50, 100, 250, 400,600,800,1000, 2000]#雨量等级
        # rgbtxt = '/home/fengx20/project/HeNan/11colors2.rgb'
        # rgb = get_rgb(rgbtxt)
        # self.colordict = rgb

        self.colorlevel=[0, 1, 10, 25, 50, 100, 250, 400,600,800,1000, 2000]#雨量等级
        rgbtxt = '/home/fengx20/project/HeNan/11colors.txt'
        rgb = get_rgb(rgbtxt)
        self.colordict = rgb

        # self.colorlevel = [0, 0.1, 2.5, 7.5, 15, 35, 70, 700]
        # self.colordict = ['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']
        
        


        # self.colorlevel=[0, 1, 10, 25, 50, 100, 200, 250, 300, 400,600,800,1000, 2000]#雨量等级
        # rgbtxt = '/home/fengx20/project/HeNan/14colors.rgb'
        # rgb = get_rgb(rgbtxt)
        # self.colordict = rgb

        # self.colordict=['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表
        # self.colorlevel=[0, 0.1, 10, 25.0, 50, 100, 250, 400,600, 1000]#雨量等级
        # self.colordict = select_cmap('rain9')
        self.colorticks = self.colorlevel[1:-1]
        # self.map_dic = {
        #         'proj':ccrs.PlateCarree(),
        #         'extent':[108, 119, 30, 38],
        #         'extent_interval_lat':1,
        #         'extent_interval_lon':2,
        #     }
        # self.map_dic = {
        #         'proj':ccrs.PlateCarree(),
        #         # 'extent':[108, 119, 30, 38],
        #         'extent':[90, 140, 20, 50],
        #         'extent_interval_lat':10,
        #         'extent_interval_lon':10,
        #     }

        # self.map_dic = {
        #     'proj':ccrs.PlateCarree(),
        #     'extent':[113, 117, 31, 33],
        #     'extent_interval_lat':1,
        #     'extent_interval_lon':1,
        # }
            
        area = {
            'lat1':33.5,
            'lat2':36.5,
            'lon1':105.5,
            'lon2':110.5,
        }        
        self.map_dic = {
            'proj':ccrs.PlateCarree(),
            'extent':[104, 115.5, 32, 37],
            'extent_interval_lat':1,
            'extent_interval_lon':2,
        }
            
            
            

        self.path_province = '/mnt/zfm_18T/fengxiang/DATA/SHP/Province_shp/henan.shp'
        self.path_henan = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_henan/henan.shp'
        self.path_city = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_henan/zhenzhou/zhenzhou_max.shp'
        self.path_tibet = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_tp/Tibet.shp'
        self.picture_path = '/mnt/zfm_18T/fengxiang/Asses_PBL/Rain/picture'
        
        
        self.station = {
            'WeiJiabao': {
                'lat': 34.289957,
                'lon': 107.72644,
                'abbreviation':'weijiabao'
            },
            'lintong': {
                'lat': 34.430699,
                'lon': 109.20191,
                'abbreviation':'lintong'
            },
            'huaxian': {
                'lat': 34.582697,
                'lon': 109.76097,
                'abbreviation':'linjiacun'
            },
            'zhangjiashan': {
                'lat': 34.6333,
                'lon': 105.6,
                # 'abbreviation':'zhanghjiashan'
                'abbreviation':'张家山'
            },
            'zhuangtou': {
                'lat': 35.005,
                'lon': 109.839,
                'abbreviation':'zhuangtou'
            },}


mp = Map()


# %%
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_new_cmorph/*CHRTOUT*'
flnm = '/home/fengx20/project/hydro/test3/RUN/test/route10/*CHRTOUT*'
ds3 = xr.open_mfdataset(flnm)
ds3.load()

# %%
# ds3
da = ds3['streamflow'].sel(time='2022-07-12 00')
da

# ds3.time
lat = da.longitude.values
lon = da.latitude.values
import matplotlib.pyplot as plt
cm = 1/2.54
fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree())
# dr = Draw(fig, ax)

# crs = ax.tricontourf(lon, lat, da.values)
crs = ax.tricontourf(lat, lon, da.T.values)
fig.colorbar(crs)
# import cartopy.feature as cfeature
# ax.add_feature(cfeature.RIVERS.with_scale('10m'), facecolor='None', edgecolor='b')
# ax.set_extent(self.map_dic['extent'])


# %%
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/FORCING/2022071600.LDASIN_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_6/FORCING/2022071015.LDASIN_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/soil_properties.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/Fulldom_hires.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/GEOGRID_LDASOUT_Spatial_Metadata.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/GWBASINS.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/GWBUCKPARM.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/soil_properties.nc'

# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/hydro2dtbl.nc'
# flnm = '/home/fengx20/project/hydro/test3/RUN/route_10/DOMAIN/Route_Link.nc'
# ds = xr.open_dataset(flnm)
# ds['Basin']
# ds.time
# ds.Time
# ds['RAINRATE'].max()

# ds['streamflow'].isel(feature_id=2).plot()
# ds1['streamflow'].isel(feature_id=2).plot()
# ds3['streamflow']#.isel(feature_id=2).plot()
# ds3['streamflow'].isel(reference_time=1).isel(feature_id=1).plot()
# ds0['streamflow'].isel(feature_id=2).plot()
# ds3['streamflow'].isel(feature_id=2).plot()
# (ds['streamflow'].isel(feature_id=1) - ds0['streamflow'].isel(feature_id=1)).plot()
# ds['streamflow'].max()
# ds1['streamflow'].max()
# ds.time
# ds1.time
ds3['streamflow'].isel(feature_id=1).plot()
# %%
# ds.feature_id[2].values  # feature_id
# id = 1, 魏嘉宝
# id = 2, 临潼
# ds['streamflow'].isel(feature_id=1)
# ds2['PRCP'].isel(time=)
# ds['streamflow'].isel(time=50).idxmin()
# ds['streamflow'].isel(time=50).idxmax()
# ds['streamflow'].sel(feature_id=28951).plot()
# ds['streamflow'].sel(feature_id=29568).plot()
# ds['streamflow'].latitude==36.199173
# np.argwhere(ds['streamflow'].latitude.values==36.199173)
for i in range(1, 10000):
    # aa = ds['streamflow'][:, 6920]
    # aa = ds['streamflow'][50, i]
    da11 = ds['streamflow'][50, i]
    da12 = ds1['streamflow'][50, i]
    aa = da11-da12
    if aa>0.0:
        if aa<0.015:
            if da11 < 10:
                print(i)

# %%
aa

# %%
# x
# y[1]
# ds['streamflow'].sel(feature_id=3333).plot()
for tt in range(23,24):
    print(tt)
    idx = (ds.isel(time=tt)['streamflow'] - ds1.isel(time=tt)['streamflow']).argmax()
    idx = idx.values
    # ds.isel(feature_id=idx)
    xx = ds.isel(feature_id=idx)['streamflow'] - ds1.isel(feature_id=idx)['streamflow']
    # ds.isel(feature_id=idx)['streamflow'].plot(color='black')
    # ds1.isel(feature_id=idx)['streamflow'].plot(color='black')
    xx.plot(color='red')
    # plt.set_ylim(0, 100)
# %%
csv = './渭河流域逐日径流.xlsx'
fi = ds.feature_id[1].values  # feature_id
# fi = ds.feature_id[29568].values  # feature_id
# fi = 29568
# fi = 28951
# fi = 7777
# fi = 1
# for fi in np.arange(1, 1000, 1):
df = pd.read_excel(csv)
# df['站名']
# df2 = df[df['站名'] == '临潼']
df2 = df[df['站名'] == '华县']
# df2 = df[df['站名'] == '魏家堡']
df3 = df2[['时间','流量(立方米/秒)']]
# type(df3['时间'].values).astype('pd.time64')
xx = df3['时间'].values
xx = xx-pd.Timedelta('8H')
yy = df3['流量(立方米/秒)']

da11 = ds['streamflow'].sel(feature_id=fi)
da12 = ds1['streamflow'].sel(feature_id=fi)
(da11-da12).plot()
# da11.plot()
# da12.plot()
lat = da11.latitude.values
lon = da11.longitude.values
db = ds2['PRCP'].sel(lat=lat, method='nearest').sel(lon=lon, method='nearest')
# db = ds2['PRCP'].mean(dim=['lat', 'lon'])
ttt = pd.date_range('2022-07-14 00', '2022-07-18 00', freq='1H')
# labels = da11.sel(time=ttt).time.dt.strftime('%dT%H:00')
labels = da11.sel(time=ttt).time.values
x = labels
y = da11.sel(time=ttt).values
y22 = da12.sel(time=ttt).values
y1 = db.sel(time=ttt).values
cm = 1/2.54
fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.17, 0.25, 0.8, 0.65])
ax2 = ax.twinx()
# ax3 = ax.twinx()
# ax.plot(x,y[1], label='streamflow', color='red', linestyle='--')
ax.plot(x,y, label='streamflow3', color='red', linestyle='--')
ax.plot(x,y22, label='streamflow6', color='blue', linestyle='-.')
# ax.scatter(xx,yy,s=5, c='k', label='OBS')
ax.plot(xx,yy, color='black', marker='o', label='OBS')
ax2.bar(x,y1, label='precipitation', color='black', linestyle='-', width=0.02)
ax.set_ylim(0, 4000)

labels = da11.sel(time=ttt).time.dt.strftime('%dT%H').values
# ax.set_xticks(labels[::24])
ax.set_xticklabels(labels[::12], rotation=30, fontsize=10)

# ax.set_title('魏家堡', loc='left',fontproperties=font)
fontdict={"family": "SimHei", "size": 10, "color": "k"}
# ax.set_title('魏家堡', loc='left',fontdict=fontdict)
ax.set_title('华县', loc='left',fontdict=fontdict)
# ax.set_title('临潼', loc='left',fontdict=fontdict)
# ax.set_title(str(da11.latitude.values), loc='left')
# ax.set_title(str(da11.longitude.values), loc='right')
# ax.set_xticks(labels[::24].values)
# ax.set_xticklabels(labels.values[::24], rotation=30, fontsize=10)
ax.set_xlabel('Time')
ax.set_ylabel('Stream flow ($m^3\cdot s^{-1}$)')
ax2.set_ylabel('precipitation ($mm/h$)')
ax.legend(edgecolor='white',)
ax2.legend(edgecolor='white',bbox_to_anchor=(0.60,0.68))
figpath = '/home/fengx20/project/wrf-hydro/.virtual_documents/figure/'
fig.savefig(figpath+'1.png')
# %%
cm = 1/2.54
fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.17, 0.25, 0.8, 0.65])
fi = 1338
# fi = 2871
# fi = 33823
da11 = ds['streamflow'][:,fi]
da12 = ds1['streamflow'][:,fi]
# ((da11-da12)*10).plot()
# da11.plot()
# da12.plot()
# labels = da11.time.values
ttt = pd.date_range('2022-07-14 00', '2022-07-18 00', freq='1H')
# labels = da11.sel(time=ttt).time.dt.strftime('%dT%H:00')
labels = da11.sel(time=ttt).time.values
da11 = da11.sel(time=ttt)
da12 = da12.sel(time=ttt)
ax.plot(labels, da11, label='streamflow3', color='blue')
ax.plot(labels, da12, label='streamflow6', color='red')
ax.plot(labels, (da11-da12)*10, label='(s3-s6)*10', color='black')
ax.legend(edgecolor='white')

labels = da11.sel(time=ttt).time.dt.strftime('%dT%H').values
ax.set_xticklabels(labels[::12], rotation=30, fontsize=10)
ax.set_xlabel('Time')
ax.set_ylabel('Stream flow ($m^3\cdot s^{-1}$)')
lat = da11.latitude.values.round(2)
lon = da11.longitude.values.round(2)
ax.set_title('lon=%s, lat=%s'%(str(lon), str(lat)), loc='left')
# ax.set_xticklabels(labels[::12], rotation=30, fontsize=10)
# %%
# lat = da11.latitude.values.round(2)
# lon = da11.longitude.values.round(2)
k = np.arange(1, 10)
rs = 1-1/np.e**(-k)+10000
# rs
# rs
cm = 1/2.54
fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.17, 0.25, 0.8, 0.65])
ax.plot(k, rs)