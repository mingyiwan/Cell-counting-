import os
import roifile
from roifile import ImagejRoi,roiwrite
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from zipfile import ZipFile
import numpy as np
import matplotlib.pyplot as plt

#RUN FUNCTION_1 to convert ROI files into polygons
def roi2polygons(channel_name):
    lis=[]
    for i in range(0,len(channel_name)):
        poly=Polygon(channel_name[i].coordinates())
        lis.append(poly)
    return lis

#RUN FUNCTION2 colocalization of channels and nuclei
#This function will return three things:a list of all the nuclei kept, a list of all the nuceli deleted, a list of the areas of puncta area in each nuclei
def count_colocal (nuclei_poly,channel_poly, puncta_thresh, area_thresh):
    min_count=puncta_thresh
    min_cluster_area=area_thresh 
    nu_C=[]
    nu_C_deleted=[]
    area=[] 
    for poly in nuclei_poly:
        inside=[sp for sp in channel_poly if sp.intersects(poly)]
        n_inside=len(inside)
        cluster = unary_union(inside) if inside else None #prevent overcounting of the overlapped
        cluster_area=cluster.area if cluster else 0.0
        area.append(cluster_area)
        if (n_inside >= min_count) or (cluster_area >= min_cluster_area):
            nu_C.append(poly)
        else: 
            nu_C_deleted.append(poly)
                    
    return nu_C, nu_C_deleted, area

#RUN Function3 turn polygons into ROI zip files
def write_ROI(POLY_list, name_of_file):
    roi_list_nu_C =[]
    name=name_of_file
    for idx, poly in enumerate (POLY_list):
        coords=np.asarray(poly.exterior.coords, dtype=float)
        roi=ImagejRoi.frompoints(coords.tolist())
        roi_list_nu_C.append(roi)
    roiwrite(f'{name}.zip', roi_list_nu_C,mode='w')