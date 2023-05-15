# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('/home/fengx20/mypy/baobao/my.mplstyle')

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
del df['sta_name']
del df['Date']
df = df.groupby(['Year']).mean()
df2 = df.mean(axis=1)
df2
x1 = df1.index
y1 = df1
x2 = df2.index
y2 = df2
#%%
# df1.index
# df2
df
# %%
cm = 1/2.54
fig = plt.figure(figsize=(4, 3), dpi=300)
ax = fig.add_axes([0.25, 0.2, 0.7, 0.7])
x1 = df1.index
y1 = df1
x2 = df2.index
y2 = df2
ax.plot(x1, y1)
ax.plot(x2, y2)
ax.tick_params(which='major',length=8,width=1.0) # 控制标签大小 
ax.tick_params(which='minor',length=4,width=0.5)  #,colors='b')
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_ylabel('径流量 $(m^3/s)$')
ax.set_xlabel('Year')
ax.set_xticks(np.arange(1970, 2015, 10))
ax.set_xticklabels(np.arange(1970, 2015, 10))
figpath_year = '/home/fengx20/project/hydro/Draw/figure/'+'year_streamflow.png'
fig.savefig(figpath_year)
# %%
# df1
# df2
flnm1 = '/home/fengx20/project/hydro/data/output/1980武山站逐日平均流量表.xls'
df1 = pd.read_excel(flnm1)
del df1['Date']
col = ['Year','Jun', 'Jul', 'Aug']
# df1[col].
df1 = df1[col]
# df1
df1 = df1.groupby(['Year']).mean()
df1 = df1.mean(axis=1)
df1
# df1
flnm2 = '/home/fengx20/project/hydro/data/output/2010渭河武山站逐日平均流量表.xls'
df = pd.read_excel(flnm2)
df = df.rename(columns={'站名':'sta_name', '年份':'Year', '日期':'Date'})
del df['sta_name']
del df['Date']
col = ['Year',6,7, 8]
df = df[col]
df = df.groupby(['Year']).mean()
df2 = df.mean(axis=1)
df2
x3 = df1.index
y3 = df1
x4 = df2.index
y4 = df2
# %%
cm = 1/2.54
fig = plt.figure(figsize=(4, 2), dpi=300)
ax = fig.add_axes([0.25, 0.2, 0.7, 0.7])
x3 = df1.index
y3 = df1
x4 = df2.index
y4 = df2
ax.plot(x1, y1, color='k', label='year')
ax.plot(x2, y2, c='k')
ax.plot(x3, y3, c='blue', linestyle='-', label='summer')
ax.plot(x4, y4, c='blue', )


ax.legend(edgecolor='white')

ax.tick_params(which='major',length=8,width=1.0) # 控制标签大小 
ax.tick_params(which='minor',length=4,width=0.5)  #,colors='b')
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_ylabel('径流量 $(m^3/s)$')
ax.set_xlabel('Year')
ax.set_xticks(np.arange(1970, 2015, 10))
ax.set_xticklabels(np.arange(1970, 2015, 10))
figpath_year = '/home/fengx20/project/hydro/Draw/figure/'+'year_streamflow.png'
fig.savefig(figpath_year)
# %%