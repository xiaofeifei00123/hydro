# %%
import xarray as xr
import numpy as np
# %%



# flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.CHRTOUT_GRID1'
flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.GWOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/grid/DOMAIN/Fulldom_hires.nc'
flnm = '/home/fengx20/project/hydro/test3/RUN/grid/DOMAIN/geo_em.d01.nc'
flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140100.CHRTOUT_DOMAIN1'
flnm = '/home/fengx20/project/hydro/test3/RUN/route_01/202207140000.CHRTOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.GWOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test3/RUN/grid/DOMAIN/hydro2dtbl.nc'
# flnm = '/home/fengx20/project/hydro/test2/RUN/lake/201908010000.CHRTOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test2/RUN/route/201908010000.CHRTOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test_case/croto_ny/Gridded_no_lakes/201108260000.CHRTOUT_DOMAIN1'
# flnm = '/home/fengx20/project/hydro/test_case/croto_ny/Reach/201108260100.CHRTOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
ds
print(ds.latitude.values.max(), ds.latitude.values.min())
print(ds.longitude.values.max(), ds.longitude.values.min())
# %%

# %%
lon_list = [
    107.72644,
    109.20191,
    109.76097,
    # 105.6,
    109.839,
    108.13333,
]

lat_list = [
    34.289957,
    34.430699,
    34.582697,
    # 34.6333,
    35.005,
    35.000,
]

def get_nearest_latlon(lat0, lon0):
    # flnm = '/home/fengx20/project/hydro/test2/RUN/route/201908010000.CHANOBS_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test2/RUN/route/201908010000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/route/202207100000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/route_01/202207140000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/route_new_cmorph/202207100000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.CHRTOUT_GRID1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.CHRTOUT_GRID1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/grid/202207140000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test2/RUN/lake/201908010000.CHRTOUT_DOMAIN1'
    # flnm = '/home/fengx20/project/hydro/test3/RUN/grid_new_sta/202207140000.CHRTOUT_DOMAIN1'
    flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140000.CHRTOUT_DOMAIN1'
    # print('***'*10)
    # print(lat0, lon0)
    ds = xr.open_dataset(flnm)
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
    # print(da[idx].latitude.values)
    # print('***'*10)

# lat_list_new = []
# lon_list_new = []

for lat, lon in zip(lat_list, lon_list):
    # print(lat, lon)
    get_nearest_latlon(lat, lon)
    # lat_list_new.append(lat_n)
    # lon_list_new.append(lon_n)
# print(lon_list_new)
# %%
flnm1 = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/*CHANOBS*'
ds1 = xr.open_mfdataset(flnm1)
ds1.load()
# %%
import matplotlib.pyplot as plt
# for id in range(0,5):
id = 0
da = ds1['streamflow'].isel(feature_id=id)
print(da.longitude.values, da.latitude.values)
da.plot(label=id)
# plt.legend()

# %%
# ds