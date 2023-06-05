# %%
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

# %%

# da_p2 = xr.open_dataarray('/home/fengx20/project/hydro/src/data/precip_2003.nc')
# da_p2
# %%
# dss
# dsp
# dso
# dsp.to_array().squeeze()
# dsp = dsp.rename({'__xarray_dataarray_variable__':'Wei Jiabao'})
# dsp
# %%
# # var = 'Wei Jiabao'
# var = 'Lin Jiacun'
# # var = 'Qin An'
# # var = 'Wu Shan'
# x = dss.time
# y_obs = dso[var]
# y_sim = dss[var]
# y_p = dsp[var]



# %%
def draw(x, y_obs, y_sim, y_p, var):
    cm = 1/2.54
    fig = plt.figure(figsize=(12*cm, 7*cm), dpi=300)
    ax = fig.add_axes([0.15, 0.3, 0.7, 0.6])


    ax_sub = ax.twinx()
    ax.plot(x, y_obs, lw=1., ls='-',color='gray', label='OBS')
    ax.plot(x, y_sim*1, lw=1., ls='--', color='red', label='SIM1')
    # ax.plot(x, y_sim2, lw=1., ls='-', color='orange', label='SIM2')
    ax_sub.bar(x, y_p, width=0.8, color='k', label='PRE')
    ax_sub.set_ylim(80, 0) # 右Y轴反转
    ax_sub.tick_params(axis='y', direction='in', length=5, width=0.7, colors='black', pad=6)

    if var in ['Wu Shan', 'Qin An']:
        ax.set_ylim(0, 300)
    elif var == 'Wei Jiabao':
        ax.set_ylim(0, 3000)
    elif var == 'Lin Jiacun':
        ax.set_ylim(0, 2000)
    # 获取每个月的第一天日期
    df = x.to_dataframe()
    monthly_ticks = df.resample('MS').first().index

    # 设置 x 轴刻度为每个月的第一天日期
    ax.set_xticks(monthly_ticks)
    ax.set_xticklabels(monthly_ticks.strftime('%Y-%m-%d'), rotation=30)

    ax.legend(loc='upper right', edgecolor='white')
    ax_sub.legend(bbox_to_anchor=(0.99, 0.75), edgecolor='white')



    ax.set_xlabel('Time (year-month-day)')
    ax.set_ylabel('Q $(m^3 \, s^{-1}$)')
    ax_sub.set_ylabel('P $(mm \, d^{-1})$')
    ax.set_title(var)


    plt.show()
    figpath = '/home/fengx20/project/hydro/figure/streamflow/'+'stream_'+var+'_2.png'
    fig.savefig(figpath)
# %%
# dss['Qin An'].plot()
if __name__ == "__main__":
    flnm_obs = '/home/fengx20/project/hydro/data/output/2010/'+'streamflow_obs.nc'
    flnm_sim = '/home/fengx20/project/hydro/src/data/frxst2.nc'
    # flnm_sim = '/home/fengx20/project/hydro/src/data/frxst_tucenghoudu.nc'
    flnm_p = '/home/fengx20/project/hydro/src/data/precip_areamean_2003.nc'

    t = pd.date_range('2003-07-02', '2003-10-31', freq='1d')
    dss =  xr.open_dataset(flnm_sim).sel(Time=t).rename({'Time':'time'})
    # dss1 =  xr.open_dataset(flnm_sim1).sel(Time=t).rename({'Time':'time'})
    # dss2 =  xr.open_dataset(flnm_sim2).sel(Time=t).rename({'Time':'time'})
    dso =  xr.open_dataset(flnm_obs).sel(Date=t).rename({'Date':'time'})
    dsp = xr.open_dataset(flnm_p).sel(time=t)

    var_list = ['Wei Jiabao', 'Lin Jiacun', 'Qin An', 'Wu Shan']
    # var = 'Wei Jiabao'
    for var in var_list:
        x = dss.time
        y_obs = dso[var]
        y_sim = dss[var]
        # y_sim1 = dss1[var]
        # y_sim2 = dss2[var]
        y_p = dsp[var]
        # draw(x, y_obs, )
        draw(x, y_obs, y_sim, y_p, var)