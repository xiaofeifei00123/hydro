# %%
import pandas as pd
import pypinyin
# %%
flnm_csv = '/home/fengx20/project/hydro/Draw/station_latlon.csv'
df = pd.read_csv(flnm_csv)
# col = ['code', 'lat', 'lon', 'name']
col = ['code', 'lon', 'lat', 'name']
df1 = df[col]
df2 = df1.rename(index=str, columns={'code':'FID', 'lat':'LAT', 'lon':'LON', 'name':'Name'})
df2
# for i in df2['name']:
#     print('叠加%s站点'%i.strip())
#     df3 = df2[df2.name.str.contains(i)]
#     lon = df3['lon'].values[0]
#     lat = df3['lat'].values[0]
#     sta_name = df3['name'].values[0].strip()
#     print(lon, lat, sta_name)
# %%
# df2
df3 = df2.set_index('FID')
sta_list = []
for i in df3['Name']:
    result  = pypinyin.pinyin (i,style=pypinyin.NORMAL)
    result_ = [i[0] for i in result]
    result2 = result_[0].capitalize() + ' ' + ''.join(result_[1:]).capitalize()
    sta_list.append(result2)
df3['STATION'] = sta_list
col = ['LON', 'LAT', 'STATION', 'Name']
df4 = df3[col]
# %%
# df4

sta_list = [
    # '罗李村',
    # '马渡王',
    # '秦渡',
    # '黑峪口',
    '秦安',
    '天水',
    # '柳林',
    # '涝峪口',
    # '耀县',
    '隆德',
    # '北道',
    '华县',
    '林家村',
    '魏家堡',
    '武山',
    # '咸阳',
    # '淳化',
]
idx_list = []
for i in sta_list:
    ddf = df4[df4.Name.str.contains(i)]
    idx = ddf.index.values[0]
    idx_list.append(idx)
idx_list
df5 = df4.loc[idx_list]
# df4[df4['STATION'].isin(['Hua Xian', 'Zhuang tou'])]
csv_path = '/home/fengx20/project/hydro/Draw/sta.csv'
df5.to_csv(csv_path)