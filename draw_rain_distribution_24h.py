#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
降水分布图
实况降水，站点插值出
模式降水，原始的wrfout网格点(未插值)


更改这个东西，留下绘制多图的接口
色标， colorlevel, colordict这些可以放在外面定义
这个东西比较麻烦的一个是传参， 传着传着就复杂了
内核需要什么东西要搞清楚，然后要传递啥东西, 不同的图哪些东西是需要变的，哪些是不变的
有些东西需要变，但是在这里不是一个常变的变量，可以在类的属性里面设置， 在类的属性里面设置了，也可以变的好像
类的属性有个默认值之后，还可以改变
对象的属性是可以重新定义的
dr.colorlevel = [0, 1, 3,]
一般而言，画降水嘛，就是数据不一样
不同的试验会是地图啥的不一样，重写类就可以了

东西一定要简洁，思路一定要清晰，让别人和未来的自己一看就明白
把数据和图耦合起来
函数不要过长，也不要过短
-----------------------------------------
Time             :2021/09/27 15:45:32
Author           :Forxd
Version          :1.0
'''

# %%

import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# import cmaps
import sys
import pandas as pd
import datetime
sys.path.append('/home/fengx20/mypy/')
import os
from baobao.map import Map, get_rgb
from matplotlib import rcParams
config = {
    "font.family": 'serif', # 衬线字体
    "font.size": 12, # 相当于小四大小
    "font.serif": ['SimSun'], # 宋体
    "mathtext.fontset": 'stix', # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False # 处理负号，即-号
}
rcParams.update(config)
#%%

# flnm = '/home/fengx20/project/HeNan/Data/rain_obs.nc'
# ds = xr.open_dataset(flnm)
#
# ds['PRCP'].max()


# %%
# flnm = '/home/fengx20/project/HeNan/Data/HENAN_PRECIP/*.nc'
# flnm = '/home/fengx20/project/HeNan/Data/HENAN_PRECIP/Z_NAFP_C_BABJ_20210718000058_P_CLDAS_NRT_ASI_0P0625_HOR-PRE-2021071600.nc'
# # t_str = flnm.split('/')[-1].split('_')[-1].split('-')[-1].split('.')[0]
# # t = datetime.datetime.strptime(t_str,'%Y%m%d%H')
# # path = '/home/fengx20/project/HeNan/Data/HENAN_PRECIP/Z_NAFP_C_BABJ_20210721084125_P_CLDAS_RT_ASI_0P0625_HOR-PRE-2021072108.nc'
# # path = '/home/fengx20/project/HeNan/Data/HENAN_PRECIP/Z_NAFP_C_BABJ_20210721084125_P_CLDAS_RT_ASI_0P0625_HOR-PRE-2021072108.nc'
# ds = xr.open_dataset(flnm)
# ds
# # %%
# ds
# flnm = '/home/fengx20/project/HeNan/Data/rain_obs.nc'
# da = xr.open_dataarray(flnm)
# da
# # %%
# # da
# # da.time
# da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
# da
# # da = da.sum(dim='time') 
# # da

# %%


def save_rain_obs():
    path = '/home/fengx20/project/HeNan/Data/HENAN_PRECIP'
    fl_list = os.popen('ls {}/*.nc'.format(path))  # 打开一个管道
    fl_list = fl_list.read().split()
    flnm = fl_list[25]
    t_list = []
    for flnm in fl_list:
        t_str = flnm.split('/')[-1].split('_')[-1].split('-')[-1].split('.')[0]
        t = datetime.datetime.strptime(t_str,'%Y%m%d%H')
        print(t)
        # t = t-pd.Timedelta('8H')

        ds = xr.open_dataset(flnm)
        dds = ds.assign_coords({'time':t})
        t_list.append(dds)
    ds_all = xr.concat(t_list, dim='time')  # 因为那两个时次的数据，所以这些数据的时次有点混乱
    ds_all = ds_all.sortby('time') # 按顺序排列这个数据
    # ds_all

    dss = ds_all.rename({'LAT':'lat','LON':'lon'})['PRCP']
    flnm_save = '/home/fengx20/project/HeNan/Data/rain_obs.nc'
    dss.to_netcdf(flnm_save)

# %%
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
        self.colorlevel=[0, 0.1, 10, 25.0, 50, 100, 250,  700]#雨量等级
        self.colordict=['#F0F0F0','#A6F28F','#3DBA3D','#61BBFF','#0000FF','#FA00FA','#800040', '#EE0000']#颜色列表

        # self.colorlevel=[0, 0.1, 10, 25, 50, 100, 250, 400,600,800,1000, 2000]#雨量等级
        # rgbtxt = '/home/fengx20/project/HeNan/11colors2.rgb'
        # rgb = get_rgb(rgbtxt)
        # self.colordict = rgb

        # self.colorlevel=[0, 1, 10, 25, 50, 100, 250, 400,600,800,1000, 2000]#雨量等级
        # rgbtxt = '/home/fengx20/project/HeNan/11colors.txt'
        # rgb = get_rgb(rgbtxt)
        # self.colordict = rgb

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
            'lat2':37.5,
            'lon1':110.5,
            'lon2':110.5,
        }        
        self.map_dic = {
            'proj':ccrs.PlateCarree(),
            'extent':[103.85, 108, 33.55, 36.5],
            'extent_interval_lat':1,
            'extent_interval_lon':2,
        }
            
            
            

        self.path_province = '/mnt/zfm_18T/fengxiang/DATA/SHP/Province_shp/henan.shp'
        self.path_henan = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_henan/henan.shp'
        self.path_city = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_henan/zhenzhou/zhenzhou_max.shp'
        self.path_tibet = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_tp/Tibet.shp'
        self.picture_path = '/mnt/zfm_18T/fengxiang/Asses_PBL/Rain/picture'
        # self.station = {
        #         'ZhengZhou': {
        #             'abbreviation':'郑州',
        #             'lat': 34.76,
        #             'lon': 113.65
        #         },
        #         'NanYang': {
        #             'abbreviation':'南阳',
        #             'lat': 33.1,
        #             'lon': 112.49,
        #         },
        #         'LuShi': {
        #             'abbreviation':'卢氏',
        #             'lat': 34.08,
        #             'lon': 111.07,
        #         },
        #     }
        # self.station = {
        #     # 'ShangQiu': {
        #     #     'lat': 34.4072,
        #     #     'lon': 115.6303,
        #     #     'abbreviation':'商丘'
        #     # },
        #     'linjiacun': {
        #         'lat': 34.38,
        #         'lon': 107.05,
        #         'abbreviation':'linjiacun'
        #     },
        #     'zhangjiashan': {
        #         'lat': 34.63,
        #         'lon': 108.6,
        #         'abbreviation':'zhanghjiashan'
        #     },}
        
        

    def add_patch(self, area, ax):
        xy = (area['lon1'], area['lat1'])
        width = area['lon2']-area['lon1']
        height = area['lat2']-area['lat1']
        rect = patches.Rectangle(xy=xy, width=width, height=height, edgecolor='blue', fill=False, lw=1.5, ) # 左下角的点的位置
        ax.add_patch(rect)


    def draw_single(self, da,):
        """画单个的那种图

        Args:
            da (DataArray): 单个时次的降水
        """
        ax = self.ax
        ## 给图像对象叠加地图
        mp = Map()
        ax = mp.create_map(ax, self.map_dic)
        ax.set_extent(self.map_dic['extent'])
        # import cartopy.feature as cfeature
        # ax.add_feature(cfeature.RIVERS.with_scale('10m'), facecolor='None', edgecolor='b')
        proj = ccrs.PlateCarree()
        import cartopy.feature as cfeature

        from cartopy.io.shapereader import Reader, natural_earth
        
        Province = cfeature.ShapelyFeature(
            Reader('/home/fengx20/DATA/SHP/china2000/china2000.shp').geometries(),  # 快速画图的地图文件
            proj,
            edgecolor='black',
            lw=1.,
            linewidth=1.,
            facecolor='none',
            alpha=1.)
            
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
        ## 将青藏高原地形文件加到地图中区
        ax.add_feature(Province, linewidth=0.5, zorder=2, alpha=0.3)
        ax.add_feature(river23,  zorder=2, alpha=1)
        ax.add_feature(river4, zorder=2, alpha=1)
        # ax.add_feature(river5, zorder=2, alpha=0.7)
        
        
        
        

        # ax.set_extent([103.85, 110.15, 33.55, 37.37],
        #             crs=ccrs.PlateCarree())
        # mp.add_station(ax, self.station, justice=True, delx=-0.1)
        from draw_basin_terrain import draw_station
        draw_station(ax)

        

        
        if 'south_north' in da.dims:
            rain_max = da.max(dim=['south_north', 'west_east'])        
        elif 'lat' in da.dims:
            rain_max = da.max(dim=['lat', 'lon'])        
        else:
            print("出错啦")
            
        # ax.set_title('Max = %s'%(rain_max.values.round(1)), fontsize=10,loc='right')

        x = da.lon
        y = da.lat
        crx = ax.contourf(x,
                          y,
                          da,
                          corner_mask=False,
                          levels=self.colorlevel,
                          colors = self.colordict,
                          transform=ccrs.PlateCarree()
                          )
        # self.add_box(ax)
        return crx
        
    def draw_tricontourf(self, rain):
        """rain[lon, lat, data],离散格点的DataArray数据
        由离散格点的数据绘制降水
        Args:
            rain ([type]): [description]
        Example:
        da = xr.open_dataarray('/mnt/zfm_18T/fengxiang/HeNan/Data/OBS/rain_station.nc')
        da.max()
        rain = da.sel(time=slice('2021-07-20 00', '2021-07-20 12')).sum(dim='time')
        """
        ax = self.ax
        mp = Map()
        ax = mp.create_map(ax, self.map_dic)
        mp.add_station(ax, self.station, justice=True)

        ax.set_extent(self.map_dic['extent'])
        cs = ax.tricontourf(rain.lon, rain.lat, rain, levels=self.colorlevel,colors=self.colordict, transform=ccrs.PlateCarree())

        rain_max = rain.max()        
        ax.set_title('Max = %s'%(rain_max.values.round(1)), fontsize=8,loc='right')
        # ax.set_title('2021-07 20/00--21/00', fontsize=35,)
        # ax.set_title('OBS', fontsize=10,loc='right')
        return cs


class GetData():
    def obs(self,tt):
        """这个主要是进行数据处理
        包括创建一个图片对象

        Args:
            dr (_type_): 子图的类
        """
        pass
        # flnm = '/home/fengx20/project/HeNan/Data/rain_obs.nc'
        # flnm = '/home/fengx20/project/hydro/test2/DATA/rain/data/rain_obs.nc'
        flnm = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
        da = xr.open_dataarray(flnm)
        da = da.sel(time=tt)

        # da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
        # da = da.sel(time=slice('2021-07-18 01', '2021-07-23 00'))
        # da = da.sel(time=slice('2021-07-18 01', '2021-07-21 00'))
        # da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
        # da = da.sel(time=slice('2021-07-20 01', '2021-07-21 00'))
        # da = da.sel(time=slice('2021-07-20 01', '2021-07-21 00'))
        # da = da.sel(time=slice('2021-07-19 13', '2021-07-20 12'))
        # da = da.sel(time=slice('2021-07-19 13', '2021-07-20 12'))
        # da = da.sel(time=slice('2022-07-18 01', '2022-07-19 00'))
        # da = da.sel(time=slice('2022-07-14 01', '2022-07-18 00'))
        # da = da.sel(time=slice('2021-07-19 21', '2021-07-20 20'))
        # da = da.sel(time=slice('2021-07-16 20', '2021-07-20 20'))
        da = da.sum(dim='time') 
        return da

    def onemodel(self, model='gwd3'):
        pass

        # flnm = '/home/fengx20/project/test/gwd3/rain_d02_all.nc'
        flnm = '/home/fengx20/project/test/'+model+'/rain_wrfout_d02.nc'
        # flnm = '/home/fengx20/project/test/'+model+'.nc'
        da = xr.open_dataarray(flnm)
        da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
        da = da.sum(dim='time') 
        return da


def get_dr():
    cm = 1/2.54
    proj = ccrs.PlateCarree()  # 创建坐标系
    # fig = plt.figure(figsize=(8*cm, 8*cm), dpi=300)
    fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)
    # ax = fig.add_axes([0.13,0.15,0.82,0.8], projection=proj)
    ax = fig.add_axes([0.10,0.10,0.82,0.8], projection=proj)
    dr = Draw(fig, ax)
    return dr

# ## 画观测降水
def draw_obs():
    
    # times = pd.date_range('2022-07-13 01', '2022-07-18 00', freq='24H')    
    # for t in times:
    #     dr = get_dr()
    #     gd = GetData()
    #     t1 = t
    #     # t2 = t+pd.Timedelta('24H')
    #     t2 = t+pd.Timedelta('24H')
    #     ts = pd.date_range(t1, t2, freq='1H') 

    dr = get_dr()
    gd = GetData()
    ts = pd.date_range('2022-07-14 01', '2022-07-18 00', freq='1H')
    

    da = gd.obs(tt=ts)
    # cf = dr.draw_tricontourf(da)    
    cf = dr.draw_single(da)    
    cb = dr.fig.colorbar(
        cf,
        # cax=ax6,
        orientation='horizontal',
        ticks=dr.colorticks,
        fraction = 0.06,  # 色标大小,相对于原图的大小
        pad=0.11,  #  色标和子图间距离
        )
    cb.ax.tick_params(labelsize=8)  # 设置色标标注的大小
    labels = list(map(lambda x: str(x) if x<1 else str(int(x)), dr.colorticks))  # 将colorbar的标签变为字符串
    cb.set_ticklabels(labels)
    # dr.ax.set_title('OBS', loc='left')

    
    # fig_name = t1.strftime('%d日')
    fig_name = '14日~17日'
    print(fig_name)

    dr.ax.set_title(fig_name, loc='left')
    # fig_name = 'OBS_18'
    fig_path = '/home/fengx20/project/hydro/Draw/figure/'
    dr.fig.savefig(fig_path+fig_name)
    # dr.fig.colse()

# draw_obs()

# %%

def draw_model_one(model, flag):

    dr = get_dr()  # 画图的对象

    # path_main = '/home/fengx20/project/test/'
    # path_main = '/home/fengx20/project/test/grid_cu/'
    # flnm = path_main+model+'/rain_wrfout_d02'+'_'+flag+'.nc' # 原始降水数据存储路径+文件名
    # flnm = '/home/fengx20/project/wrfda/test1_2021_1912-2100/3dvar_sounding_surface/202107191200/wrf/rain_wrfout_d03_all.nc'
    flnm = '/home/fengx20/project/hydro/test2/DATA/WPS/WRF/rain_wrfout_d01_all.nc'
    # flnm = '/home/fengx20/project/wrfda/test1_2021_1912-2100/3dvar_sounding_surface/202107191200/nogwd/rain_wrfout_d03_all.nc'
    print(flnm)
    # flnm = '/home/fengx20/project/test/'+model+'.nc'
    da = xr.open_dataarray(flnm)
    # da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
    # da = da.sel(time=slice('2021-07-20 01', '2021-07-21 00'))
    da = da.sum(dim='time') 

    cf = dr.draw_single(da)    

    cb = dr.fig.colorbar(
        cf,
        # cax=ax6,
        orientation='horizontal',
        # orientation='vertical',
        ticks=dr.colorticks,
        # fraction = 0.06,  # 色标大小,相对于原图的大小
        fraction = 0.06,  # 色标大小,相对于原图的大小
        pad=0.1,  #  色标和子图间距离
        # pad=0.05,  #  色标和子图间距离
        )
    cb.ax.tick_params(labelsize=8)  # 设置色标标注的大小
    dr.ax.set_title(model+'-'+flag, loc='left')

    # area = {
    #     'lon1':113.3,
    #     'lon2':114,
    #     'lat1':35.3,
    #     'lat2':36.5,
    #     'interval':0.125,
    # }
    area = {
        'lat1':33.5,
        'lat2':36.5,
        'lon1':105.5,
        'lon2':110.5,
    }        
    # dr.add_patch(area, ax)

    cb.ax.tick_params(labelsize=10)  # 设置色标标注的大小
    labels = list(map(lambda x: str(x) if x<1 else str(int(x)), dr.colorticks))  # 将colorbar的标签变为字符串
    cb.set_ticklabels(labels)
    
    # fig_name = model+'_'+flag+'da_nogwd'
    fig_name = model+'_'+flag+'da'
    fig_path = '/home/fengx20/'
    dr.fig.savefig(fig_path+'ttttttt')

    
def draw_mpas():

    dr = get_dr()  # 画图的对象

    # path_main = '/home/fengx20/project/test/'
    # flnm = path_main+model+'/rain_wrfout_d02'+'_'+flag+'.nc' # 原始降水数据存储路径+文件名
    # print(flnm)
    # # flnm = '/home/fengx20/project/test/'+model+'.nc'
    # da = xr.open_dataarray(flnm)
    # da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
    # da = da.sum(dim='time') 

    
    flnm = '/home/fengx20/project/mpas/test3/grid_diag.nc'
    ds = xr.open_dataset(flnm)
    r = ds['rainc']+ds['rainnc']
    # r = ds['rainc'] # 积云降水
    # r = ds['rainnc']  # 格点降水
    # rr = r.sum(dim='Time')
    # rr = r.isel(Time=-1)
    rr = r.isel(Time=25)
    da = rr.rename({'latitude':'lat', 'longitude':'lon'})
    
    cf = dr.draw_single(da)    

    cb = dr.fig.colorbar(
        cf,
        # cax=ax6,
        orientation='horizontal',
        # orientation='vertical',
        ticks=dr.colorticks,
        # fraction = 0.06,  # 色标大小,相对于原图的大小
        fraction = 0.08,  # 色标大小,相对于原图的大小
        pad=0.1,  #  色标和子图间距离
        # pad=0.05,  #  色标和子图间距离
        )
    cb.ax.tick_params(labelsize=8)  # 设置色标标注的大小
    dr.ax.set_title('MPAS-CU', loc='left')

    # area = {
    #     'lon1':113.3,
    #     'lon2':114,
    #     'lat1':35.3,
    #     'lat2':36.5,
    #     'interval':0.125,
    # }
    # def add_patch(area):
    #     xy = (area['lon1'], area['lat1'])
    #     width = area['lon2']-area['lon1']
    #     height = area['lat2']-area['lat1']
    #     rect = patches.Rectangle(xy=xy, width=width, height=height, edgecolor='blue', fill=False, lw=1.5, ) # 左下角的点的位置
    #     dr.ax.add_patch(rect)
    # ad_patch(area)

    cb.ax.tick_params(labelsize=8)  # 设置色标标注的大小
    labels = list(map(lambda x: str(x) if x<1 else str(int(x)), dr.colorticks))  # 将colorbar的标签变为字符串
    cb.set_ticklabels(labels)
    
    fig_name = 'mpas_grid'
    fig_path = '/home/fengx20/project/HeNan/picture/'
    dr.fig.savefig(fig_path+fig_name)
    
    
def draw_test(model, flag):

    dr = get_dr()  # 画图的对象

    # path_main = '/home/fengx20/pzm/2014_07_11-12/wrf6h/'
    # flnm = path_main+model+'/rain_wrfout_d02'+'_'+flag+'.nc' # 原始降水数据存储路径+文件名
    flnm = '/home/fengx20/pzm/2014_07_11-12/wrf6h/rain_wrfout_d02_all.nc'
    print(flnm)
    # flnm = '/home/fengx20/project/test/'+model+'.nc'
    da = xr.open_dataarray(flnm)
    # da = da.sel(time=slice('2021-07-17 01', '2021-07-23 00'))
    da = da.sel(time=slice('2014-07-11 16', '2014-07-11 21'))
    da = da.sum(dim='time') 

    cf = dr.draw_single(da)    

    cb = dr.fig.colorbar(
        cf,
        # cax=ax6,
        orientation='horizontal',
        # orientation='vertical',
        ticks=dr.colorticks,
        # fraction = 0.06,  # 色标大小,相对于原图的大小
        fraction = 0.06,  # 色标大小,相对于原图的大小
        pad=0.1,  #  色标和子图间距离
        # pad=0.05,  #  色标和子图间距离
        )
    cb.ax.tick_params(labelsize=8)  # 设置色标标注的大小
    dr.ax.set_title(model+'-'+flag, loc='left')

    area = {
        'lon1':113.3,
        'lon2':114,
        'lat1':35.3,
        'lat2':36.5,
        'interval':0.125,
    }
    # def ad_patch(area):
    #     xy = (area['lon1'], area['lat1'])
    #     width = area['lon2']-area['lon1']
    #     height = area['lat2']-area['lat1']
    #     rect = patches.Rectangle(xy=xy, width=width, height=height, edgecolor='blue', fill=False, lw=1.5, ) # 左下角的点的位置
    #     dr.ax.add_patch(rect)
    # ad_patch(area)

    cb.ax.tick_params(labelsize=10)  # 设置色标标注的大小
    labels = list(map(lambda x: str(x) if x<1 else str(int(x)), dr.colorticks))  # 将colorbar的标签变为字符串
    cb.set_ticklabels(labels)
    
    fig_name = model+'_'+flag
    fig_path = '/home/fengx20/'
    dr.fig.savefig(fig_path+fig_name)


if __name__ == '__main__':

    # draw_test('test', 'all')

    # save_rain_obs()
    draw_obs()

    # draw_mpas()

    # model_list = ['1600', '1612', '1700']
    # flag_list = ['all', 'grid', 'cu']

    # for model in model_list:
    #     for flag in flag_list:
            # draw_model_one(model, flag)
    # flag = 'all'
    # draw_model_one('tt', flag)
    
# %%
