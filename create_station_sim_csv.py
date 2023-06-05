"""
因为有时候指定的预报格点不在模式的河道格点上，
所以需要选择离预测格点最近的河道格点位置，作为河道格点在模式中的位置，
这样才会输出预报格点的径流等变量，所以本程序需要以下文件：
1. 预测的站点位置信息，这个是原始的真实的观测  sta.csv
2. 模式运行一个时间步长得到的CHAROUT_DOMAIN文件
"""
# %%
import xarray as xr
import numpy as np
import pandas as pd
# %%
def get_nearest_latlon(lon0, lat0, flnm_CHRTOUT):
    # flnm = '/home/fengx20/project/hydro/test_ground/RUN/200207010000.CHRTOUT_DOMAIN1'
    ds = xr.open_dataset(flnm_CHRTOUT)
    da = ds['streamflow']
    lat1 = ds['streamflow'].latitude.values
    lon1 = ds['streamflow'].longitude.values
    ### 寻找离站点最接近的辐合条件的点
    arr = ((lat1-lat0)**2+(lon1-lon0)**2)#.argmin()
    # np.sort(arr)
    idx = np.argsort(arr)
    # idx = ((lat1-lat0)**2+(lon1-lon0)**2)#.argmin()
    # return da[idx].latitude.values, da[idx].longitude.values
    print('**start**')
    print(da[idx[0]].longitude.values,',', da[idx[0]].latitude.values)
    print(da[idx[1]].longitude.values,',', da[idx[1]].latitude.values)
    print(da[idx[2]].longitude.values,',', da[idx[2]].latitude.values)
    print('**end**')
    return da[idx[0]].longitude.values, da[idx[0]].latitude.values



def test1():
    lon_list = [
        105.66667,
        105.68333,
        106.1256,
        107.05,
        107.75,
        104.883333,
        ]

    lat_list = [
        34.9,
        34.583333,
        35.6216,
        34.3833,
        34.3,
        34.73333,
    ]


    flnm_CHRTOUT = '/home/fengx20/project/hydro/test_ground/RUN/2005/200501010000.CHRTOUT_DOMAIN1'
    for lat, lon in zip(lat_list, lon_list):
        get_nearest_latlon(lon, lat, flnm_CHRTOUT)
if __name__ == "__main__":

    flnm_CHRTOUT = '/home/fengx20/project/hydro/test_ground/RUN/2005/200501020000.CHRTOUT_DOMAIN1'
    ds = xr.open_dataset(flnm_CHRTOUT)

    ### 需要测量的站点, 原始的经纬度信息
    # csv_path = '/home/fengx20/project/hydro/src/data/sta.csv'
    csv_path = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/data/sta_station.csv'
    df = pd.read_csv(csv_path)
    print(df)
    df2 = df.copy(deep=True)
    for i in range(df.shape[0]):
        # print(i)
        lat = df.iloc[i].loc['LAT']
        lon = df.iloc[i].loc['LON']
        lon1, lat1 = get_nearest_latlon(lon, lat, flnm_CHRTOUT)
        df2.iloc[i].loc['LAT'] = lat1
        df2.iloc[i].loc['LON'] = lon1
        # print(lon1)
        # print(lat, lon)
    # print(df)
    # %%
    # df2-df
    df2
    # lat
    # lat1
    # df2
    # ds
    # df
    # lon1
    # df2