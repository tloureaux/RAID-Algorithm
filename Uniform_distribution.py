#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import segmentation
from sklearn.cluster import KMeans
from skimage import measure
import cv2 as cv
from shapely.geometry import Polygon
import rasterio.features
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import os

def mycontrolpointsunif(ncontrol_points,input_image,donnee):
    original_image = plt.imread(input_image)
    img = cv.imread(input_image,0)
    
    if img[0,0] > 128 :
        img = cv.bitwise_not(img)
        
    boundary = 100
    binary = np.where(img>boundary,True,False)
    
    contour = measure.find_contours(binary)[0]
    deja_fait = []
    for i in contour:
        deja_fait.append([i[1],i[0]])
        
    deja_faitx = [p[0] for p in deja_fait]
    deja_faity = [p[1] for p in deja_fait]
    
    #Find the uniform distribution of points
    tour = 0
    
    control_pointsx = [deja_faitx[tour]]
    control_pointsy = [deja_faity[tour]]
    
    for i in range(1,ncontrol_points):
        tour = i*(len(deja_faitx)//ncontrol_points)
        control_pointsx.append(deja_faitx[tour])
        control_pointsy.append(deja_faity[tour])
        
    sous_poly = Polygon(list(zip(control_pointsx,control_pointsy)))
    sous_mask = rasterio.features.rasterize([sous_poly], out_shape=(len(binary), len(binary[0])))
    
    black_pixels = (np.sum((binary==False)&(sous_mask==1)))
    white_pixels = (np.sum((binary==True)&(sous_mask==0)))
    errorblack = black_pixels
    errorwhite = white_pixels
    error = errorblack + errorwhite
        
    if donnee == 'image':
        plt.figure(figsize = (15,15))
        plt.imshow(original_image)
        plt.plot(control_pointsx, control_pointsy, 'ro',lw=8,markersize=12)
        plt.plot(np.append(control_pointsx,control_pointsx[0]), np.append(control_pointsy,control_pointsy[0]), 'r',linewidth = 5.0)
        plt.show()
        
    elif donnee == 'error':
        return(error)

