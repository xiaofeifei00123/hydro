"""
根据原始的水文站点经纬度数据文件
创建模式预报站点需要的csv文件
原始的真实地理位置的csv文件
"""
# %%
import pandas as pd
import pypinyin
## TODO 根据 Fulldomain_hires.nc文件，对经纬度进行校正
# %%
# flnm_csv = '/home/fengx20/project/hydro/Draw/station_latlon.csv'
flnm_csv = '/home/fengx20/project/hydro/src/data/station_latlon.csv'
df = pd.read_csv(flnm_csv)

## 获取需要的列
col = ['code', 'lon', 'lat', 'name']
df1 = df[col]
df2 = df1.rename(index=str, columns={'code':'FID', 'lat':'LAT', 'lon':'LON', 'name':'Name'})
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

## 几个站点
sta_list = [
    # '罗李村',
    # '马渡王',
    # '秦渡',
    # '黑峪口',
    '秦安',
    # '天水',
    # '柳林',
    # '涝峪口',
    # '耀县',
    # '隆德',
    # '北道',
    # '华县',
    '林家村',
    '魏家堡',
    '武山',
    # '咸阳',
    # '淳化',
]

### 筛选出需要的站点的数据
idx_list = []
for i in sta_list:
    ddf = df4[df4.Name.str.contains(i)]
    idx = ddf.index.values[0]
    idx_list.append(idx)
idx_list
df5 = df4.loc[idx_list]
# df4[df4['STATION'].isin(['Hua Xian', 'Zhuang tou'])]

### 保存数据
csv_path = '/home/fengx20/project/hydro/test_ground/Hydro_Routing/data/sta_station.csv'
df5.to_csv(csv_path)
