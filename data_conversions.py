#!/bin/env python
"""
Program: Non-Soils Data Conversions
Programmer: Steven Doyle
Date: 04.28.2021

This script reads in the environmental attributes csvs and consolidates each one by taking the average of each
subnational jurisdiction's attributes and converting them into a new dataframe.

"""

import pandas as pd


def consolidate(df, variable):
    """
    This function takes the soil df dataframe, creates a new dataframe out of the subnational jurisdiction
    code unique values, and takes the average of each attribute for each jurisdiction value. It maps them
    and returns a consolidated dataframe with average soil attribute values for each location.
    """

    # Create new df from unique subnational values

    datadf = pd.DataFrame(0, index = df['GID_1'].unique(), columns=df.columns)

    ticker = 1
    # Create means for each variable
    for name in datadf.index:  # Loop through each unique subnational name
        g0 = df.loc[df['GID_1'] == name, 'GID_0'].to_list()[0]  # All these values will be the same

        n0 = df.loc[df['GID_1'] == name, 'NAME_0'].to_list()[0]

        g1 = df.loc[df['GID_1'] == name, 'GID_1'].to_list()[0]

        n1 = df.loc[df['GID_1'] == name, 'NAME_1'].to_list()[0]

        en = df.loc[df['GID_1'] == name, 'ENGTYPE_1'].to_list()[0]

        var = df.loc[df['GID_1'] == name, 'grid_code'].mean()  # Use mean for float columns

        datadf.loc[name] = [g0, n0, g1, n1, en, var]
        print('row', ticker)
        ticker+=1

    datadf.rename(columns={'grid_code': variable}, inplace=True)


    datadf = datadf.fillna(0)

    return datadf



if __name__ == '__main__':

    file_list = ['diurnal', 'dry_seasons', 'precip', 'el', 'growing_period', 'wet_temp']

    variable_names = ['temp_difference', 'dry_season_type', 'elevation', 'growing_period', 'growing_temp']

    # Consolidate the subnational jurisdictions by averaging all values within them
    for i in range(0,5):
        df = pd.read_csv('raw_env_var_csv/checked_{}_join.csv'.format(file_list[i]))
        print('csv {} red'.format(i))
        consoldf = consolidate(df, variable_names[i])
        print('csv {} consolidated'.format(i))
        consoldf.to_csv('processed_env_files/processed_{}.csv'.format(file_list[i]), header=True, index=True)




