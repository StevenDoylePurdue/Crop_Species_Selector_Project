#!/bin/env python
"""
Program: ECOCrop Quality
Programmer: Steven Doyle
Date: 04.13.2021

This script reads in the ECOCrop scraped csv file 'cropbasics_scrape.csv' as 
a dataframe. It converts performs a quality check and for gross errors by 
converting any impossible values to na and switching back any flipped values 
for maxima and minima attributes. It then drops all rows with na values for the 
key set of variables:
Temp_Opt_Min
Temp_Opt_Max
Temp_Abs_Min
Temp_Abs_Max
Rain_Opt_Min
Rain_Opt_Max
Rain_Abs_Min
Rain_Abs_Max
Alt_Abs_Max
pH_Opt_Min
pH_Opt_Max
pH_Abs_Min
pH_Abs_Max
Texture_Opt
Texture_Abs
Fertility_Opt
Fertility_Abs
Cycle_Min
Cycle_Max
It produces a cleaned csv file 'ecocrop_cleaned.csv', as well as a table listing 
na values by column and the number of rows dropped and saves it as a tab delimited 
txt file 'ecocrop_dropped_values.txt'. It also plots figures comparing before 
and after quality check distributions for attribute values.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the species name. Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Species', 
                'Temp_Opt_Min', 'Temp_Opt_Max', 
                'Temp_Abs_Min', 'Temp_Abs_Max', 'Rain_Opt_Min', 'Rain_Opt_Max', 
                'Rain_Abs_Min', 'Rain_Abs_Max', 'Alt_Abs_Max', 'pH_Opt_Min', 'pH_Opt_Max', 
                'pH_Abs_Min', 'pH_Abs_Max', 
                'Texture_Opt', 'Texture_Abs', 'Fertility_Opt', 'Fertility_Abs', 
                'Salinity_Opt', 'Salinity_Abs' 
                'Cycle_Min', 'Cycle_Max']

    # open and read the file
    DataDF = pd.read_csv(fileName,header=0)
    DataDF = DataDF.set_index('Species')
    for col in DataDF.columns[1:13]:
        DataDF[col] = DataDF[col].astype(float)
    for col in DataDF.columns[18:19]:
        DataDF[col] = DataDF[col].astype(float)
    
    
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
    ReplacedValuesDF.at['1. No Data', 'Temp_Opt_Min'] = DataDF['Temp_Opt_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Temp_Opt_Max'] = DataDF['Temp_Opt_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Temp_Abs_Min'] = DataDF['Temp_Abs_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Temp_Abs_Max'] = DataDF['Temp_Abs_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Rain_Opt_Min'] = DataDF['Rain_Opt_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Rain_Opt_Max'] = DataDF['Rain_Opt_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Rain_Abs_Min'] = DataDF['Rain_Abs_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Rain_Abs_Max'] = DataDF['Rain_Abs_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Alt_Abs_Max'] = DataDF['Alt_Abs_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'pH_Opt_Min'] = DataDF['pH_Opt_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'pH_Opt_Max'] = DataDF['pH_Opt_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'pH_Abs_Min'] = DataDF['pH_Abs_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'pH_Abs_Max'] = DataDF['pH_Abs_Max'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Cycle_Min'] = DataDF['Cycle_Min'].isna().sum()
    ReplacedValuesDF.at['1. No Data', 'Cycle_Max'] = DataDF['Cycle_Max'].isna().sum()
    return( DataDF, ReplacedValuesDF )


def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""

    # Count the occurrences of gross error
    
    a=DataDF.loc[DataDF.Temp_Opt_Min < 0, 'Temp_Opt_Min'].count()
    b=DataDF.loc[DataDF.Temp_Opt_Min > 60, 'Temp_Opt_Min'].count()
    toi=a+b
    c=DataDF.loc[DataDF.Temp_Opt_Max <= 0, 'Temp_Opt_Max'].count()
    d=DataDF.loc[DataDF.Temp_Opt_Max > 60, 'Temp_Opt_Max'].count()
    toa=c+d
    e=DataDF.loc[DataDF.Temp_Abs_Min < 0, 'Temp_Abs_Min'].count()
    f=DataDF.loc[DataDF.Temp_Abs_Min > 60, 'Temp_Abs_Min'].count()
    tai=e+f
    g=DataDF.loc[DataDF.Temp_Abs_Max <= 0, 'Temp_Abs_Max'].count()
    h=DataDF.loc[DataDF.Temp_Abs_Max > 60, 'Temp_Abs_Max'].count()
    taa=g+h
    
    i=DataDF.loc[DataDF.Rain_Opt_Min < 0, 'Rain_Opt_Min'].count()
    j=DataDF.loc[DataDF.Rain_Opt_Min > 12000, 'Rain_Opt_Min'].count()
    roi=i+j
    k=DataDF.loc[DataDF.Rain_Opt_Max <= 0, 'Rain_Opt_Max'].count()
    l=DataDF.loc[DataDF.Rain_Opt_Max > 12000, 'Rain_Opt_Max'].count()
    roa=k+l
    m=DataDF.loc[DataDF.Rain_Abs_Min < 0, 'Rain_Abs_Min'].count()
    n=DataDF.loc[DataDF.Rain_Abs_Min > 12000, 'Rain_Abs_Min'].count()
    rai=m+n
    o=DataDF.loc[DataDF.Rain_Abs_Max <= 0, 'Rain_Abs_Max'].count()
    p=DataDF.loc[DataDF.Rain_Abs_Max > 12000, 'Rain_Abs_Max'].count()
    raa=o+p
    
    q=DataDF.loc[DataDF.Alt_Abs_Max <= 0, 'Alt_Abs_Max'].count()
    r=DataDF.loc[DataDF.Alt_Abs_Max > 6500, 'Alt_Abs_Max'].count()
    aaa=q+r
    
    s=DataDF.loc[DataDF.pH_Opt_Min < 0, 'pH_Opt_Min'].count()
    t=DataDF.loc[DataDF.pH_Opt_Min > 14, 'pH_Opt_Min'].count()
    poi=s+t
    u=DataDF.loc[DataDF.pH_Opt_Max <= 0, 'pH_Opt_Max'].count()
    v=DataDF.loc[DataDF.pH_Opt_Max > 14, 'pH_Opt_Max'].count()
    poa=u+v
    w=DataDF.loc[DataDF.pH_Abs_Min < 0, 'pH_Abs_Min'].count()
    x=DataDF.loc[DataDF.pH_Abs_Min > 14, 'pH_Abs_Min'].count()
    pai=w+x
    y=DataDF.loc[DataDF.pH_Abs_Max <= 0, 'pH_Abs_Max'].count()
    z=DataDF.loc[DataDF.pH_Abs_Max > 14, 'pH_Abs_Max'].count()
    paa=y+z
    
    aa=DataDF.loc[DataDF.Cycle_Min < 0, 'Cycle_Min'].count()
    ab=DataDF.loc[DataDF.Cycle_Min > 365, 'Cycle_Min'].count()
    ci=aa+ab
    ac=DataDF.loc[DataDF.Cycle_Max <= 0, 'Cycle_Max'].count()
    ad=DataDF.loc[DataDF.Cycle_Max > 365, 'Cycle_Max'].count()
    ca=ac+ad

    # Replace outliers with nan values if above or below thresholds
    
    DataDF.loc[DataDF.Temp_Opt_Min < 0, 'Temp_Opt_Min'] = np.nan
    DataDF.loc[DataDF.Temp_Opt_Min > 60, 'Temp_Opt_Min'] = np.nan
    DataDF.loc[DataDF.Temp_Opt_Max <= 0, 'Temp_Opt_Max'] = np.nan
    DataDF.loc[DataDF.Temp_Opt_Max > 60, 'Temp_Opt_Max'] = np.nan
    DataDF.loc[DataDF.Temp_Abs_Min < 0, 'Temp_Abs_Min'] = np.nan
    DataDF.loc[DataDF.Temp_Abs_Min > 60, 'Temp_Abs_Min'] = np.nan
    DataDF.loc[DataDF.Temp_Abs_Max <= 0, 'Temp_Abs_Max'] = np.nan
    DataDF.loc[DataDF.Temp_Abs_Max > 60, 'Temp_Abs_Max'] = np.nan
    
    DataDF.loc[DataDF.Rain_Opt_Min < 0, 'Rain_Opt_Min'] = np.nan
    DataDF.loc[DataDF.Rain_Opt_Min > 12000, 'Rain_Opt_Min'] = np.nan
    DataDF.loc[DataDF.Rain_Opt_Max <= 0, 'Rain_Opt_Max'] = np.nan
    DataDF.loc[DataDF.Rain_Opt_Max > 12000, 'Rain_Opt_Max'] = np.nan
    DataDF.loc[DataDF.Rain_Abs_Min < 0, 'Rain_Abs_Min'] = np.nan
    DataDF.loc[DataDF.Rain_Abs_Min > 12000, 'Rain_Abs_Min'] = np.nan
    DataDF.loc[DataDF.Rain_Abs_Max <= 0, 'Rain_Abs_Max'] = np.nan
    DataDF.loc[DataDF.Rain_Abs_Max > 12000, 'Rain_Abs_Max'] = np.nan
    
    DataDF.loc[DataDF.Alt_Abs_Max <= 0, 'Alt_Abs_Max'] = np.nan
    DataDF.loc[DataDF.Alt_Abs_Max > 6500, 'Alt_Abs_Max'] = np.nan
    
    DataDF.loc[DataDF.pH_Opt_Min < 0, 'pH_Opt_Min'] = np.nan
    DataDF.loc[DataDF.pH_Opt_Min > 14, 'pH_Opt_Min'] = np.nan
    DataDF.loc[DataDF.pH_Opt_Max <= 0, 'pH_Opt_Max'] = np.nan
    DataDF.loc[DataDF.pH_Opt_Max > 14, 'pH_Opt_Max'] = np.nan
    DataDF.loc[DataDF.pH_Abs_Min < 0, 'pH_Abs_Min'] = np.nan
    DataDF.loc[DataDF.pH_Abs_Min > 14, 'pH_Abs_Min'] = np.nan
    DataDF.loc[DataDF.pH_Abs_Max <= 0, 'pH_Abs_Max'] = np.nan
    DataDF.loc[DataDF.pH_Abs_Max > 14, 'pH_Abs_Max'] = np.nan
    
    DataDF.loc[DataDF.Cycle_Min < 0, 'Cycle_Min'] = np.nan
    DataDF.loc[DataDF.Cycle_Min > 365, 'Cycle_Min'] = np.nan
    DataDF.loc[DataDF.Cycle_Max <= 0, 'Cycle_Max'] = np.nan
    DataDF.loc[DataDF.Cycle_Max > 365, 'Cycle_Max'] = np.nan
    
    
    # Count number of nan values for each column
    ReplacedValuesDF.loc['2. Gross Error'] = [toi, toa, tai, taa, roi, roa, rai,
                                              raa, aaa, poi, poa, pai, paa, 0, 0,
                                              0, 0, 0, 0, ci, ca]
    
    return( DataDF, ReplacedValuesDF )



def Check03_maxminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for instances when maximum is less than
    minimum for an attribute, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # Count number of occurrences of swapped min and max attributes
    a=DataDF['Temp_Opt_Min'].loc[DataDF['Temp_Opt_Min'] > DataDF['Temp_Opt_Max']].count()

    e=DataDF['Temp_Abs_Min'].loc[DataDF['Temp_Abs_Min'] > DataDF['Temp_Abs_Max']].count()
    
    i=DataDF['Rain_Opt_Min'].loc[DataDF['Rain_Opt_Min'] > DataDF['Rain_Opt_Max']].count()

    m=DataDF['Rain_Abs_Min'].loc[DataDF['Rain_Abs_Min'] > DataDF['Rain_Abs_Max']].count()
    
    s=DataDF['pH_Opt_Min'].loc[DataDF['pH_Opt_Min'] > DataDF['pH_Opt_Max']].count()

    w=DataDF['pH_Abs_Min'].loc[DataDF['pH_Abs_Min'] > DataDF['pH_Abs_Max']].count()
    
    aa=DataDF['Cycle_Min'].loc[DataDF['Cycle_Min'] > DataDF['Cycle_Max']].count()

    # Make series of times min and max attributes are swapped and swap them 
    # in the df

    bb = DataDF['Temp_Opt_Min'] > DataDF['Temp_Opt_Max']
    ee = DataDF['Temp_Abs_Min'] > DataDF['Temp_Abs_Max']
    ii = DataDF['Rain_Opt_Min'] > DataDF['Rain_Opt_Max']
    mm = DataDF['Rain_Abs_Min'] > DataDF['Rain_Abs_Max']
    ss = DataDF['pH_Opt_Min'] > DataDF['pH_Opt_Max']
    ww = DataDF['pH_Abs_Min'] > DataDF['pH_Abs_Max']
    aaaa = DataDF['Cycle_Min'] > DataDF['Cycle_Max']
    
    DataDF.loc[bb, ['Temp_Opt_Min', 'Temp_Opt_Max']] = DataDF.loc[bb, ['Temp_Opt_Max', 'Temp_Opt_Min']].values
    DataDF.loc[ee, ['Temp_Abs_Min', 'Temp_Abs_Max']] = DataDF.loc[ee, ['Temp_Abs_Max', 'Temp_Abs_Min']].values
    DataDF.loc[ii, ['Rain_Opt_Min', 'Rain_Opt_Max']] = DataDF.loc[ii, ['Rain_Opt_Max', 'Rain_Opt_Min']].values
    DataDF.loc[mm, ['Rain_Abs_Min', 'Rain_Abs_Max']] = DataDF.loc[mm, ['Rain_Abs_Max', 'Rain_Abs_Min']].values
    DataDF.loc[ss, ['pH_Opt_Min', 'pH_Opt_Max']] = DataDF.loc[ss, ['pH_Opt_Max', 'pH_Opt_Min']].values
    DataDF.loc[ww, ['pH_Abs_Min', 'pH_Abs_Max']] = DataDF.loc[ww, ['pH_Abs_Max', 'pH_Abs_Min']].values
    DataDF.loc[aaaa, ['Cycle_Min', 'Cycle_Max']] = DataDF.loc[aaaa, ['Cycle_Max', 'Cycle_Min']].values


    # Count number of swapped values for both columns and set third row as  
    # equal that number
    
    ReplacedValuesDF.loc['3. Swapped'] = [a, a, e, e, i, i, m, m, 0, s, s, w, w,
                                          0, 0, 0, 0, 0, 0, aa, aa]

    return( DataDF, ReplacedValuesDF )





# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "cropbasics_scrape.csv"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    InitialDF = DataDF.copy()
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_maxminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    # Drop rows with na values
    DataDF = DataDF.dropna()
    
    # Write output files
    DataDF.to_csv('ecocrop_cleaned.csv', header=True, index=True)
    ReplacedValuesDF.to_csv('ecocrop_dropped_values.txt', sep='\t', header=True, index=True)
    
    
    # Plot histogram of initial and corrected min opt rainfall
    fig = plt.figure()
    a = plt.hist(InitialDF['Rain_Opt_Min'], bins=10, color='b')
    b = plt.hist(DataDF['Rain_Opt_Min'], bins=10, color='r')
    plt.title('Initial and Corrected Minimum Optimal Rainfall (mm)')  # Title
    plt.xlabel('Annual Rainfall (mm)')  # X axis label
    plt.ylabel('Number of Records')  # Y axis label
    fig.savefig('Temp_Opt_Rainfall_Comparison.png')  # Save figure to file as image
    plt.show()
    
    # Plot box plots of initial and corrected maximum growing periods
    fig, ax = plt.subplots(1,2)
    fig.suptitle('Maximum Growing Cycle (Days)')
    ax[0].boxplot(InitialDF['Cycle_Max'])  # Set initial box plot
    ax[1].boxplot(DataDF['Cycle_Max'])  # Set corrected box plot
    ax[0].set_xlabel('Initial Cycle')
    ax[1].set_xlabel('Corrected Cycle')
    ax[0].set_ylabel('Days')
    fig.savefig('Max_Cycle_Comparison.png')  # Save figure
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    