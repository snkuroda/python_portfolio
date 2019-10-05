"""
Title: Visualing Change in the Garden Home neighborhood

Description:  Iterates through each of the feature classes and pulls buildings
              that the only were built since the previous decade.

              Follow-up with hexbinning and kernel density
"""
# Import Libraries
import arcpy, os, zipfile
from requests import get
from io import BytesIO
from zipfile import ZipFile


# Set Workspsce

wksp = r'E:\GIS_DATA\GEO_267\Garden Home History\Data.gdb'
arcpy.env.workspace = wksp
arcpy.env.overwriteOutput = True


# Set feature classes
featNames = ['Buildings_1955', 'Buildings_1960', 'Buildings_1970'
             , 'Buildings_1985', 'Buildings_1995', 'Buildings_2008'
             , 'Buildings_2010']

# Generate empty list for outputs (for later use)
decadePts = []

## Parse out newly created features per decade  
for feat in featNames:
    # Extract Year from Feature
    CurrentYear = feat.split('_')[-1]
    inLYR = arcpy.MakeFeatureLayer_management(feat, CurrentYear)

    # Set WhereClause based on Year
    WC = """ 'Year_Noted' = %s """ % CurrentYear
    selSet = arcpy.SelectLayerByAttribute_management(inLYR, "", WC)
    # Create New features based on new buildings per decade
    outFeat = "Only" + CurrentYear
    arcpy.CopyFeatures_management(selSet, outFeat)

    # Feature to Point
    arcpy.FeatureToPoint_management(outFeat, "  Point" + CurrentYear)
    decadePts.append("Point" + CurrentYear)

### Create Density Maps with Hexagon Binning

##Create Concave Hull (not included in ArcGIS)
# Download ConcaveHull Tool and import into ArcPy
url = 'https://geonet.esri.com/servlet/JiveServlet/download/54704-1-156235/ConcaveHullByCase.zip'
request = get(url)
zip_file= ZipFile(BytesIO(request.content))
zip_file.extractall(r'E:\GIS_DATA')
arcpy.ImportToolbox(r'E:\GIS_DATA\ConcaveHullByCase')

# Apply Concave Hull to build polygon to overlay hexagon mesh
buildPt = arcpy.FeatureToPoint_management(r'E:\GIS_DATA\GEO_267\Garden Home History\Data.gdb\Buildings_2010', 'Build_pts')
arcpy.ConcaveHull(buildPt, "", 'buildingPerimeter')
arcpy.Merge_management(['buildingPerimeter', 'GH_Neighborhood'], 'hex_basis')


## Apply Hexagons
'''
Using "Create Hexagon Tesselation" tool created by Tim Whiteaker,
Available at http://www.arcgis.com/home/item.html?id=03388990d3274160afe240ac54763e57#!
'''
arcpy.ImportToolbox(r'E:\GIS_DATA\HexagonTool.tbx')
arcpy.CreateHexagonsBySideLength2('hex_basis', 129.48, 'hexagon_base')
# Hexagons per Decade
for decade in decadePts:
    shape = decade.split('.')[0]
    year = shape.split('Point')[1]
    arcpy.SpatialJoin_analysis('hexagon_base', decade, 'hex' + year)

# Hexagons covering all current buildings
arcpy.FeatureToPoint_management(buildPt, 'CurrentBuild')
arcpy.SpatialJoin_analysis('hexagon_base', 'CurrentBuild', 'CurrentHex')
