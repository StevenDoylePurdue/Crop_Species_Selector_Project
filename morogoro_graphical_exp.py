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
import numpy as np
import seaborn as sns; sns.set()
from sklearn.decomposition import PCA
import plotly.express as px
from sklearn.preprocessing import StandardScaler



if __name__ == '__main__':

    # Initialize total df
    totaldf = pd.read_csv('morogoro_all_data.csv', header=0)
    totaldf = totaldf.set_index('Species', drop=False)

    # Initialize passing df
    pscore = pd.read_csv('morogoro_passing_data.csv', header=0)
    pscore = pscore.set_index('Species', drop=False)

    # Initialize failing df
    fscore = pd.read_csv('morogoro_failing_data.csv', header=0)
    fscore = fscore.set_index('Species', drop=False)

    '''# Count failing variables
    alt = fscore[fscore['Alt'] == 0].shape[0]
    rain = fscore[fscore['Rain'] == 0].shape[0]
    ph = fscore[fscore['pH'] == 0].shape[0]
    tmin = fscore[fscore['Temp_Min'] == 0].shape[0]
    tmax = fscore[fscore['Temp_Max'] == 0].shape[0]
    text = fscore[fscore['Texture'] == 0].shape[0]
    fert = fscore[fscore['Fertility'] == 0].shape[0]
    cycle = fscore[fscore['Cycle'] == 0].shape[0]
    labels = ['Alt', 'Precip', 'pH', 'Min Temp', 'Max Temp',
              'Texture', 'Fertility', 'Growing Period']
    vars = [alt, rain, ph, tmin, tmax, text, fert, cycle]
    fig = plt.figure(dpi=96)
    plt.rcParams['figure.figsize'] = (20, 30)
    plt.rcParams['font.size'] = '28'
    plt.bar(labels, vars)
    plt.title('Causes of Plant Growth Failure')  # Title
    plt.xlabel('Variable')  # X axis label
    plt.ylabel('Number of Occurrences')  # Y axis label
    plt.xticks(labels, size=8)
    fig.savefig('Fail_Bar.png')  # Save figure to file as image
    plt.show()'''

    # PCA
    df = totaldf[['Temp_Abs_Min', 'Temp_Abs_Max', 'Rain_Abs_Min', 'Rain_Abs_Max', 'Alt_Abs_Max',
                 'pH_Abs_Min', 'pH_Abs_Max', 'Cycle_Min', 'Cycle_Max', 'Growth']].copy()

    '''pca = PCA().fit(df)
    fig = plt.figure(dpi=96)
    plt.rcParams['figure.figsize'] = (20, 15)
    plt.rcParams['font.size'] = '28'
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Principal Component Fitting')  # Title
    fig.savefig('pca_fit.png')  # Save figure to file as image
    plt.show()'''


    features = ['Temp_Abs_Min', 'Temp_Abs_Max', 'Rain_Abs_Min', 'Rain_Abs_Max', 'Alt_Abs_Max',
                 'pH_Abs_Min', 'pH_Abs_Max', 'Cycle_Min', 'Cycle_Max']

    scaler = StandardScaler()
    scaler.fit(df)
    scaled_data = scaler.transform(df)
    pca = PCA(n_components=2)
    pca.fit(scaled_data)
    x_pca = pca.transform(scaled_data)

    plt.figure()
    #plt.rcParams['figure.figsize'] = (20, 15)
    #plt.rcParams['font.size'] = '28'
    targets = df['Growth'].values
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=targets, cmap='rainbow')
    plt.xlabel('First principal component')
    plt.ylabel('Second Principal Component')
    plt.title('Principal Component Analysis of Plant Variables')  # Title
    plt.show()
    plt.savefig('pca_scatter.png')
