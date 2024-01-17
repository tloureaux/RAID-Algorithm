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

def comparison(ncontrol_points,input_image):
    graphunif = []
    graphopti = []
    for i in range(3,ncontrol_points+1):
        errorunif = mycontrolpointsunif(i,input_image,'error')
        erroropti = mycontrolpointsopti0(i,input_image,'error')
        graphunif.append(errorunif)
        graphopti.append(erroropti)
    plt.figure(figsize=(15,15))
    #plt.axvspan(10, 15, facecolor='lawngreen', alpha=0.5)
    plt.plot(np.linspace(3,ncontrol_points,ncontrol_points-2),graphunif,'r',label='uniform distribution')
    plt.plot(np.linspace(3,ncontrol_points,ncontrol_points-2),graphopti,'b',label='optimized distribution')
    plt.legend(loc=2,prop={'size': 20})
    plt.xticks(range(0,ncontrol_points,5))
    plt.show()

