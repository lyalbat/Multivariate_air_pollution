#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:03:50 2022

@author: larissa
"""
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects import pandas2ri
#Must be activated
pandas2ri.activate()


import numpy as np
y = np.zeros((10,10))
def as_grid25(dataMatrix, gridsize=5, nmax=10):
  step = int(nmax/gridsize)
  sectors = np.arange(0,10,step)
  coverageMatrix = np.zeros((5,5))
  for i in range(len(sectors)):
	  for j in range(len(sectors)):
		  #Sweeping on each sector
		  for x in range(int(sectors[i]),int(sectors[i])+(step-1)): 
			  for y in range(int(sectors[i]),int(sectors[i])+(step-1)):  
				  if(dataMatrix[x][y] == 1):
					  coverageMatrix[i][j] = 1
            
  return(coverageMatrix)


all_stations = as_grid25(y)
print(y)
'''
print(all_stations == 1)

all_stations <- which(all_stations == 1, arr.ind=TRUE) # 2

all_stations <- all_stations[order(all_stations[,1]),] # 3
colnames(all_stations) <- c("x","y")

print(all_stations)
'''