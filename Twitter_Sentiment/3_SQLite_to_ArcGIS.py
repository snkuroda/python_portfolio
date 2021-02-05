"""
Title: Import sql table to Arc
Description: Import sqlite tables containing the parsed tweets to ArcMap,
             using pandas dataframes as an intermediary.
"""
import sqlite3, os, arcpy
import pandas as pd
import numpy as np

# Set Arc Environments
wksp = r'E:\GIS_DATA\GEO_242\Final_Project\Data\Tweets'
arcpy.env.workspace = wksp
arcpy.env.overwriteOutput = True

tableList = ['trump', 'climate', 'news', 'politics', 'covfefe']
for table in tableList:
    # Connect and read SQLite data by table name
    conn = sqlite3.connect('selected_tweets.db')
    inTable = ("SELECT * FROM %s" %table)
    df = pd.read_sql_query(inTable, conn)

    # Set output objects
    outDBF = table + ".dbf"
    lyrName = table
    outSHP = table + ".shp"
    print(outDBF, lyrName, outSHP)
    ### Convert to ESRI dbf
    x = np.array(np.rec.fromrecords(df.values))
    
    names = df.dtypes.index.tolist()

    x.dtype.names = tuple(names)

    tbl = arcpy.da.NumPyArrayToTable(x, os.path.join(wksp, outDBF))

    lyr = arcpy.MakeXYEventLayer_management(os.path.join(wksp, outDBF), "y_coordina", "x_coordina", lyrName)

    # arcpy.
