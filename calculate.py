# -*- coding: utf-8 -*-
'''
functions that calculate something

by lvt, September 2017
'''

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import r2_score as R2

def accumulated(df, m):

    '''
    df: DataFrame with 10-min-dels to calculate accumulated del value
    '''

    assert (m != 4) | (m != 10), 'Whoeler value, either 4 or 10'

    for load in df.columns:
        df[ 'acc_' + load ] = ( df [load] **m ).cumsum() ** 1/m

    return df

def metrics(measured, estimated, name='test'):

    '''
    measured, estimated: numpy 1D array of NORMALISED records
    name: string naming the test ran
    '''

    mae = MAE(estimated, measured)
    mse = MSE(estimated, measured)
    root_mse = np.sqrt(mse)
    relative_mse = MSE(estimated, measured, sample_weight=1/(estimated.flatten()**2))
    r2 = R2(estimated, measured)
    re = ( ( (estimated+1) - (measured+1) ) / (measured+1) ) * 100

    vals = [mae, mse, root_mse, relative_mse, r2, re.mean(), re.std(), 3*re.std()]
    cols = ['mae [-]', 'mse [-]', 'root_mse [-]', 'relative_mse [-]', 'r2 [-]', 're_avg ', 're_std', 'TL']

    df = pd.DataFrame([vals], columns=cols, index=[name])

    return df
