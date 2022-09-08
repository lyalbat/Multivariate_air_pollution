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

#Importando pacotes necessarios para conversao R -> Python
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

#from rpy2.robjects.packages import gstat
#from rpy2.robjects.conversion import localconverter

#Importando os dados já completos de prediction

#from prediction import estacoes_t as airpol
#airpol.to_csv(r'/home/larissa/Documents/airPolution\airpol.csv', index=False)
airpol = pd.read_csv('/home/larissa/Documents/airPolution/airpol.csv')


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
                    if(dataMatrix[x,y] == 1):
                        coverageMatrix[i,j] = 1
    return coverageMatrix

def sectorize_coord():
    all_stations = np.zeros((1000,1000));
    all_stations[240][540] = 1 # X73 - CONGONHAS
    all_stations[300][780] = 1 # X94 - CENTRO
    all_stations[320][680] = 1 # X90 - CAMBUCI
    all_stations[230][600] = 1 # X83 - IBIRAPUERA
    all_stations[360][720] = 1 # X85 - MOOCA
    all_stations[250][430] = 1 # X72 - P. D. PEDRO II
    all_stations[210][720] = 1 # X99 - PINHEIROS
    all_stations[230][810] = 1 # X63 - SANTANA
    all_stations[250][480] = 1 # X64 - SANTO AMARO
    
    all_stations = as_grid25(all_stations) # 1
    rows, cols = np.where(all_stations == 1)
    all_stations = np.vstack((rows, cols)).T
    #Talvez usar: all_stations[np.arange(condicional- all_stations == 1)]
	#all_stations = all_stations[order(all_stations[,1]),] # 3
    
    return(all_stations)


def map_coords():
    img_path = os.path.join(os.path.expanduser('~'),'Documents','airPolution','spmap.png')
    img = cv2.imread(img_path,0);
    spmap = img / 255.0;
    
    coords = as_grid25(spmap).astype(int)
    coords = np.where((coords==0)|(coords==1), (coords)^1, coords)
    #print(coords)
    
    return coords

def combination(station_id, var_name):
    df_cols = np.array(np.meshgrid(station_id,var_name)).T
    
    df_cols = np.concatenate((df_cols[0],df_cols[2],df_cols[4],df_cols[7],df_cols[8]),axis=0)
    
    df_cols = np.delete(df_cols,np.where(df_cols[:,1] == 'SO2') ,axis=0)
    df_cols = np.delete(df_cols,np.where(df_cols[:,1] == 'NO2') ,axis=0)
    df_cols = pd.DataFrame(data = df_cols,columns = ['Var2', 'Var1'])
    return df_cols


def snapshot_series(station_coords, st_airpol_nafix, var_name, station_id):
    PM10,CO,O3 = [],[],[]
    station_id_CO_PM10_03 = ["83","85","72","99"]
    var_name_CO_PM10_O3 = ["CO", "PM10", "O3"]
    
    #Ainda nao sei se vai ser util, mas adicionei
    to_predict = []
    
    for row in airpol:
      station, pol = row.split('-')
      if(station in station_id_CO_PM10_03 and pol in var_name_CO_PM10_O3):
        if(pol == "CO"):
          CO.append(airpol[row])
        elif(pol == "PM10"):
          PM10.append(airpol[row])
        else:
          O3.append(airpol[row])
      else:
        to_predict.append(airpol.pop(row))
    
        PM10,CO,O3 = np.array(PM10),np.array(CO), np.array(O3)
        new_PM10,new_CO,new_O3 = [], [], []
        
        for row2 in range(len(CO[0])):
          new_CO.append(CO[:,row2])
        new_CO = np.vstack(new_CO)
        
        for row2 in range(len(PM10[0])):
          new_PM10.append(PM10[:,row2])
        new_PM10 = np.vstack(new_PM10)
        
        for row2 in range(len(O3[0])):
          new_O3.append(O3[:,row2])
        new_O3 = np.vstack(new_O3)
        
        return snapshot
            
                

#Alterar o predict

