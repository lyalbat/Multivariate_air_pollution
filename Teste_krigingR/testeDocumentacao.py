#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:13:02 2022

@author: larissa
"""

#Teste de gstat - exemplo genérico - documentação

#Python tradicional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
#Importando pacotes necessarios para conversao R -> Python
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from rpy2.robjects.packages import gstat
from rpy2.robjects.conversion import localconverter'''

# These will let us use R packages:
from rpy2.robjects.packages import importr, data
from rpy2.robjects import pandas2ri

# Convert pandas.DataFrames to R dataframes automatically.
pandas2ri.activate()

sp = importr("sp")
gstat = importr("gstat")
meuse_df = pd.read_csv('/home/larissa/Documents/airPolution/Teste_krigingR/meuse.csv')

meuse_df['coordinates']  = "(" + meuse_df['x'].astype(str) + ","  + meuse_df['y'].astype(str) + ")"

#Transformacoes para cokriging:
    
meuse_df['ltom']  = np.log10(meuse_df['om'])
meuse_df['ltpb']  = np.log10(meuse_df['lead'])
meuse_df['ltzn']  = np.log10(meuse_df['zinc'])

'''
#Analisando correlacao entre target variable (om) e co-variable (pb)
print(meuse_df['ltom'].corr(meuse_df['ltpb']))

plt.scatter(meuse_df['ltom'] , meuse_df['ltpb'] )
plt.title('Feature-space relation between target (log10OM) and co-variable (log10Pb)')
plt.xlabel('log10(OM)')
plt.ylabel('log10(Pb)')
plt.show()

'''

#<- subset(as.data.frame(meuse), !is.na(om), c(x, y, om))

meuse_co = meuse_df[~meuse_df['om'].isnull()]
meuse_co = meuse_co[['om','x','y','ltom']]

'''

# convert to spatial object
coordinates(meuse.co) <- ~ x + y

# experimental variogram
v.ltom <- variogram(ltom ~ 1, meuse.co, cutoff=1800)
plot(v.ltom, pl=T)

# model by eye
m.ltom <- vgm(.035, "Sph", 800, .015)

# fit
(m.ltom.f <- fit.variogram(v.ltom, m.ltom))
plot(v.ltom, pl=T, model=m.ltom.f)

# compare variogram structure to target variable
m.ltom.f$range[2]; m.ltpb.f$range[2]

'''



