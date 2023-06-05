"""
根据观测的csv文件降水数据，合并保存各站点的降水数据
"""
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('/home/fengx20/mypy/baobao/my.mplstyle')
import calendar
import xarray as xr

#%%

def combine_streamflow_1sta(flnm):
    da_list = []
    df = pd.read_excel(flnm)
    df = df.rename(columns={'站名':'sta_name', '年份':'Year', '日期':'Date'})
    for y in range(2002, 2013):
        for m in range(1, 13):
            strtime = str(y)+'-'+str(m)#.zfill(2)

            days = calendar.monthrange(y, m)[1]
            df1 = df[df.Year==y]
            df2 = df1[['Date', m]]
            df3 = df2.dropna(axis=0,how='any')
            df3['Date'] = strtime+'-'+df3['Date'].astype('str')
            df3 = df3.head(days)
            df3['Date'] = pd.to_datetime(df3['Date'], format='%Y-%m-%d')
            df3.rename(columns={m:"streamflow"}, inplace=True)
            da_list.append(df3)
    df_return = pd.concat(da_list)
    df_return = df_return.set_index('Date')
    return df_return

def combine_streamflow_allsta():
    flnm_ws = '/home/fengx20/project/hydro/data/output/2010/2010渭河武山站逐日平均流量表.xls'
    flnm_ld = '/home/fengx20/project/hydro/data/output/2010/清流河隆德站逐日平均流量表.xls'
    flnm_ljc = '/home/fengx20/project/hydro/data/output/2010/渭河林家村（合)站逐日平均流量表.xls'
    flnm_wjb = '/home/fengx20/project/hydro/data/output/2010/渭河魏家堡站逐日平均流量表.xls'
    flnm_qa= '/home/fengx20/project/hydro/data/output/2010/葫芦河秦安站逐日平均流量表.xls'
    flnm_ts= '/home/fengx20/project/hydro/data/output/2010/藉河天水站逐日平均流量表.xls'
    sta_list = ['Wu Shan', 'Long De', 'Lin Jiacun', 'Wei Jiabao', 'Qin An', 'Tian Shui']
    station_name_list = ['武山', '隆德', '林家村', '魏家堡', '秦安', '天水']
    flnm_list = [flnm_ws, flnm_ld, flnm_ljc, flnm_wjb, flnm_qa, flnm_ts]
    da_list = []
    for i in range(len(sta_list)):
        print(sta_list[i])
        df = combine_streamflow_1sta(flnm_list[i])
        da1 = xr.DataArray(df.squeeze())
        da1.name = sta_list[i]
        da1.attrs['station_name'] = station_name_list[i]
        da_list.append(da1)
    ds = xr.merge(da_list)
    return ds


if __name__ == "__main__":
    ds = combine_streamflow_allsta()
    flnm_save = '/home/fengx20/project/hydro/data/output/2010/'+'streamflow_obs.nc'
    ds.to_netcdf(flnm_save)



# %%
### 以下是测试部分
def draw_test():
    flnm = '/home/fengx20/project/hydro/data/output/2010/'+'streamflow_obs.nc'
    ds =  xr.open_dataset(flnm)
    ds1 = ds.sel(Date='2003')

    for var in list(ds1.data_vars):
        da = ds1[var]
        name = da.attrs['station_name']
        da.plot(label=var)
    plt.legend(loc='upper left', edgecolor='white')
    plt.ylabel('Streamflow ($m^3s^{-1}$)')
    # %%
    # ds1['ts'].plot()

