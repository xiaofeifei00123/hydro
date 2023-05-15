
# %%
# flnm = '/home/fengx20/mm/test/1_wrfout_d01_2014-07-11_12:00:00.mean'

flnm = '/home/fengx20/mm/test0_psot/fg'
flnm1 = '/home/fengx20/mm/test0_psot/wrfvar_output_t0'
flnm2 = '/home/fengx20/mm/test0_psot/wrfvar_output_t25'
flnm3 = '/home/fengx20/mm/test0_psot/wrfvar_output_t50'
flnm4 = '/home/fengx20/mm/test0_psot/wrfvar_output_t75'
flnm5 = '/home/fengx20/mm/test0_psot/wrfvar_output_t100'
# flnm = '/home/fengx20/mm/test/wrfout_d02_2014-07-11_12:00:00'
ds = xr.open_dataset(flnm)
ds
# %%
# ds.T.min()
fn = nc.Dataset(flnm)
fn1 = nc.Dataset(flnm1)
fn2 = nc.Dataset(flnm2)
fn3 = nc.Dataset(flnm3)
fn4 = nc.Dataset(flnm4)
fn5 = nc.Dataset(flnm5)
t = wrf.getvar(fn,'temp')
t1 = wrf.getvar(fn1,'temp')
t2 = wrf.getvar(fn2,'temp')
t3 = wrf.getvar(fn3,'temp')
t4 = wrf.getvar(fn4,'temp')
t5 = wrf.getvar(fn5,'temp')
# t2.min()
# %%
da = (t5-t)[17,:,:]
da
lat = da.XLAT.values
lon = da.XLONG.values
# (t1-t)[17,:,:].plot()
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