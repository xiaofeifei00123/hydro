# %%
import xarray as xr
import numpy as np
# %%

flnm = '/home/fengx20/project/hydro/test_ground/RUN/200201010000.CHRTOUT_DOMAIN1'
ds = xr.open_dataset(flnm)
print(ds.latitude.values.max(), ds.latitude.values.min())
print(ds.longitude.values.max(), ds.longitude.values.min())

# %%
lon_list = [
    # 105.66667,
    # 105.68333,
    106.1256,
    # 107.05,
    107.75,
    # 104.883333,
]

lat_list = [
    # 34.9,
    # 34.583333,
    35.6216,
    # 34.3833,a
    34.3,
    # 34.73333,
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
    # flnm = '/home/fengx20/project/hydro/test3/RUN/Grid_nolake/202207140000.CHRTOUT_DOMAIN1'
    flnm = '/home/fengx20/project/hydro/test_ground/RUN/200201010000.CHRTOUT_DOMAIN1'
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