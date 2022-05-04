#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 10:45:47 2022

@author: larissa
"""

import os
import pandas as pd
from datetime import *
from functools import reduce
import numpy as np


#Importing the paths for Congonhas station

cong_pm = os.path.join(os.path.expanduser('~'),'Documents', 'airPolution','dados','PM10','cong_pm.csv')
cong_co = os.path.join(os.path.expanduser('~'),'Documents', 'airPolution','dados','CO','cong_co.csv')
cong_no2 = os.path.join(os.path.expanduser('~'),'Documents', 'airPolution','dados','NO2','cong_no2.csv')
cong_so2 = os.path.join(os.path.expanduser('~'),'Documents', 'airPolution','dados','SO2','cong_so2.csv')

#Reading the Congonhas files with pandas

cong_pm  = pd.read_csv(cong_pm,encoding='ISO-8859-1', sep = ',', parse_dates = {'date': ['Data','Hora']}, dayfirst = True)
cong_co = pd.read_csv(cong_co,encoding='ISO-8859-1', sep = ',', parse_dates = {'date': ['Data','Hora']}, dayfirst = True)
cong_no2 = pd.read_csv(cong_no2,encoding='ISO-8859-1', sep = ',', parse_dates = {'date': ['Data','Hora']}, dayfirst = True)
cong_so2 = pd.read_csv(cong_so2,encoding='ISO-8859-1', sep = ',', parse_dates = {'date': ['Data','Hora']}, dayfirst = True)

#Fixing CO
for co in range(len(cong_co) -1):
    cong_co['73-CO'][co] = cong_co['73-CO'][co] + ((cong_co['Unnamed: 3'][co])/10)

cong_co = cong_co.drop('Unnamed: 3',axis = 1)


#Turning multiple dataframes into one

 
df_temp = [cong_pm, cong_co,cong_no2,cong_so2]

for df in df_temp:
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y %H:%M")

stations = reduce(lambda left,right: pd.merge(left,right, on=['date'],
                                              how = 'outer'),df_temp)


#Filling missing values in the station columns 

def fix_na_1(df_col):
    h_matrix = pd.DataFrame()
    hours = 24
    #Mudei de 25 para 24 - 04/02/2022
    for i in range(24):    
        s = list(range(i, len(df_col),hours))
        h = df_col.loc[s]
        h = h.reset_index(drop = True)
        h_matrix = h_matrix.append(h)
    return h_matrix

def fix_na_2(df):
    for i in range(0,len(df)):
        for j in range(0,len(df.columns)):
            if(np.isnan(df.iloc[i,j])):
                #Check if the column and row are empty
                na_row = np.isnan(df.iloc[i,:].std())
                na_col = np.isnan(df.iloc[:,j].std())
                
                if (na_row and na_col):
                    print('Blank row and column. Could not predict')
                    break
                
                # Estimate a random sample based on row (hour) mean/sd
                elif(~na_row):
                    m1 = df.iloc[i,:].mean()
                    sd1 = df.iloc[i,:].std()
                    row_norm = round(np.random.normal(m1,sd1),2)
                    
                    # Avoid negative samples
                    while(row_norm <0):
                        row_norm = round(np.random.normal(m1,sd1),2)
                    df.iloc[i,j] = row_norm
                    
                elif(~na_col):
                    m2 = df.iloc[:,j].mean()
                    sd2 = df.iloc[:,j].std()
                    col_norm = round(np.random.normal(m2,sd2),2)
                    
                    # Avoid negative samples
                    while(col_norm <0):
                        col_norm = round(np.random.normal(m2,sd2),2)
                    df.iloc[i,j] = col_norm
                
                else:
                    m1 = df.iloc[i,:].mean()
                    m2 = df.iloc[:,j].mean()
                    sd1 = df.iloc[i,:].std() 
                    sd2 = df.iloc[:,j].std()
                    norm = abs(round(np.random.normal([m1,m2],[sd1,sd2]),2))
                    while(norm < 0):
                        norm = abs(round(np.random.normal([m1,m2],[sd1,sd2]),2))
                    df.iloc[i,j] = norm
    y = []
    for i in range(0,len(df.columns)):
        x = df.iloc[:,i]
        x = x.to_list()
        y.append(x)
    df_col = [item for sublist in y for item in sublist]
    return df_col

estacoes_t = stations.copy(deep = True)
estacoes_t = pd.DataFrame(estacoes_t.iloc[6888:7056,:])
estacoes_t = estacoes_t.reset_index()

for i in stations:
    if i == 'date':
        continue
    else:
        ts = estacoes_t.loc[:,i]
        df = fix_na_1(ts)
        df_col = fix_na_2(df)
        estacoes_t.loc[:,i] = df_col