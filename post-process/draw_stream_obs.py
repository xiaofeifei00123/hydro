#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
画预测的站点的径流量
-----------------------------------------
Time             :2023/02/03 16:51:48
Author           :Forxd
Version          :1.0
'''


#%%
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import pandas as pd
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

# %%  模拟数据

# flnm1 = '/home/fengx20/project/hydro/test3/RUN/route_01/output_14/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/grid_new_sta/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHANOBS*'
# flnm1 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHANOBS*'
flnm1 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/output/*CHANOBS*'
ds1 = xr.open_mfdataset(flnm1)
ds1.load()
# %%
# ds1['streamflow']
flnm = '/home/fengx20/project/hydro/test_ground/RUN/2002/200201040000.CHRTOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
# ds['streamflow'].plot()
# %%
ds['streamflow']

# %%

# flnm2 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake_0710-0720_1.1rough/*CHANOBS*'
# flnm2 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHANOBS*'
# flnm2 = '/home/fengx20/project/hydro/test3/RUN/grid_new_sta2/*CHANOBS*'
# ds2 = xr.open_mfdataset(flnm2)
# ds2.load()

#%%  观测数据
## 径流
csv = './渭河流域逐日径流.xlsx'
df = pd.read_excel(csv)
# df2 = df[df['站名'] == '临潼']
# df2 = df[df['站名'] == '张家山']
# df2 = df[df['站名'] == '状头']
# df2 = df[df['站名'] == '华县']
df2 = df[df['站名'] == '魏家堡']
df3 = df2[['时间','流量(立方米/秒)']]
xx = df3['时间'].values
xx = xx-pd.Timedelta('8H')
yy = df3['流量(立方米/秒)']

# 
## 降水
flnm3 = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
ds3 = xr.open_dataset(flnm3)
# %%


ds1.feature_id

# %%
da11 = ds1.isel(feature_id=0)['streamflow']
da12 = ds2.isel(feature_id=0)['streamflow']
lat = da11.latitude.values
lon = da11.longitude.values
print(lat, lon)
db = ds3['PRCP'].sel(lat=lat, method='nearest').sel(lon=lon, method='nearest')
# db = ds2['PRCP'].mean(dim=['lat', 'lon'])
ttt = pd.date_range('2022-07-14 00', '2022-07-18 00', freq='1H')
# ttt = pd.date_range('2022-07-14 00', '2022-07-20 00', freq='1H')
# labels = da11.sel(time=ttt).time.dt.strftime('%dT%H:00')
labels = da11.sel(time=ttt).time.values
# da11.time
# labels
x = labels
y = da11.sel(time=ttt).values
y22 = da12.sel(time=ttt).values
y1 = db.sel(time=ttt).values

cm = 1/2.54
fig = plt.figure(figsize=(12*cm, 8*cm), dpi=300)
ax = fig.add_axes([0.17, 0.25, 0.7, 0.65])
# ax.scatter(xx,yy,s=5, c='k', label='OBS')

ax2 = ax.twinx()
# # ax3 = ax.twinx()
# # ax.plot(x,y[1], label='streamflow', color='red', linestyle='--')
ax.plot(x,y, label='WRF-Hydro', color='red', linestyle='--')
# ax.plot(x,y22, label='100m', color='blue', linestyle='-.')
# # ax.scatter(xx,yy,s=5, c='k', label='OBS')
ax.plot(xx,yy, color='black', marker='o', label='OBS')
ax2.bar(x,y1, label='pre', color='black', linestyle='-', width=0.02)
ax.set_ylim(0, 4000)


# labels = da11.sel(time=ttt).time.dt.strftime('%dT%H').values
labels = da11.sel(time=ttt).time.dt.strftime('%d日%H时').values
# ax.set_xticks(labels[::24])
ax.set_xticklabels(labels[::12], rotation=30, fontsize=10)

# ax.set_title('魏家堡', loc='left',fontproperties=font)
fontdict={"family": "SimSun", "size": 10, "color": "k"}
# ax.set_title('魏家堡', loc='left',fontdict=fontdict)
# ax.set_title('华县', loc='left',fontdict=fontdict)
# ax.set_title('状头', loc='left',fontdict=fontdict)
ax.set_title('临潼', loc='left',fontdict=fontdict)
# ax.set_title(str(da11.latitude.values), loc='left')
# ax.set_title(str(da11.longitude.values), loc='right')
# ax.set_xticks(labels[::24].values)
# ax.set_xticklabels(labels.values[::24], rotation=30, fontsize=10)
ax.set_xlabel('Time')
ax.set_ylabel('Stream flow ($m^3\cdot s^{-1}$)')
ax2.set_ylabel('precipitation ($mm/h$)')
# ax.legend(edgecolor='white',loc='upper left')
# ax2.legend(edgecolor='white',bbox_to_anchor=(0.85,0.75))
# ax.legend(edgecolor='white',loc='upper right')
ax2.legend(edgecolor='white',bbox_to_anchor=(0.30,0.75))
ax.legend(edgecolor='white',loc='upper left')
# ax2.legend(edgecolor='white',bbox_to_anchor=(0.27,0.75))
figpath = '/home/fengx20/project/hydro/Draw/figure/'
fig.savefig(figpath+'状头.png')
# %%
csv = './渭河流域逐日径流.xlsx'
df = pd.read_excel(csv)
df2 = df[['站名','时间','流量(立方米/秒)']]
df2

# %%
sta_list = ['状头', '华县', '魏家堡', '临潼'] 
da_list = []
# ds = xr.Dataset()
for sta in sta_list:
    d1 = df2[df2['站名']==sta]
    da = xr.DataArray(
            name= str(d1['站名'].values[0]),
            data=d1['流量(立方米/秒)'].values,
            coords=[d1['时间'].values],
            dims=['time']
        )
    da_list.append(da)
ds = xr.merge(da_list)#
ds
# ds2 = ds.resample(time='1H').asfreq()
# ds3 = ds.resample(time='12H').interpolate('linear')
# ds3['状头']
#%%
da1 = ds['状头'].dropna(dim='time')
da2 = ds['华县'].dropna(dim='time')
da3 = ds['临潼'].dropna(dim='time')
da4 = ds['魏家堡'].dropna(dim='time')
da = ds['临潼']

cm = 1/2.54
fig = plt.figure(figsize=(8*cm,6*cm), dpi=300)
ax = fig.add_axes([0.15, 0.3, 0.75, 0.65])
# ax.scatter(da.time.values, da.values)
for sta in sta_list:
    da = ds[sta].dropna(dim='time')
    ax.plot(da.time.values, da.values, marker='o', label=sta)
    # ax.plot(da1.time.values, da1.values, marker='o')
    # ax.plot(xx,yy)
    # ax.plot(da2.time.values, da2.values, marker='o')
    # ax.plot(da3.time.values, da3.values, marker='o')
    # ax.plot(da4.time.values, da4.values, marker='o')
    # ax.scatter(da.time.values, da.values, marker='*')

xl = ax.get_xticklabels()
xt = ax.get_xticks()
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
# ax.legend()
# fontdict={"family": "TimesNewRoman", "size": 10, "color": "k"}
# ax.set_title('魏家堡', loc='left',fontdict=fontdict)
# ax.set_title('华县', loc='left',fontdict=fontdict)
# ax.set_title('状头', loc='left',fontdict=fontdict)
cl = ax.legend(edgecolor='white', fontsize=10)#,bbox_to_anchor=(0.85,0.75))
# cl.set
ax.set_xlabel('Time(Date Hour)')#, fontdict=fontdict)
# ax.set_ylabel('Streamflow')
ax.set_ylabel('Stream flow ($m^3\cdot s^{-1}$)')
# ax.set_xticks(xt, rotation=0, labels=xl)
# xl = ax.get_xticklabels()
fig.savefig('./figure/streamflow_obs.png')
# xl
#  %%
# ax.plot(xx,yy, color='black', marker='o', label='OBS')
# ds2.max()
# .resample.('D').asfreq()
# xr.concat(da_list, dim='time')
# %%
# ds
# d1['时间'].values
# )
# ds = xr.concat(da_list, dim='time')
# ds
da_list[0]
# %%
