#!/bin/env python
"""
Program: Cultivation Function
Programmer: Steven Doyle
Date: 04.29.2021

This script displays the function used to determine whether or not a plant can be grown in a given environment and
the factors relating to its success.

"""

import pandas as pd

def cultivation(plantrow, staterow):
    '''
    This function reads in the named plant's attribute row from the plant dataframe and the state's attributes row
    from the state dataframe. It compares the plant's required conditions with the state's environmental conditions
    and determines if and to what degree of success the plant can be grown. If any values are found to be outside of
    the plant's absolute boundary values, the plant cannot be grown. If the majority of the values are outside of the
    plant's optimal boundaries, it can be grown marginally. If the majority of the values are within the plant's
    optimal values, it can be grown moderately. If the all of the values are within the plant's optimal values, it can
    be grown successfully. The function returns both the plant and state values, as well as a numerical score from 0 to
    3, with 0 being impossible and 3 being successful.

    '''

    # For each variable, check to see if plant var abs is outside of env var and assign 0 if it is
    # If within plant var abs but below plant var opt, assign 1
    # If within plant var opt, assign 2

    # Altitude
    if plantrow['Alt_Abs_Max'] < staterow['Alt']:
        alt = 0
    else:
        alt = 2


    # Rainfall
    if plantrow['Rain_Abs_Min'] > staterow['Rain'] or plantrow['Rain_Abs_Max'] < staterow['Rain']:
        rain = 0
    elif plantrow['Rain_Abs_Min'] < staterow['Rain'] and plantrow['Rain_Opt_Min'] > staterow['Rain']:
        rain = 1
    elif plantrow['Rain_Abs_Max'] > staterow['Rain'] and plantrow['Rain_Opt_Max'] < staterow['Rain']:
        rain = 1
    else:
        rain = 2

    # pH
    if plantrow['pH_Abs_Min'] > staterow['pH'] or plantrow['pH_Abs_Max'] < staterow['pH']:
        ph = 0
    elif plantrow['pH_Abs_Min'] < staterow['pH'] and plantrow['pH_Opt_Min'] > staterow['pH']:
        ph = 1
    elif plantrow['pH_Abs_Max'] > staterow['pH'] and plantrow['pH_Opt_Max'] < staterow['pH']:
        ph = 1
    else:
        ph = 2


    # Minimum Temperature
    if plantrow['Temp_Abs_Min'] > staterow['Temp_Min']:
        tmin = 0
    elif plantrow['Temp_Abs_Min'] < staterow['Temp_Min'] and plantrow['Temp_Opt_Min'] > staterow['Temp_Min']:
        tmin = 1
    else:
        tmin = 2

    # Maximum Temperature
    if plantrow['Temp_Abs_Max'] < staterow['Temp_Max']:
        tmax = 0
    elif plantrow['Temp_Abs_Max'] > staterow['Temp_Max'] and plantrow['Temp_Opt_Max'] < staterow['Temp_Max']:
        tmax = 1
    else:
        tmax = 2


    # Texture
    abstext = plantrow['Texture_Abs'].split(', ')
    opttext = plantrow['Texture_Opt'].split(', ')
    if staterow['Texture'] in abstext:
        if staterow['Texture'] in opttext:
            text = 2
        else:
            text = 1
    else:
        text = 0


    # Fertility
    fertdict = {'high':3, 'moderate':2, 'low':1}
    abs = fertdict[plantrow['Fertility_Abs']]
    opt = fertdict[plantrow['Fertility_Opt']]
    env = fertdict[staterow['Fertility']]

    if env < abs:
        fert = 0
    elif env >= abs and env < opt:
        fert = 1
    elif env >= opt:
        fert = 2


    # Cycle
    if staterow['Cycle'] >= plantrow['Cycle_Min'] and staterow['Cycle'] <= plantrow['Cycle_Max']:
        cycle = 2
    else:
        cycle = 0


    # Check if 0 is present, if so, assign 0 to growth

    val_list = [alt, rain, ph, tmin, tmax, text, fert ,cycle]
    if 0 in val_list:
        growth = 0
    # If mean == 1, assign 1 to growth
    elif sum(val_list)/len(val_list) == 1:
        growth = 1
    # If 0 is not present and 2 > mean > 1, assign 2 to growth
    elif 0 not in val_list and sum(val_list)/len(val_list) < 2 and sum(val_list)/len(val_list) > 1:
        growth = 2
    # If mean == 2, assign 3 to growth
    elif sum(val_list)/len(val_list) == 2:
        growth = 3

    # make list with plant name, state name, country name, env var scores, and growth score

    row = [staterow['State_Code'], staterow['State_Name'], staterow['State_Type'], staterow['Country_Code'],
           staterow['Country_Name'], plantrow['Species'], alt, rain, ph, tmin, tmax, text, fert, cycle,
           growth]

    return row



if __name__ == '__main__':

    # Initialize dataframes
    plants = pd.read_csv('ecocrop_files/ecocrop_cleaned.csv', header = 0)
    plants = plants.set_index('Species', drop=False)
    states = pd.read_csv('processed_env_files/env_var.csv', header= 0)
    states = states.set_index('State_Code', drop=False)

    # Choose State
    staterow = states.loc['TZA.14_1']

    # Initialize results df
    cols= ['State_Code', 'State_Name', 'State_Type',
               'Country_Code', 'Country_Name', 'Species',
               'Alt', 'Rain', 'pH', 'Temp_Min', 'Temp_Max', 'Texture', 'Fertility', 'Cycle', 'Growth']
    resdf = pd.DataFrame(columns=cols)


    for name in plants.index:
        plantrow = plants.loc[name]
        results = cultivation(plantrow, staterow)
        res_ser = pd.Series(results, index=resdf.columns, name=name)
        resdf = resdf.append(res_ser)
    resdf.to_csv('{}_{}_{}_scores.csv'.format(staterow['State_Name'],staterow['State_Type'],
                                              staterow['Country_Name']), header=True, index=False)







