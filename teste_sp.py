# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 11:00:28 2021

@author: dwlar
"""
#Bibliotecas já testadas
import pandas as pd
import numpy as np
import datetime
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes
from shapely.geometry import Point, Polygon
plt.style.use('seaborn')
#Testando agora
import folium 
from scipy import stats 
from functools import reduce


#Algumas funcoes uteis
def merger(x,y):
    merged = pd.merge(x, y, how="outer", on=["Data", "Hora"])
    return merged
def converte_CO(x):
    for i in range(18,25):
        x.iloc[:,i] = [x.replace(',','.') if isinstance(n, str) else n for n in x.iloc[:,i]]
        x.iloc[:,i] = x.iloc[:,i].astype(float)
    return x

#PM10 - por estação
camb_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/camb_pm.csv'
centro_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/centro_pm.csv' 
cong_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/cong_pm.csv'
ibi_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/ibi_pm.csv'
lapa_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/lapa_pm.csv'
mooca_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/mooca_pm.csv'
pdp_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/pdp_pm.csv'
pin_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/pin_pm.csv'
samar_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/samar_pm.csv'
san_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/san_pm.csv'
smp_pm = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/PM10/smp_pm.csv'
 
#O3 - por estação
ibi_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/ibi_o3.csv'
mooca_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/mooca_o3.csv'
pdp_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/pdp_o3.csv'
pin_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/pin_o3.csv'
smp_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/smp_o3.csv'
 
#CO - por estação
centro_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/centro_co.csv'
cong_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/cong_co.csv'
ibi_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/ibi_co.csv'
lapa_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/lapa_co.csv'
mooca_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/mooca_co.csv'
pdp_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/pdp_co.csv'
pin_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/pin_co.csv'
 
#NO2 - por estação
centro_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/centro_no2.csv'
cong_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/cong_no2.csv'
ibi_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/ibi_no2.csv'
pin_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/pin_no2.csv'
 
#SO2 - por estação
cong_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/cong_so2.csv'
ibi_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/ibi_so2.csv'
pdp_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/pdp_so2.csv'

#Lendo os arquivos csv
camb_pm = pd.read_csv(camb_pm ,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
centro_pm  = pd.read_csv(centro_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
estacoes = merger(camb_pm,centro_pm)
cong_pm  = pd.read_csv(cong_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
estacoes = merger(estacoes,cong_pm)
ibi_pm = pd.read_csv(ibi_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
estacoes = merger(estacoes,ibi_pm)
lapa_pm = pd.read_csv(lapa_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
estacoes = merger(estacoes,lapa_pm)
mooca_pm = pd.read_csv(mooca_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
estacoes = merger(estacoes,mooca_pm)
pdp_pm = pd.read_csv(pdp_pm,encoding='ISO-8859-1', sep = ';',parse_dates = [0], dayfirst = True)
estacoes = merger(estacoes,pdp_pm)
pin_pm = pd.read_csv(pin_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pin_pm)
samar_pm = pd.read_csv(samar_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,samar_pm)
san_pm = pd.read_csv(san_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,san_pm)
smp_pm = pd.read_csv(smp_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,smp_pm)

ibi_o3 = pd.read_csv(ibi_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,ibi_o3)
mooca_o3 = pd.read_csv(mooca_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,mooca_o3)
pdp_o3 = pd.read_csv(pdp_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pdp_o3)
pin_o3 = pd.read_csv(pin_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pin_o3)
smp_o3 = pd.read_csv(smp_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,smp_o3)

centro_co = pd.read_csv(centro_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,centro_co)
cong_co = pd.read_csv(cong_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,cong_co)
ibi_co = pd.read_csv(ibi_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,ibi_co)
lapa_co = pd.read_csv(lapa_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,lapa_co)
mooca_co = pd.read_csv(mooca_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,mooca_co)
pdp_co = pd.read_csv(pdp_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pdp_co)
pin_co = pd.read_csv(pin_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pin_co)

centro_no2  = pd.read_csv(centro_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,centro_no2)
cong_no2 = pd.read_csv(cong_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,cong_no2)
ibi_no2 = pd.read_csv(ibi_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,ibi_no2) 
pin_no2 = pd.read_csv(pin_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pin_no2)

cong_so2 = pd.read_csv(cong_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True) 
estacoes = merger(estacoes,cong_so2)
ibi_so2 = pd.read_csv(ibi_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,ibi_so2)
pdp_so2 = pd.read_csv(pdp_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
estacoes = merger(estacoes,pdp_so2)

''''
#Separando os datasets em grupos
pm10 = [camb_pm,centro_pm,cong_pm,ibi_pm,lapa_pm,mooca_pm,pdp_pm,pin_pm,samar_pm,san_pm,smp_pm]
o3 = [ibi_o3,mooca_o3,pdp_o3,pin_o3,smp_o3]
co = [centro_co,cong_co,ibi_co,lapa_co,mooca_co,pdp_co,pin_co]
no2 = [centro_no2,cong_no2,ibi_no2,pin_no2]
so2 = [cong_so2,ibi_so2,pdp_so2]
estacoes = pm10 + o3 + co + no2 + so2
'''
#Formatando CO
#estacoes = converte_CO(estacoes)

estacoes["94-CO"] = [x.replace(',','.') if isinstance(x, str) else x for x in estacoes["94-CO"]]
estacoes["94-CO"] = estacoes["94-CO"].astype(float)

estacoes['73-CO'] =  [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['73-CO']]
estacoes['73-CO']= estacoes['73-CO'].astype(float)

estacoes['83-CO'] =  [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['83-CO']]
estacoes['83-CO'] = estacoes['83-CO'].astype(float)

estacoes['84-CO'] =  [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['84-CO']]
estacoes['84-CO'] = estacoes['84-CO'].astype(float)

estacoes['85-CO'] =  [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['85-CO']]
estacoes['85-CO'] = estacoes['85-CO'].astype(float)

estacoes['72-CO'] = [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['72-CO'] ]
estacoes['72-CO'] = estacoes['72-CO'].astype(float)

estacoes['99-CO'] =  [x.replace(',','.') if isinstance(x, str) else x for x in estacoes['99-CO']]
estacoes['99-CO'] = estacoes['99-CO'].astype(float)

#Testando a imputacao de valores faltantes por predicao usando valores de regressao linear
'''
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
testdf = estacoes[estacoes.isnull()== True]
traindf = estacoes[estacoes.isnull()== False]
y = traindf['73-SO2']
traindf.drop(["73-SO2",'Data','Hora'],axis=1,inplace=True)
lr.fit(traindf,y)
testdf.drop("73-SO2",axis=1,inplace=True)
pred = lr.predict(testdf)
testdf['73-SO2']= pred
'''
'''
from sklearn.impute import SimpleImputer
imputer = SimpleImputer()
val = estacoes.drop(['Data','Hora'])
transformed_values = imputer.fit_transform(estacoes)

'''