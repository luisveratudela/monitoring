# -*- coding: utf-8 -*-
'''
functions that build a data-driven model based on optimized architecture

by lvt, September 2017
'''

import numpy as np

from sklearn.neighbors import KNeighborsRegressor as neighbors
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping

def knn_build(X, y):

    '''
    X: 2D np-array with predictors
    y: 1D np-array with target
    '''
    
    np.random.seed(96)
    
    
    return model


def nn_build(nl, n1, nc, nx=None, activ='relu', optim='adam', cfunc='mse'):

    '''
    nl: number of hidden layers
    n1: number of neurons in first hidden layer
    nc: number of predictors
    nx: number of neurons in all subsequent hidden layers (if nlayers > 1)
    activ: activation function
    optim: optimization function
    cfunc: cost function to optimize ('mse', 'mae')
    '''
    
    assert ( nl >=1 ) & ( n1 >=1 ) & ( nc >= 1 ), 'min: 1 layer/neuron/column'

    np.random.seed(96)
    
    model = Sequential()
    model.add( Dense(n1, input_dim=nc, activation=activ) )
    
    count = 2 # used at least in 2nd layer
    if nl > 1:
        while count <= nl:
            model.add( Dense(nx, activation=activ) ) # equal layers
            count += 1 
        
    model.add( Dense(1) ) # last layer
    
    model.compile( loss=cfunc, optimizer=optim )
    
    return model

def nn_fit(model, X, y, nsplit=0.3, npatience=6, nepochs=200):

    '''
    model: nn build with keras and lms.nn_build function
    X: 2D np-array with predictors
    y: 1D np-array with targets
    nsplit: fraction hold out for validation
    npatience: nr of runs to wait for improvement
    nepochs: times all data are passed to improve
    '''
  
    #assert type(model) =='keras*', 'model type cannot be processed'
    
    assert X.shape[0] == y.shape[0], 'nr. of records are not equal'

    nbatch = int( y.shape[0] / 50 ) # run at approx. 2% 
    if nbatch > 250: nbatch = 250 # for computing with a laptop 

    watch = EarlyStopping( patience=npatience )

    training = model.fit( X, y, epochs=nepochs, batch_size=nbatch,
                    validation_split=nsplit, callbacks=[watch], verbose=0 )

    return training

