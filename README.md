# LandSuitability


This is an ArcPy tool made for a final project GEOG-656, Programming and Scripting for GIS at the University of Maryland. It is not intended for use in real-life scenarios, but is rather a personal practice in developing an ArcPy tool.   

**_Important_**: The two raster inputs (used in step 1) used to run this tool examine the area of Prince George's County, Maryland. If you would like to use the identical rasters used in this script example, please contact me. However, Any two DEM and land use rasters should work. Keep in mind the Land Use reclassification is arbitrary and the results are not intended for actual use.
_______________________

####The tool performs the following tasks:  

######1) Accepts input of two rasters as parameters to the tool (DEM and Land Use)  

######2) Input two decimal values representing weights for each suitability layer (w1 and w2)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Where w1 and w2 take values between 0 and 1 inclusively, and add up to 1.0.     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Only slope and aspect have a weight parameter, land use does not.  

######3) Create one output raster that is be defined by the user  

######4) Calculate the Slope and Aspect from the DEM  

######5) Reclassifies the Slope Layer 

Slope Reclassification:   

Old Slope Value (Degree)  | New Slope Value (Rank)
:-------------: | :-------------:
0-3  | 3
3-6  | 2 
6-90  | 1

######6) Reclassifies the Aspect Layer  

Aspect Reclassification:   

Old Aspect Value (Degree)  | New Aspect Value (Rank)
:-------------: | :-------------:
-1-0  | 3
0-45  | 1 
45-135  | 2
135-225  | 3
225-315  | 2
315-360  | 1

######7) Reclassifies the Land Use Layer  

Land Use Reclassification:   

Old Land Use Code  | New Slope Value (Rank)
:-------------: | :-------------:
18 (Urban land)  | 1
73 (Bare Ground)  | 1 
All Others  | 0

######8) Models the suitability based on the following formula:  

*Best Site = int(w1 * Reclassified Slope + w2 * Reclassified Aspect) * Reclassified Land Use*    

#### Result:    
The final output is a raster with values of 0-3, with the higher amount indicating the best areas for building new housing according to previously defined parameters. 

_______________________
#### ArcPy Tool Configuration in ArcMap   

The following parameter properties are assigned when using this script as a custom tool in ArcMap:

Parameter  | Data Type | Required? | Direction
:-------------: | :-------------: | :-------------: | :-------------:
Workspace | Workspace | No | Input
Output Raster Name | Raster Layer | No | Output
DEM Input | Raster Layer | Yes | Input
Land Use Input | Raster Layer | Yes | Input
Weight 1 | Any Value | Yes | Input
Weight 2 | Any Value | Yes | Input



