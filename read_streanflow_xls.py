# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('/home/fengx20/mypy/baobao/my.mplstyle')
import calendar
import xarray as xr

#%%

flnm1 = '/home/fengx20/project/hydro/data/output/1980武山站逐日平均流量表.xls'
df1 = pd.read_excel(flnm1)
del df1['Date']
df1 = df1.groupby(['Year']).mean()
df1 = df1.mean(axis=1)
df1
# %%
# df1
flnm2 = '/home/fengx20/project/hydro/data/output/2010渭河武山站逐日平均流量表.xls'
df = pd.read_excel(flnm2)
df = df.rename(columns={'站名':'sta_name', '年份':'Year', '日期':'Date'})
df
# %%
df2 = df[df.Year==2002]
# %%
df2
# %%
# df2[1]
def combine_streamflow(flnm):
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

def combine_streamflow():
    flnm_ws = '/home/fengx20/project/hydro/data/output/2010/2010渭河武山站逐日平均流量表.xls'
    flnm_ld = '/home/fengx20/project/hydro/data/output/2010/清流河隆德站逐日平均流量表.xls'
    flnm_ljc = '/home/fengx20/project/hydro/data/output/2010/渭河林家村（合)站逐日平均流量表.xls'
    flnm_wjb = '/home/fengx20/project/hydro/data/output/2010/渭河魏家堡站逐日平均流量表.xls'
    flnm_qa= '/home/fengx20/project/hydro/data/output/2010/葫芦河秦安站逐日平均流量表.xls'
    flnm_ts= '/home/fengx20/project/hydro/data/output/2010/藉河天水站逐日平均流量表.xls'
    # df = combine_streamflow(flnm)
    sta_list = ['ws', 'ld', 'ljc', 'wjb', 'qa', 'ts']
    station_name_list = ['武山', '隆德', '林家村', '魏家堡', '秦安', '天水']
    flnm_list = [flnm_ws, flnm_ld, flnm_ljc, flnm_wjb, flnm_qa, flnm_ts]
    # df.plot()
    da_list = []
    for i in range(len(sta_list)):
        print(sta_list[i])
        df = combine_streamflow(flnm_list[i])
        da1 = xr.DataArray(df.squeeze())
        da1.name = sta_list[i]
        da1.attrs['station_name'] = station_name_list[i]
        da_list.append(da1)
        # da1
    ds = xr.merge(da_list)
    return ds

# %%
if __name__ == "__main__":
    ds = combine_streamflow()
    flnm_save = '/home/fengx20/project/hydro/data/output/2010/'+'streamflow_obs.nc'
    ds.to_netcdf(flnm_save)





# %%
### 以下是测试部分
flnm= '/home/fengx20/project/hydro/data/output/2010/'+'streamflow_obs.nc'
ds =  xr.open_dataset(flnm)
ds
#%%
# ds = ds.sel()
ds1 = ds.sel(Date='2003')
# ds1 = ds
ds1
# ds1
#%%
# fig = plt.figure(figsize=(4,3), dpi=300)
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for var in list(ds1.data_vars):
    da = ds1[var]
    name = da.attrs['station_name']
    da.plot(label=var)
plt.legend(loc='upper left', edgecolor='white')
plt.ylabel('Streamflow ($m^3s^{-1}$)')
# %%
# ds1['ts'].plot()

#%%
# ds1['ws'].plot()
flnm = '/home/fengx20/project/hydro/test_ground/RUN/FORCING/200207010900.PRECIP_FORCING.nc'
ds = xr.open_dataset(flnm)
da = ds['precip_rate']*3600
da.max()
#%%
# da.plot()
db.sel(feature_id=2900).plot()
# %%
ds1 = ds.sel(Date='2003-09')
# %%
ds1['wjb'].plot()

# %%
db.sel(feature_id=3500).plot()
# %%
ds1['ld'].plot()
# %%
# db.sel(feature_id=600).plot()
# ds1 = ds1.sel(time)
# ds1['wjb'].plot()
# %%
# dc = db.sel(feature_id=900)[280:]#.plot()
# ds1['wjb'].plot()
# dc.plot()
# %%

tt=pd.date_range('2003-01-01', '2003-12-31', freq='1d')
# %%
fig = plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# ax.plot(tt, y900.values)
# ax.plot(tt, y2)
# ax.plot(y2)
# ticks = pd.date_range('2023-01-01', '2023-12-31', freq='1d')
# ax.set_xticks(ticks, rotation=30)
# ax.set_xticklabels(ticks.strftime('%m'), rotation=0)


# %%
# ds1['ts'].plot()
# y900 = db.sel(feature_id=900)
y900
# %%
# y900
# ds1['ld'].plot()
y2 = ds.sel(Date='2003')['wjb']
y2
# ds1['wjb'].shape
# ds1['ljc'].plot()
# ds1['qa'].plot()
# plt.legend()
# plt.ylim(0, 100)
# %%
# y2.plot()
# y2.Date.dt.strftime('%m%d')
# ds1['wjb']
db.sel(feature_id=900).plot()
db.sel(feature_id=300).plot()
db.sel(feature_id=600).plot()
plt.title('')
