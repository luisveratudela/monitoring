# -*- coding: utf-8 -*-
'''
Plots numerical results
'''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def linear(df, x, y, ci=None):

    '''
    df: DataFrame with numerical values
    x: string of column names to use in x-axis
    y: string of column names to use in x-axis
    ci: confidence interval around regression line
    '''

    f, ax = plt.subplots(figsize=(10,10))

    if ci==None:
        ax = sns.regplot(x=x, y=y, data=df, marker='.')
        
    else:
        ax = sns.regplot(x=x, y=y, data=df, marker='.', ci=ci)

    plt.show()


def pairwise(df, names=None, category=None):
    '''
    df: DataFrame with numerical columns to explore pairwise
    names = list of columns to investigate, including category if used
    category: optional string, column name that serves to classify results
    '''

    if names !=None: 
        df = df[names]
 
    df = df.dropna()
    
    if category == None: 
        ax = sns.pairplot(df, markers='.')
    else:
        ax = sns.pairplot(df, hue=category, markers='.')
    
    plt.show()

def violin(df, x, bins, labels, y, category=None): 

    '''
    df: DataFrame with columns to investigate
    x: string, column name with data to bin 
    bins: list of limits to bin column x1 (nr of bins + 1)
    labels: list of labels to bin to use as categories   
    y: string, column name with numerical values
    category: optional string, column name with second category
    '''

    assert ( len(bins) == len(labels) + 1 ),'wrong nr. of bins and labels' 

    df['bins'] = pd.cut(df[x], bins=bins, labels=labels)

    f, ax = plt.subplots(figsize=(12,8))

    if category == None:  
        
        sns.violinplot(x='bins', y=y, data=df, order=labels)
    
    else: 
    
        sns.violinplot(x='bins', y=y, data=df, hue=category, order=labels)

    plt.show()

def distribution(df, names=None):

    '''
    df: DataFrame with columns to plot
    names = list of columns to investigate
    '''
    
    if names !=None: 
        df = df[names]

    df = df.dropna()
    
    f, ax = plt.subplots(figsize=(10,10))
    
    for col in df.columns:
        ax = sns.distplot(df[col], bins=20, norm_hist=True, kde=True, label=col)
    
    ax.set(xlabel='Value', ylabel='Probability density [-]')
    
    plt.legend()
    
    plt.show()

def heatmap(data, xnames, ynames):

    '''
    data: 2D numpy array with numerical data
    xnames: list of names for x-axis
    ynames: list of names for y-axis
    '''

    (r, c) = np.shape(data)

    assert (len(xnames) == r) & (len(ynames) == c), 'check data & names'

    df = pd.DataFrame(data, index=xnames, columns=ynames)

    sns.heatmap(df, annot=True)
    plt.show()

