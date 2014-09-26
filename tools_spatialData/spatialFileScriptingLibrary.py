# -*- coding: utf-8 -*-
"""
This is a library of some basic spatial data manipulation commands in arcpy. Current sections include:
  1) loading the arcpy library and activating some of the useful functions of arcpy
  2) Some file management commands
  3) Some commands for shapefile manipulation
  4) Some commands for raster manipulation (to be added)

Note - there is a good help page available at http://help.arcgis.com/en/arcgisdesktop/10.0/help/ (look
  in the 'Professional Library dropdown'. If you run a different version of arcGIS, you might need 
  to consult that version's help page as well.

Created on Fri Sep 26 08:09:46 2014
@author: nrobinson
"""

#------------------------------------------------------------------------------------------------
# (1)
import arcpy
from arcpy import env  #To set your working environment
arcpy.CheckOutExtension("Spatial")  #Activates the spatial analyst extension, which is often required

#------------------------------------------------------------------------------------------------
# (2)
#File management, etc.
# LIST - shapefiles or rasters in your workspace    
print arcpy.ListFeatureClasses()
print arcpy.ListRasters()


#PROJECT (for SHP)- files to the correct CRS - I have always used a .prj file (e.g., from a proj4 library)
#  for the coordRefFile, but the online help indicates that you might be able to point to a 
#  spatial reference file that is native to arcpy (cool!) by using: arcpy.SpatialReference('NAD 1983 UTM Zone 11N')
arcpy.Project_management (in_dataset, out_dataset, coordRefFile, {transform_method}, {in_coor_system})


#DEFINE PROJECTION (for RASTER) - to make sure lal files are output in the same projection
#First, set path to projection info 
PrjPath=r"C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\Europe\S-JTSK Krovak EastNorth.prj"
#Then use the path to save raster files in the correct projection
arcpy.DefineProjection_management(outGrid, prjfile)

#------------------------------------------------------------------------------------------------
# (3)
#Some commands for shapefile manipulation:
#CLIP - Here's an example of clipping an Open Space layer to city limits of various files.
openSpace = "boulderCountyOpen.shp"

# Create list of city boundary shapefile names
cities = ["boulder", "lafayette", "louisville"]

# Loop through cities list and clip open space to each municipality
for i in cities:
    arcpy.Clip_analysis(openSpace, i + ".shp", i + "Open.shp")
    print "open space clipped to " + i + " city limits"


#BUFFER - Basic command to buffer features in a shapefile. There are additional specificiations
#  available, e.g., whether you want the buffer rounded off, in the online help.
arcpy.Buffer_analysis(inputShapefile,outputShapefile,bufferDistance [inc. units])

#INTERSECT - Here is an intersect function - I haven't done this, the command came from the help
#  page at arcgis.com

#The first list is input file names in the workspace, 'mysites' is an output feature class, 'ALL'
#  means that all attributes from the input files willbe transfered to the output
arcpy.Intersect_analysis (["vegetation_stands", "road_buffer200m", "water_buffer100"], "mysites", "ALL", "", "")

# Here, the input files are being ranked for importance during the intersect, so the files with a 2 will snap to the 'road_buffer200m' file.
arcpy.Intersect_analysis ([["vegetation_stands", 2], ["road_buffer200m", 1], ["water_buffer100", 2]], "mysites_ranked", "ALL", "", "")

#------------------------------------------------------------------------------------------------
# (4)
#Some commands for raster manipulation:
#Coming soon!
