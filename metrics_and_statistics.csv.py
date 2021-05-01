#!/bin/env python
"""
Program: Cultivation Function
Programmer: Steven Doyle
Date: 04.29.2021

This script produces descriptive statistics for the results of the cultivation function when specifying a single state
as the location variable and all plants as the plant variable.

"""

import pandas as pd
import matplotlib.pyplot as plt

def avg_std(df):
    cols = ['Temp_Abs_Min (C)', 'Temp_Abs_Max (C)', 'Rain_Abs_Min (mm)', 'Rain_Abs_Max (mm)', 'Alt_Abs_Max (m)', 'pH_Abs_Min',
            'pH_Abs_Max', 'Texture_Abs', 'Fertility_Abs', 'Cycle_Min (Days)', 'Cycle_Max (Days)']
    resdf = pd.DataFrame(columns=cols)
    mtmin = df['Temp_Abs_Min'].mean()
    mtmax = df['Temp_Abs_Max'].mean()
    mrmin = df['Rain_Abs_Min'].mean()
    mrmax = df['Rain_Abs_Max'].mean()
    mamax = df['Alt_Abs_Max'].mean()
    mpmin = df['pH_Abs_Min'].mean()
    mpmax = df['pH_Abs_Max'].mean()
    mtabs = df['Texture_Abs'].mode()
    mfabs = df['Fertility_Abs'].mode()
    mcmin = df['Cycle_Min'].mean()
    mcmax = df['Cycle_Max'].mean()

    means = [mtmin,mtmax,mrmin,mrmax,mamax,mpmin,mpmax,mtabs,mfabs,mcmin,mcmax]
    mres_ser = pd.Series(means, index=resdf.columns, name='Mean (Continuous), Mode (Categorical)')
    resdf = resdf.append(mres_ser)

    mtmin = df['Temp_Abs_Min'].std()
    mtmax = df['Temp_Abs_Max'].std()
    mrmin = df['Rain_Abs_Min'].std()
    mrmax = df['Rain_Abs_Max'].std()
    mamax = df['Alt_Abs_Max'].std()
    mpmin = df['pH_Abs_Min'].std()
    mpmax = df['pH_Abs_Max'].std()
    mtabs = 'na'
    mfabs = 'na'
    mcmin = df['Cycle_Min'].std()
    mcmax = df['Cycle_Max'].std()

    stds = [mtmin, mtmax, mrmin, mrmax, mamax, mpmin, mpmax, mtabs, mfabs, mcmin, mcmax]
    sres_ser = pd.Series(stds, index=resdf.columns, name='Standard Deviation')
    resdf = resdf.append(sres_ser)
    resdf.to_csv('morogoro_pass_metrics.csv', header=True, index=True)

    return


if __name__ == '__main__':

    # Initialize scores df
    scoredf = pd.read_csv('Morogoro_Region_Tanzania_scores.csv', header=0)
    scoredf = scoredf.set_index('Species', drop=False)

    # Initialize plant list df
    plantdf = pd.read_csv('ecocrop_files/ecocrop_cleaned.csv', header=0)
    plantdf = plantdf.set_index('Species', drop=False)


    # Merge dfs
    totaldf = scoredf.copy()
    for col in plantdf.columns:
        totaldf[col] = totaldf.index.map(plantdf[col])
    totaldf.to_csv('morogoro_all_data.csv', header=True, index=False)

    # Initialize df of plants that can grow
    passing = totaldf['Growth'] != 0
    pscore = totaldf[passing]
    pscore.to_csv('morogoro_passing_data.csv', header=True, index=False)

    # Initialize df of plants that cannot grow
    failing = totaldf['Growth'] == 0
    fscore = totaldf[failing]
    fscore.to_csv('morogoro_failing_data.csv', header=True, index=False)

    # Get variable means and sds from passing plants
    pscore = pd.read_csv('morogoro_passing_data.csv', header=0)
    pscore = pscore.set_index('Species', drop=False)
    avg_std(pscore)


    '''# Plot Rainfall Min
    fig, ax = plt.subplots(dpi=96)
    plt.rcParams['figure.figsize'] = (20, 15)
    ax.boxplot([pscore['Rain_Abs_Min'],totaldf['Rain_Abs_Min']])
    plt.title('Well-Suited Plants vs All Plants Minimum Rainfall (mm)')  # Title
    plt.xlabel('Morogoro Plants Left, All Plants Right')  # X axis label
    plt.ylabel('Precipitation (mm)')  # Y axis label
    plt.rcParams['font.size'] = '28'
    fig.savefig('Min_Rain_Diff.png')  # Save figure to file as image
    plt.show()'''

    # Plot histogram of altitude
    fig = plt.figure(dpi=96)
    plt.rcParams['figure.figsize'] = (20, 20)
    plt.rcParams['font.size'] = '20'
    plt.hist(pscore['Alt_Abs_Max'], bins=20)
    plt.title('Distribution of Maximum Altitudes (m)')  # Title
    plt.xlabel('Altitude (m)')  # X axis label
    plt.ylabel('Number of Species')  # Y axis label
    fig.savefig('Max_Alt.png')  # Save figure to file as image
    plt.show()



