# -*- coding: utf-8 -*-
'''
functions that perform imputation on missing data

by lvt, September 2017
'''

import numpy as np
import pandas as pd

def allindex(df, freq='10min'):
    '''
    df: DataFrame with missing data and datetime to be reindexed
    freq: frequency for adding rows of missing data
    '''
    
    start, end = df.index[0], df.index[-1]
    
    date_index = pd.date_range(start, end, freq=freq)
    
    df2 = df.reindex(date_index)
    
    return df2

def impute(df, style='interpolate', patience=9999):
    
    '''
    df: DataFrame with NaNs
    style: string to indicate type of imputation
    patience: times to consecutively repeat online procedure
    '''
    
    if style == 'median':
        df2 = df.fillna(df.median())
    
    elif style == 'interpolate':
        df2 = df.fillna(df.interpolate('linear')) # check 'time'
    
    elif style == 'hotdeck': # still to develop (assert)
        print('hotdeck is not ready yet')

    elif style == 'forward': # still to develop (assert)
        df2 = df.fillna(method='ffill', limit=patience)
    
    else: 
        raise ValueError('unknown style')
    
    assert df2.isnull().sum().sum() == 0, 'there are NaN left'
    
    return df2
