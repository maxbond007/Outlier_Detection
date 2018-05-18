# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Fri May 18 01:59:51 2018

@author: panda
"""
def generator(test, percent):
    
    import numpy as np  
    # генерация аномальных пациентов 1%
    if percent == 1:
        true_data = np.zeros(len(test))
        anom_patients = [100,303,404,256]
        for i in anom_patients:
            test.iloc[int(i),1:50] = 5
            test.iloc[int(i),300:370] = 5
            true_data[i] = 1
            
    # генерация аномальных пациентов 5%
    elif percent == 5:
        true_data = np.zeros(len(test))
        anom_patients = [0,1,2,3,4,5,6,7,9,11,28,40,53,89,201,203]
        for i in anom_patients:
            test.iloc[i,0:50] = 5
            test.iloc[i,300:370] = 5
            true_data[i] = 1
    
    # генерация аномальных пациентов 10%
    elif percent == 10:
        true_data = np.zeros(len(test))
        anom_patients = [i for i in np.arange(0,400, 10)]
        for i in anom_patients:
            test.iloc[int(i),1:100] = 5
            test.iloc[int(i),300:370] = 5
            true_data[int(i)] = 1   
    
    # генерация аномальных пациентов 15%
    elif percent == 15:
        true_data = np.zeros(len(test))
        anom_patients = [i for i in np.arange(0,400, 7)]
        for i in anom_patients:
            test.iloc[i,1:100] = 5
            true_data[i] = 1 
            
    else:
        print('Wrong number of percent, please choose one from these: 1,5,10,15')
    return test, true_data, anom_patients