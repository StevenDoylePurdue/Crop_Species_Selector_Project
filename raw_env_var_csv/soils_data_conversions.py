#!/bin/env python
"""
Program: Soils Data Conversions
Programmer: Steven Doyle
Date: 04.28.2021

This script reads in the soil info file (SU_Info.csv), checks its data quality, and selects
relevant attributes for mapping to the checked soils join csv.  It then reads in the checked
soils join csv, maps the attributes to the soil names, and saves a new csv file of the joined
soils with attribute values instead of soil names.

"""

import pandas as pd


def process_ref(soil_ref):
    """
    This function takes the raw soils reference dataframe, conducts a quality check converting any
    illogical values to na and dropping columns that are not relevant. It returns the processed ref
    dataframe.
    """
    soil_ref = soil_ref.replace('-1', '0')  # -1 is used for na values, replace it with 0 for statistical uses

    soil_ref = soil_ref[['type', 'sand % topsoil', 'silt % topsoil', 'clay % topsoil', 'OC % topsoil',
                        'C/N topsoil']].copy()  # These are the relevant columns


    soil_ref = soil_ref[soil_ref['type'].map(len) < 3]  # Drop rows for soil type variants which are listed with > 2 chars

    return (soil_ref)


def process_join(soil_join):
    """
    This function takes the soils join dataframe, conducts a quality check converting any
    incorrect soil codes to their correct versions, dropping irrelevant columns, and returning the df.
    """

    soil_join['FAOSOIL'] = soil_join['FAOSOIL'].replace(['WAT', 'WATER', 'SALT', 'D/SS', 'ROCK'],
                                                        ['WR', 'WR', 'SA', 'DS', 'RK'])  # Fixing discrepancies in soil codes

    soil_join = soil_join.drop('grid_code', axis=1)  # Dropping unneeded column

    soil_join['Soil_Code'] = soil_join['FAOSOIL'].str.slice(0,2)  # Trim extra characters

    soil_join['Soil_Code'] = soil_join['Soil_Code'].str.replace('[^a-zA-Z]', '', regex=True)  # Cut all non alphabetical

    soil_join['Soil_Code'] = soil_join['Soil_Code'].str.upper()  # Convert to uppercase

    soil_join = soil_join.drop('FAOSOIL', axis=1)  # Dropping unneeded column

    return  soil_join


def merge_soils(soil_join, soil_ref):
    """
    This function takes the soils join dataframe and the soil ref dataframe and maps the soil ref
    attributes and returns a dataframe where the soil code is replaced by the soil variables.
    """

    # Convert soil_ref attribute columns to dictionaries with the soil code as key and attribute as value
    soil_ref.set_index('type', inplace=True)  # Convert soil type to index to become the dict key
    sand_dict = soil_ref['sand % topsoil'].to_dict()  # Convert each column to dict
    silt_dict = soil_ref['silt % topsoil'].to_dict()
    clay_dict = soil_ref['clay % topsoil'].to_dict()
    oc_dict = soil_ref['OC % topsoil'].to_dict()
    cn_dict = soil_ref['C/N topsoil'].to_dict()

    soil_join['Sand'] = soil_join['Soil_Code'].map(sand_dict)  # Map each column using the index and the soil code
    soil_join['Silt'] = soil_join['Soil_Code'].map(silt_dict)
    soil_join['Clay'] = soil_join['Soil_Code'].map(clay_dict)
    soil_join['OC'] = soil_join['Soil_Code'].map(oc_dict)
    soil_join['CN'] = soil_join['Soil_Code'].map(cn_dict)

    soil_join = soil_join.drop('Soil_Code', axis=1)  # Drop the soil code because it is no longer needed

    return soil_join


def consolidate(soil_df):
    """
    This function takes the soil df dataframe, creates a new dataframe out of the subnational jurisdiction
    code unique values, and takes the average of each attribute for each jurisdiction value. It maps them
    and returns a consolidated dataframe with average soil attribute values for each location.
    """

    # Create new df from unique subnational values

    datadf = pd.DataFrame(0, index = soil_df['GID_1'].unique(), columns=soil_df.columns)


    # Create means for each variable
    for name in datadf.index:  # Loop through each unique subnational name
        g0 = soil_df.loc[soil_df['GID_1'] == name, 'GID_0'].to_list()[0]  # All these values will be the same
        n0 = soil_df.loc[soil_df['GID_1'] == name, 'NAME_0'].to_list()[0]
        g1 = soil_df.loc[soil_df['GID_1'] == name, 'GID_1'].to_list()[0]
        n1 = soil_df.loc[soil_df['GID_1'] == name, 'NAME_1'].to_list()[0]
        en = soil_df.loc[soil_df['GID_1'] == name, 'ENGTYPE_1'].to_list()[0]
        sa = soil_df.loc[soil_df['GID_1'] == name, 'Sand'].mean()  # Use mean for float columns
        si = soil_df.loc[soil_df['GID_1'] == name, 'Silt'].mean()
        cl = soil_df.loc[soil_df['GID_1'] == name, 'Clay'].mean()
        oc = soil_df.loc[soil_df['GID_1'] == name, 'OC'].mean()
        cn = soil_df.loc[soil_df['GID_1'] == name, 'CN'].mean()
        datadf.loc[name] = [g0, n0, g1, n1, en, sa, si, cl, oc, cn]

    datadf = datadf.drop('GID_1', axis=1)  # Drop duplicate column

    datadf = datadf.fillna(0)

    return datadf



if __name__ == '__main__':

    # Prepare soil reference df for attribute mapping
    soil_ref = pd.read_csv('SU_Info.csv', header=0)
    soil_ref = process_ref(soil_ref)  # Process soil reference df

    # Prepare checked soils join csv for attribute mapping
    soil_join = pd.read_csv('checked_soils_join.csv', header=0)
    soil_join = process_join(soil_join)  # Process soil join df

    # Map attributes to soils join df
    soil_df = merge_soils(soil_join,soil_ref)  # Transfer attributes to soil join and make new df

    # Consolidate the subnational jurisdictions by averaging all values within them
    final_soil = consolidate(soil_df)

    final_soil.to_csv('processed_soil.csv', header=True, index=True)
