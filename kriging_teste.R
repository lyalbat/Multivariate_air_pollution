library(gstat)
library(hash)
library(sp)
library(tidyr)
library(EnvStats)
library(png)

# -----------------------------------------------------------------
export_img <- function(name_, points) {

	xcoords <- ceiling(points$x)
	ycoords <- ceiling(points$y)

	fieldMatrix <- matrix(1, nrow=100, ncol=100)

	for(i in 1:length(xcoords)) {
		fieldMatrix[xcoords[i], ycoords[i]] = 0
	}

	graphics.off()
	postscript(name_,horizontal=FALSE,onefile=FALSE,height=8,width=8,pointsize=14)
	image(fieldMatrix, col=gray((1:32)/32), xaxt="n", yaxt="n", xlab="", ylab="")
	graphics.off()

}
# -----------------------------------------------------------------
# Build a temporal sequence with 
predict_series <- function(snapshot_series, var_names, coords) {

	timeserie_map <- list()
	matern <- NULL


	for(i in 1:length(snapshot_series)) {
		airpol_snapshot <- snapshot_series[[i]]
		airpol.g <- NULL

		if(is.element("CO", var_names))
			airpol.g <- gstat(id="CO", 
					  formula= log(unlist(airpol_snapshot$CO)) ~ 1,
					  data=airpol_snapshot, 
					  nmax = 10)

		if(is.element("PM10", var_names))
			airpol.g <- gstat(airpol.g, 
					  "PM10", 
					  log(unlist(airpol_snapshot$MP10))~1,
					  data=airpol_snapshot, 
					  nmax = 10)

		if(is.element("O3", var_names))
			airpol.g <- gstat(airpol.g, 
					  "O3", 
					  log(unlist(airpol_snapshot$O3))~1,
					  airpol_snapshot, 
					  nmax = 10)

		if(is.element("NO2", var_names))
			airpol.g <- gstat(airpol.g, 
					  "NO2", 
					  log(unlist(airpol_snapshot$NO2))~1,
					  airpol_snapshot, 
					  nmax = 10)

		if(is.element("SO2", var_names))
			airpol.g <- gstat(airpol.g, 
					  "SO2", 
					  log(unlist(airpol_snapshot$SO2))~1,
					  airpol_snapshot, 
					  nmax = 10)


		#matern=vgm(0.1, "Mat", 3, kappa=0.5)

		#if(is.element("NO2", var_names))
			matern=vgm(5, "Mat", 3, kappa=0.5)

		airpol.g <- gstat(airpol.g, model=matern, fill.all=T)
		v <- variogram(airpol.g,50)

		airpol.fit = fit.lmc(v, airpol.g, model=matern, 
						  fit.ranges=FALSE, 
						  correct.diagonal=1.01)

		plot(v, model=airpol.fit)

		# Running reconstruction and storing output at "info"
		info <- capture.output(
			timestamp_map_rebuilt <- predict(airpol.fit, newdata = coords)
		)

		timeserie_map[[i]] <- timestamp_map_rebuilt 

		# Formatting console output
		ic <- info[1] # string log for Intrinsic Correlation
		method <- substr(info[2], 8, 25) # string log formatted for cokriging

		# Progress
		progress = ceiling(100*i/length(snapshot_series))
		cat('\r',format(paste0(ic, " ", method, ": ", progress, "% ")))
		flush.console()
	}

	message("\nDone!")
	return(timeserie_map)
}
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Assign predicted samples to missing stations
# Rerturns () with
station_assign <- function(var_to_assign, 
			   missing_station_coord,
			   var_reconst_series,
 			   summary_table_out # dataset to be updated 
			   ) {

	# Early statements
	var_name <- var_to_assign
	pred_st <- summary_table_out

	# Assemblying stations with missing variables
	missing_var_station <- expand.grid(var_name,
					   names(missing_station_coord))

	missing_var_station <- missing_var_station[c("Var2", "Var1")]

	# Set of station/pollutant to be assigned with new sample i.e.:missing_station_NO2
	missing_station_var  <- {} 
	for(i in 1:nrow(missing_var_station)) 
		missing_station_var[i] <- paste(missing_var_station[i,1], 
						missing_var_station[i,2], sep='_')

	# Assigning predicted values at gathered missing stations
	for(i in 1:nrow(pred_st)) {

		# Filtering columns with missing samples, only navigate where's NA
		st_var_missing_indexes <- which(is.na(pred_st[i,]))
		st_var_missing <- names(pred_st[i,st_var_missing_indexes]) 

		# Missing station/variables to fill with predicted samples on this turn
		var_indexes <- match(missing_station_var, st_var_missing)

		# Indexes to get cols in summary table with missing samples
		st_col_assign <- na.exclude(st_var_missing_indexes[var_indexes])

		# Names of missing stations and empty vector to store missing samples
		missing_station_names <- names(pred_st[i, st_col_assign])
		missing_station_samples <- {}

		for(missing_station in missing_station_names) {

			 # Tokenizing by field and cleaning indexes
			stok_station <- unlist( strsplit(missing_station, "_") ) 

			# Getting pollutant variable to assign prediction
			var <- stok_station[2]

			# Getting respective coords from current missing station
			station <- stok_station[1]
			coord_missing <- missing_station_coord[[station]]
			x <- coord_missing[1]
			y <- coord_missing[2]

			# Map coordinates for reference
			map_coords <- coordinates(var_reconst_series[[i]])
			x_ref <- map_coords[,1]
			y_ref <- map_coords[,2]

			# Matching x and y separately
			x_match <- which(x==x_ref)
			y_match <- which(y==y_ref)

			# Finding index for get sample at missing coord (same for x,y)
			sample_index <- match(x_match, y_match)
			sample_index <- y_match[na.exclude(sample_index)] 

			# Halt execution if no matching index is found
			if(!length(sample_index)) 
				stop("No matching coordinate. Check if it's out of bounds.")

			sample <- NULL

			# Get sample from matched position x,y
			if(var == "CO")
				sample <- round(var_reconst_series[[i]]$CO.pred[sample_index],2)

			if(var == "PM10")
				sample <- round(var_reconst_series[[i]]$MP10.pred[sample_index],2)

			if(var == "O3")
				sample <- round(var_reconst_series[[i]]$O3.pred[sample_index],2)

			if(var == "NO2")
				sample <- round(var_reconst_series[[i]]$NO2.pred[sample_index],2) 

			if(var == "SO2")
				sample <- round(var_reconst_series[[i]]$SO2.pred[sample_index],2)

			# Assemblying a sequence with predicted samples to assign at missing row
			missing_station_samples <- append(missing_station_samples, sample)

		}

		# Assign predicted sample row to missing cells at summary table
		pred_st[i, st_col_assign] <- missing_station_samples

		# Progress
		progress = ceiling(100*i/nrow(pred_st))
		cat('\r',format(paste("Progress: ", progress, "%", sep='')))
		flush.console()

	}

	message("\nDone!")
	return(pred_st)
}
# -----------------------------------------------------------------

