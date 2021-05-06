#!/bin/env python
"""
Program: ECO_Crop Exploration
Programmer: Steven Doyle
Date: 04.13.2021

This script examines the ecocrop list and produces figures on the dataset's agronomic requirements.

inputs: "ecocrop_cleaned.csv", 'cropbasics_scrape.csv'
outputs: 'rainfall_changes_prob.png', 'temp_diff.png', 'Minimum_Temp_vs_Altitude.png'

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe."""
    

    # open and read the file
    DataDF = pd.read_csv(fileName,header=0, index_col=('Species'))
    
    
    # define and initialize the missing data dictionary
    
     
    return( DataDF)




if __name__ == '__main__':

    fileName = "ecocrop_cleaned.csv"
    DataDF= ReadData(fileName)

    file2 = 'cropbasics_scrape.csv'
    olddf = ReadData(file2)

    # Plot temps
    fig = plt.figure()
    a = plt.hist(DataDF['Rain_Opt_Min'], color='r', alpha = 0.3, density = True, bins = 20, range = (0, 5000))
    b = plt.hist(olddf['Rain_Opt_Min'], color='b',alpha = 0.3, density = True, bins = 20, range = (0, 5000))
    plt.title('Initial and Corrected Minimum Optimal Rainfall Probability Density')  # Title
    plt.xlabel('Rainfall (mm)')  # X axis label
    plt.ylabel('Probability Density')  # Y axis label

    fig.savefig('rainfall_changes_prob.png')  # Save figure to file as image
    plt.show()





    # Plot temps
    fig = plt.figure()
    a = plt.hist(DataDF['Temp_Opt_Max']-DataDF['Temp_Opt_Min'], color='r', alpha = 0.3, bins = 20, range = (0, 60))
    b = plt.hist(DataDF['Temp_Abs_Max']-DataDF['Temp_Abs_Min'], color='b',alpha = 0.3, bins = 20, range = (0, 60))
    plt.title('Temperature Range Distribution')  # Title
    plt.xlabel('Degrees (Celsius)')  # X axis label
    plt.ylabel('Records')  # Y axis label
    
    fig.savefig('temp_diff.png')  # Save figure to file as image
    plt.show()


    #Plot temp vs alt
    fig = plt.figure()
    a = plt.scatter(DataDF['Temp_Opt_Min'], DataDF['Alt_Abs_Max'])
    plt.title('Optimum Minimum Temperature vs Altitude')
    plt.xlabel('Optimum Minimum Temperature (Degrees Celsius)')
    plt.ylabel('Maximum Altitude (Meters)')
    fig.savefig('Minimum_Temp_vs_Altitude.png')
    plt.show()

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    