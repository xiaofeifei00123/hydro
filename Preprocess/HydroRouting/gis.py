import os
IN_NC = './data/geo_em.d01.nc'
wrfhydro_gis = '/home/fengx20/project/hydro/src/Preprocess/HydroRouting/wrfhydro_gis/'
outdir = './outputs/'

## 1. 创建研究区域的shp文件, 输入geo文件，输出.shp的一些文件
# os.system('python {}/Create_Domain_Boundary_Shapefile.py -i {} -o {}'.format(wrfhydro, IN_NC, outdir))




## 2. 创建LSMOUT的经纬度信息文件
REGRID_FACTOR = 10
OUT_NC = './outputs/latlon.nc'
# OUTPUT_FORMAT = 'LDASOUT' 
OUTPUT_FORMAT = 'RTOUT' 
os.system('python {}/Build_Spatial_Metadata_File.py -i {} -r {} -f {} -o {}'.format(wrfhydro_gis, IN_NC, REGRID_FACTOR, OUTPUT_FORMAT, OUT_NC))

