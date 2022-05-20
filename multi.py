#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:26:56 2022

@author: larissa
"""

#from prediction import estacoes_t
import os
import pandas as pd
from datetime import *
from functools import reduce
import numpy as np
from numpy import asarray
import cv2
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages


def as_grid25(dataMatrix, gridsize = 25, nmax = 1000):
    step = int(nmax/gridsize)
    sectors = np.arange(0,1000,step)
    coverageMatrix = np.zeros((25,25))
    
    #Creating the gridded map
    for i in range(0, len(sectors)):
        for j in range(0, len(sectors)):
            
            #analysing the original sectors and downsizing
            for x in range(sectors[i],sectors[i]+(step-1)):
                for y in range(sectors[j],sectors[j] + (step -1)):
                    #if there's a sample, cover the sector
                    if(dataMatrix[x][y] == 1):
                        coverageMatrix[i][j] = 1
    return coverageMatrix

def sectorize_coord():
    all_stations = np.zeros((1000,1000));
    all_stations[210][720] = 1 # X27 - PINHEIROS
    all_stations[210][850] = 1 # X47 - HORTO FLORESTAL
    all_stations[230][600] = 1 # X5 - IBIRAPUERA
    all_stations[230][810] = 1 # X2 - SANTANA
    all_stations[240][540] = 1 # X8 - CONGONHAS
    all_stations[250][430] = 1 # X1 - P. D. PEDRO II
    all_stations[250][480] = 1 # X16 - SANTO AMARO
    all_stations[300][780] = 1 # X12 - CENTRO
    all_stations[320][680] = 1 # X4 - CAMBUCI
    all_stations[360][720] = 1 # X3 - MOOCA

	# -----------------------------------------------
	# 1) Get 1000x1000 coords as 25x25 ordered by row (x-axis)
	# 2) Asserts (x,y) as (n,2) | Note.: which() returns table sorted by col (y-axis)
	# 3) Sorting back by row to keep consistence  
"""
	all_stations = as_grid25(all_stations) # 1
    #Talvez usar: all_stations[np.arange(condicional- all_stations == 1)]
	all_stations = which(all_stations == 1, arr.ind=TRUE) # 2
	all_stations = all_stations[order(all_stations[,1]),] # 3
	# -----------------------------------------------

	colnames(all_stations) <- c("x","y")

	# Include a last check to confirm if all stations coords are inside the map
"""
    return(all_stations)
            

def map_coords():
    img_path = os.path.join(os.path.expanduser('~'),'Documents','airPolution','spmap.png')
    img = cv2.imread(img_path,0);
    spmap = img / 255.0;
    
    coords = as_grid25(spmap)
    #(...more to come)
    
    return coords

