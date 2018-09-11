# -*- coding: utf-8 -*-
'''
functions that read measurement data into a pandas DataFrame

by lvt, September 2017
'''

import os
import numpy as np
import pandas as pd
import scipy.io as sio
from os import listdir
from os.path import isfile, join, realpath

def baltic_coordinates(f):

    '''
    f: csv-file including coordinates
    '''
  
    coord = pd.read_csv(f, header=0, index_col=0)
    
    coord.drop(['B00'], inplace=True) # removes platform
    
    return coord

def baltic_scada(p):
    
    '''
    p: full path to folder with MCrunch-files from analysis of FAST simulations
    '''
    
    all_files = [f for f in listdir(p) if isfile(join(p, f))]
    
    scada ={}

    for file in all_files:
        
        f = join(p, file)
        
        b = sio.loadmat(f)

        name_flags = [ name[0] for name in b['name_flags'].flatten() ]
        
        name_stats = [ name[0] for name in b['name_statistics'].flatten() ]
        
        names = name_stats + name_flags

        meas = np.concatenate((b['statistics'], b['flags']), axis=1)
    
        t = b['timestamps'].astype(int)
        
        y, m, d, H, M, S  = t[:,0], t[:,1], t[:,2], t[:,3], t[:,4], t[:,5] 
        
        ts = pd.DataFrame({'year': y, 'month': m, 'day': d, 'hour': H,
            'minute': M, 'seconds': S })
    
        timestamps = pd.to_datetime(ts, unit='s')
    
        scada[file[:-4]] = pd.DataFrame(data=meas, index=timestamps, 
            columns=names)
        
    return scada 

def baltic_scada_features(df):

    '''
    df: DataFrame with SCADA data to add features: range and variance
    '''

    # range of variables
    df['range_power_wico'] = \
                    df['max_power_wico'] - df['min_power_wico']
    df['range_reactive_power'] = \
                    df['max_reactive_power'] - df['min_reactive_power']
    df['range_windspeed_sonic'] = \
                    df['max_windspeed_sonic'] - df['min_windspeed_sonic']
    df['range_windspeed_cup'] = \
                    df['max_windspeed_cup'] - df['min_windspeed_cup']
    df['range_azimuth_angle'] = \
                    df['max_azimuth_angle'] - df['min_azimuth_angle']
    df['range_temperature'] = \
                    df['max_temperature'] - df['min_temperature']

    # variance of variables
    df['var_power_wico'] = df['std_power_wico'] ** 2
    df['var_reactive_power'] = df['std_reactive_power'] ** 2
    df['var_windspeed_sonic'] = df['std_windspeed_sonic'] ** 2
    df['var_windspeed_cup'] = df['std_windspeed_cup'] ** 2
    df['var_azimuth_angle'] = df['std_azimuth_angle'] ** 2 
    df['var_temperature'] = df['std_temperature'] ** 2

    # turbulence intensity
    df['TI'] = df['std_windspeed_cup'] / df['mean_windspeed_cup']

    return df

def baltic_campaign(f):

    '''
    f: full path to MAT-file with 10-min Baltic 01 summary of 50Hz records
    '''

    b = sio.loadmat(f)

    meas = np.concatenate((b['statistics'], b['flags'], b['DEL']), axis=1)

    timestamps = [ str(stamp[0]) for stamp in b['timestamps'].flatten() ]

    name_stats = [ name[0] for name in b['name_statistics'].flatten() ]
    
    name_flags = [ name[0] for name in b['name_flags'].flatten() ]
    
    name_dels = [ name[0] for name in b['name_DEL'].flatten() ]
    
    # correct nomenclature
    name_dels = [n.replace('in_plane', 'edgewise') for n in name_dels]
    
    name_dels = [n.replace('out_of_plane', 'flapwise') for n in name_dels]
    
    names = name_stats + name_flags + name_dels

    data = pd.DataFrame(data=meas, index=timestamps, columns=names)

    data.index = pd.to_datetime(data.index, 
        yearfirst=True, infer_datetime_format=True)

    return data

def synthetic(p, ns):

    '''
    p: full path to folder with MCrunch-files from analysis of FAST simulations
    ns: number of simulations (files listed within statistics)
    '''

    all_files = [f for f in listdir(p) if isfile(join(p, f))]

    loads_files = [join(p, l) for l in all_files if 'dels' in l]
    
    scada_files = [join(p, s) for s in all_files if 'sums' in s]
    
    scada_signals = [s[len(p)+1:-5] for s in scada_files]

    data =  {}

    correctname = 'FileName' 

    # dataframes of stats as dict
    for file in enumerate(scada_files):
    
        signalname = file[1][len(p)+1:-5]
    
        statistics = list(pd.read_csv(file[1], header=1, 
            delim_whitespace=True, nrows=0).columns)
        
        statistics[1] = statistics[0] + statistics[1]
        
        statistics.pop(0)  
    
        colnames = [correctname]
    
        for stat in statistics[1:]:
            colnames.append(stat + '_' + signalname)
    
        data[scada_signals[file[0]]] = pd.read_csv(file[1], header=None,
            names=colnames, skiprows=4, delim_whitespace=True)
        
        data[scada_signals[file[0]]].set_index(colnames[0], drop=True, 
            inplace=True)

    # add loads to dict
    data['loads'] = pd.read_csv(loads_files[0], encoding='ISO-8859-1', 
        header=None, skiprows=4, delim_whitespace=True, nrows=4, 
        usecols = range(4,4+ns)).transpose()

    data['loads'].reset_index(inplace=True, drop=True)

    data['loads'].rename(columns={0:'RootMOoP1', 1:'RootMIP1', 2:'TwrBsMyt', 
        3:'TwrBsMxt'}, inplace=True)

    filenames = data[scada_signals[file[0]]].index

    data['loads'].set_index(filenames, drop=True, inplace=True)

    # concatenate dataframes in dict
    dfs = []
    
    for key in data.keys():
        dfs.append(data[key])
    
    sim = pd.concat(dfs, axis=1)

    return sim

