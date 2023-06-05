data_folder='./data/'
output_folder='./outputs/'
out_zip1=${output_folder}'ctl.zip'
in_geogrid=${data_folder}'geo_em.d01.nc'
lakes=${data_folder}'edm/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp'
csv=${data_folder}'sta.csv'
#in_dem=${data_folder}'edm/aster.tif'
in_dem=${data_folder}'edm/as_dem_3s.tif'
regrid_factor=4
routing_cells=400
over_rough_fac=1.0
retention_depth_fac=1.0



BRS='./wrfhydro_gis/Build_Routing_Stack.py'
# BRS='./wrf_hydro_gis_preprocessor/wrfhydro_gis/Build_Routing_Stack.py'
# BRS='/home/fengx20/project/hydro/test3/DATA/gis_100m/wrfhydro_gis/Build_Routing_Stack.py'

# echo lake
# python ${BRS} -i ${in_geogrid} --CSV ${csv} -d ${in_dem} -R ${regrid_factor} -t ${routing_cells} -O ${over_rough_fac} -T ${retention_depth_fac} -o ${out_zip1} -b True -l ${lakes}


echo nolake
python ${BRS} -i ${in_geogrid} --CSV ${csv} -d ${in_dem} -R ${regrid_factor} -t ${routing_cells} -O ${over_rough_fac} -T ${retention_depth_fac} -o ${out_zip1} -b True




# echo lake  # 包含水库文件，但是没有route.nc
# python ${BRS} -i ${in_geogrid} -l ${lakes} --CSV ${csv} -b True -d ${in_dem} -R ${regrid_factor} -t ${routing_cells} -o ${out_zip1}

#echo route  # 不包含水库文件，但是有route.nc
#python ${BRS} -i ${in_geogrid}  --CSV ${csv} -d ${in_dem} -r True -R ${regrid_factor} -t ${routing_cells} -o ${out_zip2}





# python Build_Routing_Stack.py -i {in_geogrid} -l {lakes} --CSV {csv} -d {in_dem} -R {regrid_factor} -t {routing_cells} -o {out_zip}

# python Build_Routing_Stack.py -i {in_geogrid} -l {lakes} --CSV {csv} -d {in_dem} -R {regrid_factor} -t {routing_cells} -o {out_zip}
# 
# 
# python Build_Routing_Stack.py -i ../data/geo_em.d01.nc -d ../data/edm/as_dem_3s.tif -r True -R 10 -t 20 -o ../outputs/tt1.zip


# python Build_Routing_Stack.py -i ../data/geo_em.d01.nc -l ../data/edm/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp --CSV ../data/sta.csv -d ../data/edm/as_dem_3s.tif -r True -R 10 -t 20 -o ../outputs/tt2.zip

