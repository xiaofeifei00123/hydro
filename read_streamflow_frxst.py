# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
# %%
def get_runoff(flnm):
    """
    用于从frxst文件中，获取各站点的径流数据
    """
    columns = ["TimeFromStart", "Time", "station", "longitude", "latitude", "Runoff", "q_cfs", "stage"]
    df = pd.read_csv(flnm, sep=',', names=columns)
    df = df[['Time','station','Runoff']]
    df['Time'] = pd.to_datetime(df['Time'])

    grouped = df.groupby('station')
    station_list = list(grouped.groups.keys())
    station_list

    s_list = []
    for sta in station_list:
        df1 = grouped.get_group(sta)
        df1.set_index('Time', inplace=True)
        s = pd.Series(df1['Runoff'])
        s.name = sta
        s_list.append(s)
    dd = pd.concat(s_list, axis=1)
    return dd

def draw(df):
    # 创建图像和坐标轴对象
    cm = 1/2.54
    fig = plt.figure(figsize=(8*cm, 6*cm), dpi=300)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # 绘制图形，并设置 x 轴为每天的日期
    ax.plot(df.index, df[900], lw=0.5, color='red')
    ax.set_xlabel('Time')
    ax.set_ylabel('Runoff')
    ax.set_title('Daily Runoff with Monthly Labels')

    # 获取每个月的第一天日期
    monthly_ticks = df.resample('MS').first().index

    # 设置 x 轴刻度为每个月的第一天日期
    ax.set_xticks(monthly_ticks)
    ax.set_xticklabels(monthly_ticks.strftime('%Y-%m'), rotation=45)

    plt.show()

if __name__ == "__main__":
    # flnm = '/home/fengx20/project/hydro/data/output/frxst_pts_out.txt'
    flnm = '/home/fengx20/project/hydro/test_ground/RUN/frxst_pts_out.txt'
    flnm_obs_station = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/data/sta1.csv'
    df = get_runoff(flnm)
    df = df.loc[~df.index.duplicated(keep='first')]
    ds = xr.Dataset(df)

    df_os = pd.read_csv(flnm_obs_station, sep=',')
    # print(df_os)

    
    # df_os
    for var in list(ds.data_vars):
        # fid = int(41100000+var)
        fid = int(var)
        # ds[var].attrs['STATION'] = 
        # print(fid)
        ds[var].attrs['STATION'] = df_os[df_os['FID']==fid]['STATION'].values[0].strip()
        ds[var].attrs['Name'] = df_os[df_os['FID']==fid]['Name'].values[0].strip()
        ds[var].attrs['LON'] = df_os[df_os['FID']==fid]['LON'].values[0].round(4)
        ds[var].attrs['LAT'] = df_os[df_os['FID']==fid]['LAT'].values[0].round(4)
        ds = ds.rename({var:ds[var].attrs['STATION']})
    flnm_save = '/home/fengx20/project/hydro/src/data/frxst2.nc'
    ds.to_netcdf(flnm_save)    


    ### 筛选某个时间范围
    # start_date = pd.to_datetime('2003-02-02')
    # end_date = pd.to_datetime('2003-03-03')
    # filtered_df = df.loc[start_date:end_date]
    # df = filtered_df
    # %%
    # df[300].max()
    # draw(df)
    # %%

    # flnm_save = '/home/fengx20/project/hydro/src/data/frxst.nc'
    # ds = xr.open_dataset(flnm_save)
    # ds.sel(Time=slice('2003-07-01', '2003-09-01'))
    # # %%
    # # t = pd.date_range('2003-01-02', '2003-10-18', freq='1d')
    # # ds.Time.sel(Time=t)
    # # ds.Time
    # # t.shape
    # ds.Time