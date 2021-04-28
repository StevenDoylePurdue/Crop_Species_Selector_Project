#!/bin/env python
"""
Program: Raster Quality
Programmer: Steven Doyle
Date: 04.13.2021

This script reads attribute csv files and filters out any errors. It produces
filtered csv files.

"""

import pandas as pd

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame. It uses the columns:
        OID_
        Join_Count
        grid_code
        GID_0
        NAME_0
        GID_1
        NAME_1
        ENGTYPE_1
    Referring to point ID, join-to-polygon status, grid coordinates, country ID, 
    country name, state ID, state name, subnational jurisdiction classification."""
    

    # open and read the file
    DataDF = pd.read_csv(fileName,header=0)
    DataDF = DataDF.drop(['OID_', 'TARGET_FID', 'pointid', 'VARNAME_1', 'NL_NAME_1',
                          'TYPE_1', 'CC_1', 'HASC_1'], axis=1)
     
    return( DataDF)

    
def RemoveNoDataValues( DataDF):
    """This check removes all points which have not been joined to a polygon."""
    
    
    DataDF = DataDF.dropna(subset=['GID_1'])  # Drop na for state ID
    DataDF = DataDF.dropna(subset=['grid_code'])  # Drop na for attribute value
    DataDF = DataDF[DataDF['Join_Count'] == 1]  # Drop all cells that have not successfully been joined
    DataDF = DataDF.drop(['Join_Count'], axis=1)


    return( DataDF)



if __name__ == '__main__':

    fileList = ['diurnal_join.csv', 'dry_seasons_join.csv', 'el_join.csv', 'precip_join.csv', 'soils_join.csv',
                'wet_temp_join.csv', 'growing_period_join.csv']

    for file in fileList:
        fileName = file
        DataDF = ReadData(fileName)
        DataDF = RemoveNoDataValues(DataDF)
        print('{} checked'.format(file))
        DataDF.to_csv('checked_{}'.format(file), header=True, index=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    