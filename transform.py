# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Tue May 22 10:19:58 2018

@author: Maxim Bondarenko
"""

#%%
def count_element(count_in, element):
    """
    This function counts the number of element appear in 'count_in'
    
    Returns:
        count of elements
    """
    count = 0
    for value in count_in:
        if value[0] == element:
            count += 1
    return count

#%%
def conver_to_date(list_of_strings):
    
    """
        This function converts string of date to datetime type
        and calculates the difference between the beginning of our era and the 
        current variable from 'list_of_strings'
        
        Returns:
            Data frame of the calculation of the differences
        
    """
    from datetime import datetime
    import pandas as pd
    import numpy as np
    
    first_date = datetime.strptime('0001-01-01', '%Y-%m-%d')
    list_of_date = []
    for string in list_of_strings:
        if type(string) == str:
            days = datetime.strptime(string, '%Y-%m-%d') - first_date
            list_of_date.append(days.days)
        else:
            list_of_date.append(np.nan)
    list_of_date = pd.DataFrame(list_of_date)
    return list_of_date