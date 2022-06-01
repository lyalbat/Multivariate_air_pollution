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

    all_stations = as_grid25(all_stations) # 1
    rows, cols = np.where(all_stations == 1)
    all_stations = np.vstack((rows, cols)).T
    return(all_stations)
            

def map_coords():
    img_path = os.path.join(os.path.expanduser('~'),'Documents','airPolution','spmap.png')
    img = cv2.imread(img_path,0);
    spmap = img / 255.0;
    
    coords = as_grid25(spmap).astype(int)
    coords = np.where((coords==0)|(coords==1), (coords)^1, coords)
    #print(coords)
    
    return coords

sp_coords = map_coords()
#No original as coordenadas sao convertidas em um csv...talvez fazer
#write.csv(sp_coords, "../environment/spcoords_25x25.csv", row.names=FALSE)

station_coord = sectorize_coord()

station_id = [["X1"],["X2"],["X3"],["X4"],["X5"],["X8"],["X12"],["X16"],["X27"],["X47"]]

var_name = [["CO"],["PM10"], ["O3"], ["NO2"], ["SO2"]]

station_id_coord = np.append(station_coord, station_id, axis = 1)

#df_cols = np.append(var_name, station_id, axis = 1)

df_cols = np.array(np.meshgrid(station_id,var_name)).T
