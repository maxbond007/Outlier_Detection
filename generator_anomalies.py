# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Fri May 18 01:59:51 2018

@author: Maxim Bondarenko
"""
def generator(test, percent):
    
    """
        This function generates anomalies in the data (1%, 5%, 10%, 15%)
        
        Returns:
            data with anomalies
        
    """
    
    import numpy as np  
    # 1% of anomalies in the data
    if percent == 1:
        true_data = np.zeros(len(test))
        anom_patients = [100,303,404,256]
        for i in anom_patients:
            test.iloc[int(i),1:50] = 5
            test.iloc[int(i),300:370] = 5
            true_data[i] = 1
            
    # 5% of anomalies in the data
    elif percent == 5:
        true_data = np.zeros(len(test))
        anom_patients = [0,1,2,3,4,5,6,7,9,11,28,40,53,89,201,203]
        for i in anom_patients:
            test.iloc[i,0:50] = 5
            test.iloc[i,300:370] = 5
            true_data[i] = 1
    
    # 10% of anomalies in the data
    elif percent == 10:
        true_data = np.zeros(len(test))
        anom_patients = [i for i in np.arange(0,400, 10)]
        for i in anom_patients:
            test.iloc[int(i),1:100] = 5
            test.iloc[int(i),300:370] = 5
            true_data[int(i)] = 1   
    
    # 15% of anomalies in the data
    elif percent == 15:
        true_data = np.zeros(len(test))
        anom_patients = [i for i in np.arange(0,400, 7)]
        for i in anom_patients:
            test.iloc[i,1:100] = 5
            true_data[i] = 1 
            
    else:
        print('Wrong number of percent, please choose one from these: 1,5,10,15')
    return test, true_data, anom_patients