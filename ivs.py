# -*- coding: utf-8 -*-
'''
select predictors from DataFrame with inputs, flags and targets as columns

by lvt, August 2017
'''

import numpy as np
import pandas as pd

def pfilter(df, target_names, flag_names=None, kmin=0.5, kmax=0.95):

    '''
    df: DataFrame with all records: inputs, targets & unwanted flags
    target_names: list of column names (strings) containing targets (y)
    flag_names: list of column names (strings) containing unwanted flags (z)
    klow: keep inputs with correlation coeff. to targets above kmin
    kmax: keep inputs with correlation coeff. to inputs below kmax
    '''

    assert set(target_names) < set(df.columns), 'target name not found'

    # DataFrames: target, flags and inputs
    targets = df[target_names] 

    if flag_names !=None:

        assert set(flag_names) < set(df.columns), 'flag name not found'

        flags = df[flag_names]
    
        inputs = df.drop( target_names + flag_names, axis=1 )
    
    else: 
        inputs = df.drop( target_names, axis=1 )

    # name of inputs as list
    input_names = list( inputs.columns )

    # DataFrame for analysis
    data = pd.merge( inputs, targets,
                    left_index=True, right_index=True, how='outer' )

    # all pearson coefficients
    corr_matrix = data.corr()

    # empty dicts for selection per target
    ranking, candidates, predictors = {}, {}, {}

    # identify candidates with high correlation to target
    for load in target_names:
    
        # pearson coeff., inputs-to-load
        corr_targets = corr_matrix[load][:-len(target_names)]

        # sort series of pearson coeff. ascending (remove nan)
        ranking[load] = corr_targets.sort_values(axis=0, ascending=True,
                                           inplace=False, na_position='last')
    
        # and keep only values above thredhold
        ranking[load] = ranking[load].loc[ ranking[load] > kmin ]

        # candidates as list
        candidates[load] = list( ranking[load].index )

    # highly correlated inputs   
    for load in target_names:
    
        # pearson coeff., inputs-to-inputs
        corr_inputs = data.loc[ :,candidates[load] ].corr()

        # empty list to remove
        to_remove = []

        # starting with lower relation to target
        for candidate in candidates[load]:
    
            # list its peers (highly correlated to target)
            peers = list( corr_inputs[candidate].loc[corr_inputs[candidate] >=
                            kmax].drop(candidate).index )
    
            # identify better peers, not yet listed to remove
            better_peers = list( set(peers) - set(to_remove) )
    
            # add candidate to remove if it has better peers
            if better_peers: to_remove.append(candidate)

        # assign predictors per load
        predictors[load] = [x for x in candidates[load] if x not in to_remove]

    return ranking, predictors
