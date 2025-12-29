import os
import pandas as pd
import roifile
from roifile import ImagejRoi,roiwrite
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from zipfile import ZipFile
import numpy as np
import matplotlib.pyplot as plt
from Functions import *

#dataframes
oprk1_count=[]
crh_count=[]
fos_count=[]
oprk1_crh_count=[]
oprk1_fos_count=[]
crh_fos_count=[]
all_count=[]
dapi_count=[]
animal=[]


#read directory
Master_folder=r"C:\Users\mingy\OneDrive\Desktop\RNAscope cell count\whola\new batch";
sub_folder=os.listdir(Master_folder)
list_folder=[]
for i in range (len(sub_folder)):
    folder=sub_folder[i]
    dir=os.path.join(Master_folder,folder)
    list_folder.append(dir)

#start looping through each individual brain file
for k in range (len(list_folder)):
    folder=list_folder[k]
    files=os.listdir(folder)
    nu=os.path.join(folder,files[4])
    c1=os.path.join(folder,files[1])
    c2=os.path.join(folder,files[2])
    c3=os.path.join(folder,files[3])

    #RUN read files in the folder
    nuclei=roifile.roiread(nu)
    oprk1=roifile.roiread(c1)
    crh=roifile.roiread(c2)
    fos=roifile.roiread(c3)

    #RUN turn roi into polygons 
    nuclei_mask=roi2polygons(nuclei)
    oprk1_mask=roi2polygons(oprk1)
    crh_mask=roi2polygons(crh)
    fos_mask=roi2polygons(fos)

    #RUN counting how many cell is positive for certain single channel
    #you can change the area threshold by changing the last number
    nu_oprk1,nu_oprk1_deleted,area_oprk1=count_colocal(nuclei_mask, oprk1_mask,3,109.05)
    nu_crh,nu_crh_deleted,area_crh=count_colocal(nuclei_mask, crh_mask,3,66.45)
    nu_fos,nu_fos_deleted,area_fos=count_colocal(nuclei_mask, fos_mask,3,89.1)

    #RUN counting how many cell is positive for any combination of two channels 
    #oprk1_crh
    oprk1_crh,oprk1_crh_deleted,area_oc=count_colocal(nu_oprk1,crh_mask,3,66.45)
    #oprk1_fos
    oprk1_fos,oprk1_fos_deleted,area_of=count_colocal(nu_oprk1,fos_mask,3,89.1)
    #crh_fos
    crh_fos,crh_fos_deleted,area_cf=count_colocal(nu_crh,fos_mask,3,89.1)

    #RUN counting how many cell is positive for all three channels 
    oprk1_crh,_,_=count_colocal(nu_oprk1,crh_mask,3,66.45)
    oprk1_crh_fos,oprk1_crh_fos_deleted,area_all=count_colocal(oprk1_crh,fos_mask,3,89.1)
  
    #write ROI files
    imagename=os.path.join(folder,files[0])
    file_name=os.path.basename(imagename)
    write_ROI(nu_oprk1,file_name+"_nu_oprk1")
    write_ROI(nu_oprk1_deleted,file_name+"_nu_oprk1_deleted")
    write_ROI(nu_crh,file_name+"_nu_crh")
    write_ROI(nu_crh_deleted,file_name+"_nu_crh_deleted")
    write_ROI(nu_fos,file_name+"_nu_fos")
    write_ROI(nu_fos_deleted,file_name+"_nu_fos_deleted")

    write_ROI(oprk1_crh,file_name+"_oprk1_crh")
    write_ROI(oprk1_crh_deleted,file_name+"_oprk1_crh_deleted")
    write_ROI(oprk1_fos,file_name+"_oprk1_fos")
    write_ROI(oprk1_fos_deleted,file_name+"_oprk1_fos_deleted")
    write_ROI(crh_fos,file_name+"_crh_fos")
    write_ROI(crh_fos_deleted,file_name+"_crh_fos_deleted")

    write_ROI(oprk1_crh_fos,file_name+"_oprk1_crh_fos")
    write_ROI(oprk1_crh_fos_deleted,file_name+"_oprk1_crh_fos_deleted")


    #append data to data frame
    count_oprk1_pos=str(len(nu_oprk1))
    count_crh_pos=str(len(nu_crh))
    count_fos_pos=str(len(nu_fos))
    count_oprk1_crh=str(len(oprk1_crh))
    count_oprk1_fos=str(len(oprk1_fos))
    count_crh_fos=str(len(crh_fos))
    count_all=str(len(oprk1_crh_fos))
    animalid=file_name

    oprk1_count.append(count_oprk1_pos)
    crh_count.append(count_crh_pos)
    fos_count.append(count_fos_pos)
    oprk1_crh_count.append(count_oprk1_crh)
    oprk1_fos_count.append(count_oprk1_fos)
    crh_fos_count.append(count_crh_fos)
    all_count.append(count_all)
    dapi_count.append(str(len(nuclei_mask)))
    animal.append(animalid)

#creat pandas dataframe
data_frame={
    "animal_ID": animal,
    "oprk1":oprk1_count,
    "crh":crh_count,
    "fos": fos_count,
    "oprk1 and crh":oprk1_crh_count,
    "oprk1 and fos":oprk1_fos_count,
    "crh and fos": crh_fos_count,
    "all channels": all_count,
    "total number of cell":dapi_count
}

df=pd.DataFrame(data_frame)
filepath=os.path.join(Master_folder,"batch3.csv")
df.to_csv(filepath)

