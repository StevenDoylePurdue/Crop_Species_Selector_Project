#!/bin/env python
"""
Program: Raster Quality
Programmer: Steven Doyle
Date: 04.13.2021


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    Referring to point ID, join-to-polygon status, grid coordinates, country ID, 
    country name, state ID, and state name."""
    

    # open and read the file
    DataDF = pd.read_csv(fileName,header=0, usecols=[0,1,4,5,6,7,8])
    
    
    # define and initialize the missing data dictionary
    
     
    return( DataDF)

    
def Check01_RemoveNoDataValues( DataDF):
    """This check removes all points which have not been joined to a polygon."""
    
    # Drop na for state ID
    DataDF = DataDF.dropna(subset=['GID_1'])

    return( DataDF)



if __name__ == '__main__':

    fileName = "growing_period_join.csv"
    DataDF= ReadData(fileName)
    InitialDF = DataDF.copy()
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF= Check01_RemoveNoDataValues( DataDF)
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    
    
    
    
    
    
    
    
    
    
    
    
    