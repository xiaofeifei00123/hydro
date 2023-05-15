# %%
import xarray as xr
import os
# %%


def mf_gldas():
    print('读取文件')
def read_combine_ds(fl):
    fl_list = os.popen('ls {}'.format(fl)) # 打开一个管道
    fl_list = fl_list.read().split()
    ds_list = []
    for flnm in fl_list:
        print(flnm.split('/')[-1])
        ds = xr.open_dataset(flnm)
        ds2 = ds.drop_vars('time_bnds')
        ds_list.append(ds2)
    print("合并文件")
    ds_concat = xr.concat(ds_list, dim='time')
    print("合并文件结束")
    return ds_concat

fl = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_DATA/*.nc4'
ds = read_combine_ds(fl)
# ds = xr.open_mfdataset(fl, concat_dim='time', combine='nested')
# ds = ds.load()
print('加载文件结束，开始重采样')
ds2 = ds.resample(time='H').interpolate('linear')
print('重采样结束')

print('开始保存文件')
def save_file_hourly(ds):
    path = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_DATA_1h/'
    for t in ds.time:
        # ds1 = ds.sel(time=t, drop=False)
        # ds1 = ds.sel(time=t, drop=True)
        # ds2 = ds1.assign_coords
        ds1 = ds.sel(time=t).expand_dims('time')
        ft = str(t.dt.strftime('GLDAS_NOAH025_3H.A%Y%m%d.%H%M.021.nc4').values)
        print(ft)
        fs = os.path.join(path, ft)  # file_save
        ds1.to_netcdf(fs)
save_file_hourly(ds2)
