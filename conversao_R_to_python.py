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


#Algumas funcoes
def merger(x,y):
    merged = pd.merge(x, y, how="outer", on=["Data", "Hora"])
    return merged


#PM10 - por estacao
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
 
#O3 - por estacao
ibi_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/ibi_o3.csv'
mooca_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/mooca_o3.csv'
pdp_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/pdp_o3.csv'
pin_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/pin_o3.csv'
smp_o3 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/O3/smp_o3.csv'
 
#CO - por estacao
centro_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/centro_co.csv'
cong_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/cong_co.csv'
ibi_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/ibi_co.csv'
lapa_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/lapa_co.csv'
mooca_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/mooca_co.csv'
pdp_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/pdp_co.csv'
pin_co = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/CO/pin_co.csv'
 
#NO2 - por estacao
centro_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/centro_no2.csv'
cong_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/cong_no2.csv'
ibi_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/ibi_no2.csv'
pin_no2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/NO2/pin_no2.csv'
 
#SO2 - por estacao
cong_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/cong_so2.csv'
ibi_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/ibi_so2.csv'
pdp_so2 = 'C:/Users/dwlar/Desktop/Projetos/LACCAN/teste_saopaulo/dados/SO2/pdp_so2.csv'

#Lendo os arquivos csv - por estacao

#smp 
smp_pm = pd.read_csv(smp_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
smp_o3 = pd.read_csv(smp_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)


#camb
camb_pm = pd.read_csv(camb_pm ,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)


#centro
centro_pm  = pd.read_csv(centro_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
centro_co = pd.read_csv(centro_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
centro_no2  = pd.read_csv(centro_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#congonhas
cong_pm  = pd.read_csv(cong_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
cong_co = pd.read_csv(cong_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
cong_no2 = pd.read_csv(cong_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
cong_so2 = pd.read_csv(cong_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#ibiripuera
ibi_pm = pd.read_csv(ibi_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
ibi_o3 = pd.read_csv(ibi_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
ibi_co = pd.read_csv(ibi_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
ibi_no2 = pd.read_csv(ibi_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
ibi_so2 = pd.read_csv(ibi_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#lapa 
lapa_pm = pd.read_csv(lapa_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
lapa_co = pd.read_csv(lapa_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#mooca 
mooca_pm = pd.read_csv(mooca_pm,encoding='ISO-8859-1', sep = ';', parse_dates = [0], dayfirst = True)
mooca_o3 = pd.read_csv(mooca_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
mooca_co = pd.read_csv(mooca_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#pdp 
pdp_pm = pd.read_csv(pdp_pm,encoding='ISO-8859-1', sep = ';',parse_dates = [0], dayfirst = True)
pdp_o3 = pd.read_csv(pdp_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
pdp_co = pd.read_csv(pdp_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
pdp_so2 = pd.read_csv(pdp_so2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#pin 
pin_pm = pd.read_csv(pin_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
pin_o3 = pd.read_csv(pin_o3,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
pin_co = pd.read_csv(pin_co,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)
pin_no2 = pd.read_csv(pin_no2,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#samar 
samar_pm = pd.read_csv(samar_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)

#san 
san_pm = pd.read_csv(san_pm,encoding='ISO-8859-1', sep = ';', parse_dates=[0], dayfirst = True)


#Juntando dados
nt = [camb_pm, centro_pm, centro_co, centro_no2,
      cong_pm, cong_co, cong_no2, cong_so2,
      ibi_pm,ibi_o3, ibi_co, ibi_no2, ibi_so2, lapa_pm, lapa_co,
      mooca_pm, mooca_o3, mooca_co,pdp_pm,pdp_o3,pdp_co,pdp_so2,
      pin_pm,pin_o3,pin_co,pin_no2,samar_pm,san_pm]

estacoes = merger(smp_pm, smp_o3)

for i in nt:
    estacoes = merger(estacoes,i)

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
estacoes_t = pd.DataFrame(estacoes.iloc[6888:7056,:])
estacoes_t = estacoes_t.reset_index()
'''
ts = estacoes_t.loc[:,'63-PM10']
df = fix_na_1(ts)
df_col = fix_na_2(df)
'''
#Mesmo formando um novo dataframe, continua alterando o original
estacoes_2 = pd.DataFrame(estacoes_t)
for i in estacoes_t:
    if i == 'Data' or i == 'Hora':
        continue
    else:
        ts = estacoes_t.loc[:,i]
        df = fix_na_1(ts)
        df_col = fix_na_2(df)
        estacoes_2.loc[:,i] = df_col