def predict_series (snapshot_series, var_names, coords):
    timeserie_map = list()
    matern = None
    for i in range(len(snapshot_series)):
        airpol_snapshot = snapshot_series[[i]]
        airpol.g = None
        
        if("CO" in var_names):
            airpol.g = gstat(id="CO",
                             formula = ro.r('''log(unlist(airpol_snapshot$CO)) ~ 1'''),
                             data = airpol_snapshot,
                             nmax = 10)
            
        if("PM10" in var_names):
            airpol.g = gstat(id="PM10",
                             formula = ro.r('''log(unlist(airpol_snapshot$CO)) ~ 1'''),
                             data = airpol_snapshot,
                             nmax = 10)
            
        if("O3" in var_names):
            airpol.g = gstat(id="O3",
                             formula = ro.r('''log(unlist(airpol_snapshot$CO)) ~ 1'''),
                             data = airpol_snapshot,
                             nmax = 10)
            
        if("NO2" in var_names):
            airpol.g = gstat(id="NO2",
                             formula = ro.r('''log(unlist(airpol_snapshot$CO)) ~ 1'''),
                             data = airpol_snapshot,
                             nmax = 10)
        if("SO2" in var_names):
            airpol.g = gstat(id="SO2",
                             formula = ro.r('''log(unlist(airpol_snapshot$CO)) ~ 1'''),
                             data = airpol_snapshot,
                             nmax = 10)

		#matern=vgm(0.1, "Mat", 3, kappa=0.5)
        print(airpol.g)

		#if(is.element("NO2", var_names))
        matern=ro.r('''vgm(5, "Mat", 3, kappa=0.5)''')
        airpol.g = ro.r('''gstat(airpol.g, model=matern, fill.all=T)''')
        v = ro.r('''variogram(airpol.g,50)''')
        ro.r('''airpol.fit <- fit.lmc(v, airpol.g, model=matern, 
						  fit.ranges=FALSE, 
						  correct.diagonal=1.01)

		plot(v, model=airpol.fit)
        ''')

		# Running reconstruction and storing output at "info"
        '''
		info = capture.output(
			timestamp_map_rebuilt = predict(airpol.fit, newdata = coords)
		)

		timeserie_map[[i]] <- timestamp_map_rebuilt 

		# Formatting console output
		ic <- info[1] # string log for Intrinsic Correlation
		method <- substr(info[2], 8, 25) # string log formatted for cokriging

		# Progress
		progress = ceiling(100*i/length(snapshot_series))
		cat('\r',format(paste0(ic, " ", method, ": ", progress, "% ")))
		flush.console()'''
        print("\nDone!")
        return(timeserie_map)


sp_coords = map_coords()
#No original as coordenadas sao convertidas em um csv...talvez fazer
#write.csv(sp_coords, "../environment/spcoords_25x25.csv", row.names=FALSE)

station_coord = sectorize_coord()
#tation_coord['coordinates'] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)

station_id = [["73-"],["94-"],["90-"],["83-"],["85-"],["72-"],["99-"],["63-"],["64-"]]
var_name = [["CO"],["PM10"], ["O3"], ["NO2"], ["SO2"]]

station_id_coord = np.append(station_id,station_coord, axis = 1)

df_cols = combination(station_id, var_name)

#PREDICTION - FIRST STEP
var_name_CO_PM10_O3 = ["CO", "MP10", "O3"]
station_id_CO_PM10_03 = ["83-","85-","72-","99-"]

CO_PM10_03_coords = pd.DataFrame(station_id_coord, columns = ['station_id', 'x','y']).drop([0,1,2,7,8]).reset_index()
CO_PM10_03_coords['coordinates'] = CO_PM10_03_coords.apply(lambda x: [x['x'], x['y']], axis=1)
airpol_1st_pred = airpol.copy()
CO,PM10,O3 = [],[],[]

for key in airpol_1st_pred.columns:
    if(key == 'date'):
        pass
    else:
        if(key[:3] in station_id_CO_PM10_03):
            if(key[3:] == "CO"):
                #coords = CO_PM10_03_coords[CO_PM10_03_coords['station_id']==key[:3]]['coordinates'].values[0]
                CO.append(airpol_1st_pred[key])
            elif(key[3:] == "PM10"):
                #coords = CO_PM10_03_coords[CO_PM10_03_coords['station_id']==key[:3]]['coordinates'].values[0]
                PM10.append(airpol_1st_pred[key])
            elif(key[3:] == "O3"):
                #coords = CO_PM10_03_coords[CO_PM10_03_coords['station_id']==key[:3]]['coordinates'].values[0]
                O3.append(airpol_1st_pred[key])
            else:
                pass
        else:
            airpol_1st_pred = airpol_1st_pred.drop(columns=[key])
            
dic_test= {'Coordinates':CO_PM10_03_coords['coordinates'],'CO': CO, 'PM10': PM10, 'O3': O3}
dic_test = pd.DataFrame(dic_test)

#CO_PM10_03_snapshot_series = snapshot_series(CO_PM10_03_coords,airpol,var_name_CO_PM10_O3,station_id_CO_PM10_03)
#CO_PM10_03_reconst = predict_series(CO_PM10_03_snapshot_series,var_name_CO_PM10_O3,sp_coords)


