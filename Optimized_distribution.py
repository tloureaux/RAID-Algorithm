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

def mycontrolpointsopti(ncontrol_points,input_image,donnee):
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
    ncontrol = 2
    tour = 0
    
    control_pointsx = [deja_faitx[tour]]
    control_pointsy = [deja_faity[tour]]
    
    for i in range(1,ncontrol):
        tour = i*(len(deja_faitx)//ncontrol)
        control_pointsx.append(deja_faitx[tour])
        control_pointsy.append(deja_faity[tour])
        
    #Affinement du séquençage
    
    while (ncontrol != ncontrol_points):
        ncontrol = ncontrol + 1
        
        black_pixels = []
        white_pixels = []
        
        all_pointsx = np.append(control_pointsx,control_pointsx[0])
        all_pointsy = np.append(control_pointsy,control_pointsy[0])
        
        for i in range(0,len(all_pointsx)-1):
            point_1 = [all_pointsx[i],all_pointsy[i]]
            point_2 = [all_pointsx[i+1],all_pointsy[i+1]]
            
            if deja_fait.index(point_1) < (deja_fait.index(point_2)+1):
                sous_liste = deja_fait[deja_fait.index(point_1):deja_fait.index(point_2)+1]
                
            else:
                fin = deja_fait[0:(deja_fait.index(point_2)+1)]
                debut = deja_fait[deja_fait.index(point_1):len(deja_fait)-2]
                debut.extend(fin)
                sous_liste = debut
                
            sous_listex = [p[0] for p in sous_liste]
            sous_listey = [p[1] for p in sous_liste]
            
            sous_poly = Polygon(list(zip(sous_listex,sous_listey)))
            sous_mask = rasterio.features.rasterize([sous_poly], out_shape=(len(binary), len(binary[0])))
            
            black_pixels.append(np.sum((binary==False)&(sous_mask==1)))
            white_pixels.append(np.sum((binary==True)&(sous_mask==1)))
            
        black_pixels = black_pixels/np.sum(black_pixels)
        white_pixels = white_pixels/np.sum(white_pixels)
        black_irr = [i for i,v in enumerate(black_pixels) if v == max(black_pixels)]
        white_irr = [i for i,v in enumerate(white_pixels) if v == max(white_pixels)]
            
        if not (black_irr == [] and white_irr == []):
                
            if max(max(black_pixels),max(white_pixels))==max(black_pixels):
                p1 = [all_pointsx[black_irr[0]],all_pointsy[black_irr[0]]]
                p2 = [all_pointsx[black_irr[0]+1],all_pointsy[black_irr[0]+1]]
                    
            else:
                p1 = [all_pointsx[white_irr[0]],all_pointsy[white_irr[0]]]
                p2 = [all_pointsx[white_irr[0]+1],all_pointsy[white_irr[0]+1]]
                    
            if deja_fait.index(p1) < (deja_fait.index(p2)+1):
                sous_liste = deja_fait[deja_fait.index(p1):deja_fait.index(p2)+1]
                    
            else:
                fin = deja_fait[0:(deja_fait.index(p2)+1)]
                debut = deja_fait[deja_fait.index(p1):len(deja_fait)-2]
                debut.extend(fin)
                sous_liste = debut
                    
            distdroite = []
                
            if p1[0] == p2[0]:
                    
                for j in range(0,len(sous_liste)-1):
                    truedist = (sous_liste[j][0]-p1[0])**2
                    distdroite.append(truedist)
                    
            elif p1[1] == p2[1]:
                    
                for j in range(0,len(sous_liste)-1):
                    truedist = (sous_liste[j][1]-p1[1])**2
                    distdroite.append(truedist)
                        
            else:
                adroite = (p2[1]-p1[1])/(p2[0]-p1[0])
                bdroite = p1[1]-adroite*p1[0]
                    
                for j in range(0,len(sous_liste)-1):
                    xdroite = (sous_liste[j][1]-bdroite)/adroite
                    ydroite = adroite*sous_liste[j][0]+bdroite
                    truedist = min((sous_liste[j][1]-ydroite)**2,(sous_liste[j][0]-xdroite)**2)
                    distdroite.append(truedist)
                        
            ncontrol_point = sous_liste[distdroite.index(np.amax(distdroite))]
                
            list_x = [i for i in range(0,len(control_pointsx)) if control_pointsx[i]==p1[0]]
            list_y = [i for i in range(0,len(control_pointsy)) if control_pointsy[i]==p1[1]]
            common = [element for element in list_x if element in list_y]
                
        control_pointsx.insert(common[0]+1,ncontrol_point[0])
        control_pointsy.insert(common[0]+1,ncontrol_point[1])
        
    poly_test = Polygon(list(zip(control_pointsx,control_pointsy)))
    mask_test = rasterio.features.rasterize([poly_test], out_shape=(len(binary), len(binary[0])))
        
    nblack_pixels = (np.sum((binary==False)&(mask_test==1)))
    nwhite_pixels = (np.sum((binary==True)&(mask_test==0)))
    error = nblack_pixels+nwhite_pixels
        
    if donnee == 'image':
        plt.figure(figsize = (15,15))
        plt.imshow(original_image)
        plt.plot(control_pointsx, control_pointsy, 'ro',lw=8,markersize=12)
        plt.plot(np.append(control_pointsx,control_pointsx[0]), np.append(control_pointsy,control_pointsy[0]), 'r',linewidth = 3.0)
        plt.xticks([])
        plt.yticks([])
        plt.show()
        
    elif donnee == 'error':
        return(error)

