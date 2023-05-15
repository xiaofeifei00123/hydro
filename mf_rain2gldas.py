import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import xesmf as xe

def regrid_rain():
    flnm_gldas = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/input_files_old/GLDAS_NOAH025_3H.A20220710.0600.021.nc4'
    ds_gldas = xr.open_dataset(flnm_gldas)
    # ds_gldas.lat.values.round(3)
    # ds_out = xr.Dataset(
    #     {
    #         "lat": (["lat"], ds_gldas.lat.values, {"units": "degrees_north"}),
    #         "lon": (["lon"], ds_gldas.lon.values, {"units": "degrees_east"}),
    #     }
    # )
    ds_out = xe.util.grid_2d(70, 150, 0.25, 5, 60, 0.25)
    flnm_rain = '/home/fengx20/project/hydro/test3/DATA/rain/data/rain_obs.nc'
    ds_rain = xr.open_dataset(flnm_rain)
    ds = ds_rain
    regridder = xe.Regridder(ds, ds_out, "bilinear")
    # da = regridder(ds['PRCP'])
    ds2 = regridder(ds)

    path = '/home/fengx20/project/hydro/test3/DATA/forcingdata/GLDAS_PROCESS/regrid_rain/input_files_new/'
    for t in ds2.time:
        # ds1 = ds.sel(time=t, drop=False)
        # ds1 = ds.sel(time=t, drop=True)
        # ds2 = ds1.assign_coords
        ds1 = ds.sel(time=t).expand_dims('time')
        ft = str(t.dt.strftime('GLDAS_NOAH025_3H.A%Y%m%d.%H%M.021.nc4').values)
        print(ft)
        fs = os.path.join(path, ft)  # file_save
        ds1.to_netcdf(fs)

regrid_rain()