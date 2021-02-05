"""
Import CSVs and xls files to ESRI
"""

import xlrd, arcpy, csv, os, urllib2
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as BS


# Set Workspace
wksp = r'E:\GIS_DATA\GEO_242\Final_Project\Data\ElectionData.gdb'
arcpy.env.workspace = wksp
arcpy.env.overwriteOutput = True

# Inputs
xls_folder = r'E:\GIS_DATA\GEO_242\Final_Project\ElectionResultAnalysis\Election Data\XLS'
US_counties = r'USCounties'



# Convert xls tables to geodatabase tables
xls_dir = r'E:\GIS_DATA\GEO_242\Final_Project\ElectionResultAnalysis\ElectionData\XLS'
xls_list = os.listdir(xls_dir)
for xls in xls_list:
    xls_path = os.path.join(xls_dir, xls)
    st_name = xls.split('.')[0]
    outDBF = st_name.replace(' ','')

    
    arcpy.ExcelToTable_conversion(xls_path, outDBF)

#Covert csv to geodatabase tables    
csv_dir = r'E:\GIS_DATA\GEO_242\Final_Project\ElectionResultAnalysis\ElectionData\CSV'    
csv_list= os.listdir(csv_dir)
print(csv_list)
for csv in csv_list:
    csv_path = os.path.join(csv_dir, csv)
    df = pd.read_csv(csv_path)
    st_name = csv.split('.')[0]
    
    outDBF =  st_name.replace(' ','')
    print(outDBF)
    ### Convert to ESRI dbf
    x = np.array(np.rec.fromrecords(df.values))

    names = df.dtypes.index.tolist()

    x.dtype.names = tuple(names)
    tbl = arcpy.da.NumPyArrayToTable(x, outDBF[:10])


### Import FIPS numbers and corresponding state
fips_list = []
# Access website with list
url = r'https://www.mcc.co.mercer.pa.us/dps/state_fips_code_listing.htm '
header = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(url, headers=header)
page = urllib2.urlopen(req)
soup = BS(page, "html.parser")

# Parse out table
table = soup.body.find('table')
# Build a 2-D array with fips codes and states
for row in table.findAll('tr')[1:]:
    cells = row.findAll('td')
    fips1 = cells[1].contents[0]
    state1 = cells[2].contents[0]
    fips2 = cells[4].contents[0]
    state2 = cells[5].contents[0]
    
    st_fips = [state1, fips1]
    st_fips2 = [state2, fips2]

    fips_list.append(st_fips)
    fips_list.append(st_fips2)


# Break County map by states
# Get rid codes/states I didnt need
fips_list.sort()
del fips_list[1]
del fips_list[1]
del fips_list[10]
del fips_list[10]
del fips_list[-1]
del fips_list[-6]
del fips_list[-13]

print(fips_list)
for fips in fips_list:

    fip_code = fips[1]
    state = fips[0]
    
    WC = '"STATEFP"=' + "'%s'" %fip_code 
    
    inLYR = arcpy.MakeFeatureLayer_management(US_counties, "Counties", WC)
    
    arcpy.CopyFeatures_management(inLYR, fips[0].replace(' ',"")[:8] + "_co")
    
    print(state.capitalize())

    inFeat = fips[0].replace(' ',"")[:8] + "_co.shp"
    joinTable =  fips[0].capitalize().replace(' ','')
    outFeat_name = fips[0].replace(' ',"")[:6] + "_elec"
    print(inFeat)
    
    print(joinTable)
    joinFeat = arcpy.JoinField_management(inFeat, 'NAME', joinTable, 'County')
    arcpy.CopyFeatures_management(joinFeat, outFeat_name)



