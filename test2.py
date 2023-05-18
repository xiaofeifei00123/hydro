# %%
import xarray as xr
import numpy as np
import scipy 
import pyinterp
import pyinterp.backends.xarray
from scipy.interpolate import RegularGridInterpolator
import cmaps
# %%
import math as m
freq = 1000
t = np.arange(1000) / freq
t = t[:, None] + t
t_data = (np.sin(t * m.tau) / 0.1 + np.sin(2 * t * m.tau) / 0.2 +
          np.sin(5 * t * m.tau) / 0.5 + np.sin(10 * t * m.tau) +
          np.sin(20 * t * m.tau) / 2 + np.sin(50 * t * m.tau) / 5 +
          np.sin(100 * t * m.tau) / 10)
t_data
# %%
t_data.shape

# %%
# flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_DATA_1h/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
flnm = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_new/GLDAS_NOAH025_3H.A20220710.0000.021.nc4'
ds = xr.open_dataset(flnm)
ds
# %%
flnm2 = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/output_files/2022071001.LDASIN_DOMAIN1'
ds2 = xr.open_dataset(flnm2)
ds2
# %%
string = 'https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi?FILENAME=%2Fdata%2FGLDAS%2FGLDAS_NOAH025_3H.2.1%2F2002%2F001%2FGLDAS_NOAH025_3H.A20020101.0600.021.nc4&VARIABLES=LWdown_f_tavg%2CPsurf_f_inst%2CQair_f_inst%2CRainf_tavg%2CSWdown_f_tavg%2CTair_f_inst%2CWind_f_inst&SHORTNAME=GLDAS_NOAH025_3H&BBOX=20%2C85%2C50%2C120&DATASET_VERSION=2.1&SERVICE=L34RS_LDAS&FORMAT=bmM0Lw&LABEL=GLDAS_NOAH025_3H.A20020101.0600.021.nc4.SUB.nc4&VERSION=1.02'
string = 'https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi?FILENAME=%2Fdata%2FGLDAS%2FGLDAS_NOAH025_3H.2.1%2F2013%2F001%2FGLDAS_NOAH025_3H.A20130101.1800.021.nc4&VERSION=1.02&LABEL=GLDAS_NOAH025_3H.A20130101.1800.021.nc4.SUB.nc4&DATASET_VERSION=2.1&SHORTNAME=GLDAS_NOAH025_3H&SERVICE=L34RS_LDAS&BBOX=20%2C85%2C50%2C120&VARIABLES=LWdown_f_tavg%2CPsurf_f_inst%2CQair_f_inst%2CRainf_tavg%2CSWdown_f_tavg%2CTair_f_inst%2CWind_f_inst&FORMAT=nc4%2F'

# string.split('GLDAS')
# %%
import re
# re.search('GLDAS_NOAH025_3H.A\d{8}.\d{4}', string).group()
str_time = re.search('\d{8}.\d{4}', string).group()

# %%
"""
# %%
降水的强迫
### forcing rain
flnm_forcing = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/FORCING/202207141200.PRECIP_FORCING.nc'
dsf = xr.open_dataset(flnm_forcing)
dsf['precip'].max()   # mm/h
dd = dsf['precip'].squeeze()
# plt.contourf(lon[::10,::10],lat[::10,::10],dd*3600, levels=[0,10,20, 30, 40, 50, 100, 200])
plt.contourf(lon[::10,::10],lat[::10,::10],dd, levels=10, extend='max')
plt.colorbar()
# dd.max()
# dd.plot()
# dd.max()
# %%
### real rain
flnm = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
ds = xr.open_dataset(flnm)
da = ds['PRCP'].sel(time='2022-07-15 12')
dc = da.sel(lat=slice(34,39)).sel(lon=slice(104,110))
dc.plot()
# plt.contourf(x,y,dc, )
# %%

# %%

flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.LDASOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
# ds
# ds['UGDRNOFF'].plot()
# ds['ACCET'].plot()  # 蒸发
# ds['ACCECAN'].plot()  # 树冠水
# ds['ACCEDIR'].plot()  # 土壤蒸发
# ds['ACCETRAN'].plot()  # 蒸腾
# ds['TRAD']

# ds['SFCRNOFF'].plot()
da = ds['QRAIN']*3600
da.plot()
# %%
"""
## 将db插值到da的格点上
def regrid_coarse2fine(da, db):
    """
    da: 需要输出的较粗的网格分辨率的数据, xr.DataArray (y:417,x:582)
    db: 输入的精细网格分辨率的数据,xr.DataArray (y:4170,x:5820)
    return :
        dc: 同da网格
    """
    data = db.values
    y = db.y.values
    x = db.x.values
    ## 输入的格点
    interp = RegularGridInterpolator((y, x), data,
                                    bounds_error=False, fill_value=None)
    ## 输出的格点
    Y,X = np.meshgrid(da.y.values, da.x.values, indexing='ij')
    ## 插值
    ii = interp((Y,X))
    # dc = xr.DataArray(ii)
    dc = xr.DataArray(
        ii,
        coords=da.coords,
        dims= da.dims,
    )
    return dc
# %%
flnm_LSM = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.LSMOUT_DOMAIN1'
ds_LSM = xr.open_dataset(flnm_LSM)
da = ds_LSM['sfcheadrt'].squeeze()
# %%
flnm_RT = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207141200.RTOUT_DOMAIN1'
ds_RT= xr.open_dataset(flnm_RT)
db = ds_RT['sfcheadsubrt'].squeeze()
# db
# %%
dc = regrid_coarse2fine(da, db)
dc
# %%
flnm = '/'