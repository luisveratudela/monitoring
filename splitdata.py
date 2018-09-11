# -*- coding: utf-8 -*-
'''
functions that create training and test DataFrames or various sets in dict

by lvt, September 2017
'''

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def consecutive(df, date=None):
    '''
    df: dataframe to be divided into two consecutive sets before and after date
    date: string with format YYYY-MM-DD, last one included in training set
    '''

    if date == None: 
        
        train, test = None, df
    
    else:
        
        train = df.loc[ : date ] 

        test = df.iloc[ len(train.index) : ]

    return train, test

def holdout(df, fraction=0.3):
    '''
    df: dataframe to be divided into two consecutive sets based on fraction
    fraction: (approximately) used to form the training set
    '''

    train, test = train_test_split(df, test_size=fraction)
    
    return train, test

def crossfold(df, k=10):
    '''
    df: dataframe to be divided into k consecutive sets
    k: integer used to divide df into (approximately equal) k sets
    '''
    
    for s in range(k):
    
        sets[s] = df

    return sets
