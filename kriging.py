#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Teste python -> R


#Importando pacotes necessarios para conversao R -> Python

import rpy2
import rpy2.robjects as robjects

from rpy2.robjects.packages import importr, data


r_base = importr('base') 
r_utils = importr('utils')


r_utils.chooseCRANmirror(ind=1)
r_utils.install_packages('gstat')

gstat = importr('gstat')

#1st step of prediction

from multi import CO_PM10_03_snapshot_series, var_name_CO_PM10_O3, sp_coords


def predict_series (snapshot_series, var_names, city_coords):
    timeserie_map = robjects.r('timeserie_map <- list()')
    robjects.r('matern <- NULL')
    
    for i in range(len(snapshot_series)):
        airpol_snapshot = snapshot_series[i]
        airpol_snapshot = robjects.r('airpol_snapshot')
        robjects.r('airpol.g <- NULL')
        
        if("CO" in var_names):
           robjects.r('airpol.g <- gstat(id="CO", formula= log(unlist(airpol_snapshot$CO)) ~ 1, data=airpol_snapshot, nmax = 10)')
            
        if("PM10" in var_names):
            robjects.r('airpol.g <- gstat(airpol.g, "PM10", log(unlist(airpol_snapshot$PM10))~1,data=airpol_snapshot, nmax = 10)')
            
        if("O3" in var_names):
            robjects.r('airpol.g <- gstat(airpol.g, "O3", log(unlist(airpol_snapshot$O3))~1,data=airpol_snapshot, nmax = 10)')
            
        if("NO2" in var_names):
            robjects.r('airpol.g <- gstat(airpol.g, "NO2", log(unlist(airpol_snapshot$NO2))~1,data=airpol_snapshot, nmax = 10)')
            
        if("SO2" in var_names):
            robjects.r('airpol.g <- gstat(airpol.g, "SO2", log(unlist(airpol_snapshot$SO2))~1,data=airpol_snapshot, nmax = 10)')

		#matern=vgm(0.1, "Mat", 3, kappa=0.5)

		#if(is.element("NO2", var_names))
        robjects.r('matern= (vgm(5, "Mat", 3, kappa=0.5))')
        
        robjects.r('airpol.g <- gstat(airpol.g, model=matern, fill.all=T)')
        robjects.r('v <- variogram(airpol.g,50)')
        robjects.r('airpol.fit = fit.lmc(v, airpol.g, model=matern, fit.ranges=FALSE, correct.diagonal=1.01)')
        
        robjects.r('plot(v, model=airpol.fit)')

		# Running reconstruction and storing output at "info"
        robjects.r('info <- capture.output(timestamp_map_rebuilt <- predict(airpol.fit, newdata = coords))')
        timeserie_map = robjects.r('timeserie_map[[i]] <- timestamp_map_rebuilt ')

		# Formatting console output
        robjects.r('ic <- info[1]') # string log for Intrinsic Correlation
        robjects.r('method <- substr(info[2], 8, 25) ')# string log formatted for cokriging

		# Progress
        robjects.r('progress = ceiling(100*i/length(snapshot_series))')
        robjects.r('cat("\r",format(paste0(ic, " ", method, ": ", progress, "% ")))')
        robjects.r('flush.console()')

    robjects.r('message("\nDone!")')
    return(timeserie_map)

CO_PM10_03_reconst = predict_series(CO_PM10_03_snapshot_series,var_name_CO_PM10_O3, sp_coords)