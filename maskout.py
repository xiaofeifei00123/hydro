#coding=utf-8
'''
##############################################################################
#   This module enable you to maskout the unneccessary data outside          #
#            the interest region on a matplotlib-plotted output.             #
#   You can use this script for free                                         #
##############################################################################
#     INPUT:                                                                 # 
#           'fig'      :  the map                                            #
#           'ax'       :  the Axes instance                                  # 
#           'shpfile'  :  the border file                                    #
#                             outside the region the data is to be maskout   #
#           'clabel': clabel instance  (optional)                            #
#           'vcplot': vector map       (optional)                            #   
#     OUTPUT:                                                                #
#           'clip'            :the masked-out map.                           #
##############################################################################
'''
import shapefile
import cartopy.crs as ccrs
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon as ShapelyPolygon
from collections import Iterable
def shp2clip(fig,ax,region_shpfile, proj=None,clabel=None,vcplot=None):
    sf = shapefile.Reader(region_shpfile)
    for shape_rec in sf.shapeRecords():
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                if proj:
                    vertices.append(proj.transform_point(pts[j][0], pts[j][1], ccrs.Geodetic()))
                else:
                    vertices.append((pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)

    if vcplot:
        if isinstance(fig,Iterable):
            for ivec in fig:
                ivec.set_clip_path(clip)
        else:
            fig.set_clip_path(clip)
    else:
        for contour in fig.collections:
            contour.set_clip_path(clip)

    if  clabel:
        clip_map_shapely = ShapelyPolygon(vertices)
        for text_object in clabel:
            if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
                text_object.set_visible(False)    

    return clip