# -----------------------------------------------------------------

# Create a data frame with each predicted x,y of map as cols and timestamps as rows

pol_map <- function(pred_st, reconst_series) {

	pol_map <- data.frame(pred_st$Date, pred_st$Time)
	names(pol_map) <- c("Date","Time")

	# Consistency check for x,y sequences
	for(i in 1:length(reconst_series)) {
		x_set <- all(reconst_series[[1]]$x == reconst_series[[i]]$x)
		y_set <- all(reconst_series[[1]]$y == reconst_series[[i]]$y)

		if(!x_set || !y_set)
			stop("Execution Halted: Coords for all timestamps shall have the same ordering, coord set not match.")
	}	

	# Since that reconst_series[1]$x /$y == reconst_series[n]$x / $y
	map_coords <- paste(paste(reconst_series[[1]]$x), 
			    paste(reconst_series[[1]]$y), sep=',')

	# Creating columns to store each x,y sample
	pol_map[map_coords] <- NA

	# Copying pol_map template for each variable
	pol_map_CO <- pol_map
	pol_map_MP10 <- pol_map
	pol_map_O3 <- pol_map
	pol_map_NO2 <- pol_map
	pol_map_SO2 <- pol_map

	# Creating pollution maps
	for(i in 1:length(reconst_series)) {
		pol_map_CO[i,3:ncol(pol_map_CO)] <- reconst_series[[i]]$CO.pred
		pol_map_MP10[i,3:ncol(pol_map_MP10)] <- reconst_series[[i]]$MP10.pred
		pol_map_O3[i,3:ncol(pol_map_O3)] <- reconst_series[[i]]$O3.pred
		pol_map_SO2[i,3:ncol(pol_map_SO2)] <- reconst_series[[i]]$SO2.pred
		pol_map_NO2[i,3:ncol(pol_map_NO2)] <- reconst_series[[i]]$NO2.pred

		# Progress
		progress = ceiling(100*i/length(reconst_series))
		cat('\r',format(paste("Progress: ", progress, "%", sep='')))
		flush.console()
	}

	# DOUBLE CHECK HERE (!z!)
	
	# Exporting files to parse as input to network simulator
	write.csv(pol_map_CO, "maps/pol_map_CO.csv", row.names=FALSE)
	write.csv(pol_map_MP10, "maps/pol_map_MP10.csv", row.names=FALSE)
	write.csv(pol_map_O3, "maps/pol_map_O3.csv", row.names=FALSE)
	write.csv(pol_map_NO2, "maps/pol_map_NO2.csv", row.names=FALSE)
	write.csv(pol_map_SO2, "maps/pol_map_SO2.csv", row.names=FALSE)

	message("\nDone!")

}
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Create a data frame with each predicted x,y of map as cols and timestamps as rows
export_map <- function(reconst_series) {

	for(i in 1:length(reconst_series)) {

		png(paste0("pollutant_map/map_CO/",i,"_CO.png"))
		print(spplot(reconst_series[[i]]["CO.pred"]))
		dev.off()

		png(paste0("pollutant_map/map_MP10/",i,"_MP10.png"))
		print(spplot(reconst_series[[i]]["MP10.pred"]))
		dev.off()

		png(paste0("pollutant_map/map_O3/",i,"_O3.png"))
		print(spplot(reconst_series[[i]]["O3.pred"]))
		dev.off()

		png(paste0("pollutant_map/map_SO2/",i,"_SO2.png"))
		print(spplot(reconst_series[[i]]["SO2.pred"]))
		dev.off()

		png(paste0("pollutant_map/map_NO2/",i,"_NO2.png"))
		print(spplot(reconst_series[[i]]["NO2.pred"]))
		dev.off()

		# Progress
		progress = ceiling(100*i/length(reconst_series))
		cat('\r',format(paste("Progress: ", progress, "%", sep='')))
		flush.console()
	}

	message("\nDone!")
}
