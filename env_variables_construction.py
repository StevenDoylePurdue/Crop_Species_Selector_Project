#!/bin/env python
"""
Program: Environmental Variables Construction
Programmer: Steven Doyle
Date: 04.29.2021

This script reads in the processed environmental attributes csvs, merges them together, and transforms
them into eco-crop compatible variables.

"""

import pandas as pd


def drop_nas(df):
    '''
    This function takes in the master df, records the number of na values per variable into a txt file,
    and drops them before returning the df.
    '''

    col_names = df.columns.to_list()  # Get column names

    nadf = pd.DataFrame(0, index=['Missing Values'], columns=col_names[5:])  # Make a new df with variables as columns

    td = df['temp_difference'].isna().sum()  # Find the sum of na values for each variable
    dst = df['dry_season_type'].isna().sum()
    el = df['elevation'].isna().sum()
    gp = df['growing_period'].isna().sum()
    pc = df['precipitation'].isna().sum()
    wt = df['wet_temp'].isna().sum()
    sa = df['Sand'].isna().sum()
    si = df['Silt'].isna().sum()
    cl = df['Clay'].isna().sum()
    oc = df['OC'].isna().sum()
    cn = df['CN'].isna().sum()
    ph = df['pH'].isna().sum()
    tt = df.isna().sum().sum()

    nadf.loc['Missing Values'] = [td, dst, el, gp, pc, wt, sa, si, cl, oc, cn, ph]  # Add these to the new df
    nadf['Total'] = tt  # Add a column for total na values
    nadf.to_csv('missing_values.txt', sep='\t', index=True, header=True)  # Save as a txt file

    df = df.dropna()  # Drop rows with na values

    return df


def temps(df):
    '''
    This function reads in the df and creates a max temp and min temp column by dividing the temp diff
    by two and adding it to or subtracting it from the wet temp respectively. It then drops the temp
    diff and wet temp columns and returns the df.
    '''

    # The minimum temperature is the mean temperature minus half the difference between max and min
    df['Temp_Min'] = df['wet_temp'] - df['temp_difference']/2
    df['Temp_Max'] = df['wet_temp'] + df['temp_difference']/2

    df = df.drop(columns=['wet_temp', 'temp_difference'], axis=1)  # Drop these columns as they are no longer useful

    return df


def textures(df, row):
    '''
    This function reads in the df and uses the sand, silt, clay, and organic carbon columns to determine
    the texture class of the soil using accepted classification methods. It adds the class as a column,
    deletes the used ones, and returns the df.
    '''

    if df['OC'][row] >= 5:  # If soil has at least 5% organic carbon, it's organic regardless of anything else
        texture = 'organic'
    else:  # If not organic, texture is the dominant particle size
        if df['Sand'][row] > df['Silt'][row] and df['Sand'][row] > df['Clay'][row]:
            texture = 'light'
        elif df['Silt'][row] > df['Sand'][row] and df['Silt'][row] > df['Clay'][row]:
            texture = 'medium'
        elif df['Clay'][row] > df['Sand'][row] and df['Clay'][row] > df['Silt'][row]:
            texture = 'heavy'
        else:  # If no clear dominator exists, the texture is considered wide
            texture = 'wide'

    return texture


def fert(df, row):
    '''
    This function takes in a C:N ratio and returns a string stating the degree of fertility in the soil.
    '''

    if df['CN'][row] > 16:  # Low fertility
        fertility = 'low'
    elif df['CN'][row] < 9:  # High fertility
        fertility = 'high'
    else:
        fertility = 'moderate'  # Moderate


    return fertility


def seasons(df, row):
    '''
    This function takes in the growing period and dry season type categories and determines the length
    of the longest growing season for that location. It returns this value.
    '''

    season = df['dry_season_type'][row].round()  # Round to category number
    if season == 0:  # Dry season frequency multiplier
        mult = 0
    elif season == 1:
        mult = 1/4
    elif season == 4:
        mult = 1/2
    else:
        mult = 1

    gdd = df['growing_period'][row].round()
    if gdd == 0:  # Total number of productive days per year category
        days = 0
    elif gdd == 1:
        days = 0
    elif gdd == 2:
        days = 29
    elif gdd == 3:
        days = 59
    elif gdd == 4:
        days = 89
    elif gdd == 5:
        days = 119
    elif gdd == 6:
        days = 149
    elif gdd == 7:
        days = 179
    elif gdd == 8:
        days = 209
    elif gdd == 9:
        days = 239
    elif gdd == 10:
        days = 269
    elif gdd == 11:
        days = 299
    elif gdd == 12:
        days = 329
    elif gdd == 13:
        days = 364
    else:
        days = 365

    length = days * mult  # Length of growing season is a product of days and dry season frequency

    return length



if __name__ == '__main__':

    # Create variables df using the diurnal csv as the frame

    df = pd.read_csv('processed_env_files/processed_diurnal.csv', header=0)
    df = df.set_index('GID_1', drop=False)


    # Map variables from other csvs to the variables df

    file_list = ['dry_seasons', 'el', 'growing_period', 'precip', 'wet_temp']  # File list
    var_list = ['dry_season_type', 'elevation', 'growing_period', 'precipitation', 'wet_temp']  # Variable name list

    for i in range(0,5):  # Loop for each of the above files and variables
        var_df = pd.read_csv('processed_env_files/processed_{}.csv'.format(file_list[i]), header=0, index_col='GID_1')
        var = var_list[i]
        df[var] = df.index.map(var_df[var])  # Map the variables to the master list via their common index

    soil_list = ['Sand', 'Silt', 'Clay', 'OC', 'CN', 'pH']  # Variable names
    soil_df = pd.read_csv('processed_env_files/processed_soil.csv', header=0, index_col='GID_1')
    for i in range(0,6):
        var = soil_list[i]
        df[var] = df.index.map(soil_df[var])  # Map the variables to the master list via their common index


    df = df[['GID_1', 'NAME_1', 'ENGTYPE_1', 'GID_0', 'NAME_0', 'temp_difference', 'dry_season_type',
             'elevation', 'growing_period', 'precipitation', 'wet_temp', 'Sand', 'Silt', 'Clay', 'OC', 'CN', 'pH']]


    # Remove locations that do not have information for the full suite of variables

    df = drop_nas(df)


    # Format variable columns so they are compatible with the ecocrop variables

    df = temps(df)  # Calc min and max temp for growing season (rainy season)
    df = df.rename(columns={'precipitation':'Rain', 'elevation':'Alt'})  # Rename columns to match ecocrop
    df['Texture'] = ''  # Make an empty column for texture
    for row in range(0,len(df)):  # loop the texture calculator for each row
        texture = textures(df, row)
        df['Texture'][row] = texture
    df = df.drop(columns=['OC', 'Sand', 'Silt', 'Clay'], axis=1)  # Drop unnecessary columns
    df['Fertility'] = ''
    for row in range(0, len(df)):  # Convert C:N ratio to Fertility
        fertility = fert(df, row)
        df['Fertility'][row] = fertility
    df = df.drop(columns='CN', axis=1)
    df['Cycle'] = ''
    for row in range(0, len(df)):
        days = seasons(df, row)
        df['Cycle'][row] = days
    df = df.drop(columns=['dry_season_type', 'growing_period'], axis=1)

    df = df.rename(columns={'GID_1':'State_Code', 'NAME_1':'State_Name', 'ENGTYPE_1':'State_Type',
                            'GID_0':'Country_Code', 'NAME_0':'Country_Name'})  # Rename columns to be more intelligible
    df.to_csv('processed_env_files/env_var.csv', header=True, index=False)
