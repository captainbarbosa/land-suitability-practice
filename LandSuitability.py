# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
# Script File Name: LandSuitability.py
# Author: Nadia Barbosa
# Date: 02.22.15
# Purpose: Calculates an output raster modeling land suitability based on DEM & Land Use raster inputs and two weight values.
#
# TOOL PARAMTER SETTINGS: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#           *DISPLAY NAME*         *DATA TYPE*      *TYPE*         *DIRECTION*
#     [0] = "Workspace"          = Workspace        = Required     = Input 
#     [1] = "Output raster name" = String           = Required     = Output
#     [2] = "DEM Raster"         = Raster Layer     = Required     = Input
#     [3] = "Land Use Raster"    = Raster Layer     = Required     = Input
#     [4] = "Slope weight"       = String           = Required     = Input
#     [5] = "Aspect weight"      = String           = Required     = Input
# -----------------------------------------------------------------------------------

# ---Import Modules---#
import os
import arcpy
from arcpy import env
from arcpy.sa import *

#---Overwrite any output---#
env.overwriteOutput = True 


#---Creating error classes---#
class LicenseError(Exception):
    pass
class WeightRangeError(Exception):
    pass
class WeightSumError(Exception):
    pass

#---Try block---#
try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("     Spatial analyst extension checked out")
    else:
        raise LicenseError
    
    #---Set tool parameters---#
    env.workspace = inWorkspace = arcpy.GetParameterAsText(0)  
    outputRaster = arcpy.GetParameterAsText(1)
    inDEM = arcpy.GetParameterAsText(2)
    inLandUseDEM = arcpy.GetParameterAsText(3)
    Weight_1 = float(arcpy.GetParameterAsText(4))
    Weight_2 = float(arcpy.GetParameterAsText(5))
    
    #---Validate weights from user input, raise value error if incorrect---#
    if Weight_1 >= 0.0 and Weight_1 <= 1.0:
        pass
    else:
        arcpy.AddError("Error with with SLOPE weight: ")
        raise WeightRangeError(Weight_1)
    if Weight_2 >= 0.0 and Weight_2 <= 1.0:
        pass
    else:
        arcpy.AddError("Error with ASPECT weight: ")
        raise WeightRangeError(Weight_2)
    if Weight_1+Weight_2==1.0:
            pass
    else:
        arcpy.AddError("Error with sum of weights: ")
        raise WeightSumError(Weight_1,Weight_2) 
    
    #     ---BEGIN MAIN CALCULATIONS---     #
    arcpy.AddMessage("---BEGINNING CALCULATIONS---")
    
    #-------------------------------------------------
    # 1) Reclassify land use raster
    reclassLandUse1 = Reclassify(inLandUseDEM, "Value", RemapValue([[11,0],[12,0],[13,0],[14,0],[15,0],
                                                                    [16,0],[18,1],[21,0],[22,0],[23,0],
                                                                    [30,0],[41,0],[42,0],[43,0],[44,0],
                                                                    [50,0],[60,0],[73,1],[74,0],[171,0],
                                                                    [172,0],[242,0]]), "DATA")
    arcpy.AddMessage("     Reclassifying land use...")
    #-------------------------------------------------
    # 2) Calculate slope based on DEM raster
    slopeDEM2 = Slope(inDEM, "DEGREE")
    arcpy.AddMessage("     Calculating slope...")
    #-------------------------------------------------
    # 3) Reclassify slope raster from step #2
    reclassSlope3 = Reclassify(slopeDEM2, "Value", RemapRange([[0,3,3],
                                                               [3,6,2],
                                                               [6,90,1]]), "DATA")
    arcpy.AddMessage("     Reclassifying slope...")
    #-------------------------------------------------
    # 4) Multiply reclassified slope from step #3 by slope weight integer
    reclassSlopeTimesW14 = Times(reclassSlope3, Weight_1)
    arcpy.AddMessage("     Multiplying slope by weight...")
    #-------------------------------------------------
    # 5) Calculate aspect based on DEM raster
    aspectDEM5 = Aspect(inDEM)
    arcpy.AddMessage("     Calculating aspect...")
    #-------------------------------------------------
    # 6) Reclassify aspect raster from step #5
    reclassAspect6 = Reclassify(aspectDEM5, "Value", RemapRange([[-1,0,3],
                                                                 [0,45,1],
                                                                 [45,135,2],
                                                                 [135,225,3],
                                                                 [225,315,2],
                                                                 [315,360,1]]), "DATA")
    arcpy.AddMessage("     Reclassifying aspect...")
    #-------------------------------------------------
    # 7) Multiply reclassified aspect from step #6 by aspect weight integer
    reclassAspectTimesW27 = Times(reclassAspect6, Weight_2)
    arcpy.AddMessage("     Multiplying aspect by weight")
    #-------------------------------------------------
    # 8) Adding step #4 and step #7
    finalCalc8 = Plus(reclassSlopeTimesW14, reclassAspectTimesW27)
    arcpy.AddMessage("     Adding results...")
    #-------------------------------------------------
    # 9) Adding step #8 to step #1 for final output
    finalRaster10 = Times(finalCalc8, reclassLandUse1)
    arcpy.AddMessage("     Finalizing calculations...")
    #-------------------------------------------------
    
    #     ---END MAIN CALCULATIONS---     #

    #---Save final output to workspace---#
    finalRaster10.save(outputRaster)   
    arcpy.AddMessage("     Saving final output to workspace...")
    arcpy.AddMessage("          COMPLETE!")
 
    #---Delete in-memory files---#
    arcpy.Delete_management("in_memory")
    
    #---Error handling---#
except WeightRangeError:
    arcpy.AddError("   Weight must fall between 0 and 1.")
except WeightSumError:
    arcpy.AddError("   Both weights MUST add up to 1.")
except LicenseError:
    arcpy.AddIDMessage("Error", 626)
    arcpy.AddError("Spatial analyst extension not found")
except StandardError as e:
    print e
except:
    print arcpy.GetMessages(2)
finally:
    #---Return extension---#
    arcpy.CheckInExtension("Spatial")    
    

    
    

