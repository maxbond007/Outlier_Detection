# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Thu May 17 2018

@author: Bondarenko M.
"""

import pandas as pd
from detection import calculate_dist, detector, quality_of_classification
from generator_anomalies import generator
#from SQL_import import date_import

def main():
    
    """
        The main function
        
    """
    '''
    database = input("Enter the name of  database: ")
    user = input("Enter your Username: ")
    password = input("Enter the password: ")
    host = input("Enter the host name where PostgreSQL database is install: ")
    port = input("Enter the port: ")

    Data = date_import(database, user, password, host, port)
    '''
    Data = pd.read_csv("Data.csv") 
    # create anomalies
    percent = 10 # percentage of anomalies in the data
    Data, true_data, anom_patients = generator(Data,percent)
    
    # calculate distances
    Mahaldist, Eucliddist, Cosinedist = calculate_dist(Data)
    
    # detection of anomalies
    (euclid, mahal, cosin, macos, maeuc, 
     eucos, maeuccos, outliers) = detector(Mahaldist, Eucliddist, Cosinedist)
    
    # quality control
    #true_data = np.zeros(len(euclid))
    max_acc, accuracy, frame_dict = quality_of_classification(euclid, mahal,
            cosin, macos, maeuc, eucos, maeuccos, true_data)
    
    return Data, max_acc, accuracy, frame_dict, outliers, anom_patients
    

if __name__ == "__main__":
    Data, max_acc, accuracy, frame_dict, outliers, anom_patients = main()
    
    '''output the result of detection'''
    
    combinations = accuracy[max_acc.index(max(max_acc))]
    print('\n\nthe best combinations are: ', combinations)
    print('\n\nthe best percentile is: ', max_acc.index(max(max_acc)))
    
    #comparing of of the result of detection and real anomalies
    combination = list(accuracy[max_acc.index(max(max_acc))].keys())[0]
    output = outliers[combination].loc[:,max_acc.index(max(max_acc))]
    anom_patients = pd.Series(anom_patients)
    list_of_series = [output,anom_patients]
    df = pd.DataFrame(list_of_series).T
    df.columns = ['detected','true_anomalies']
    print('subject id which are anomalies:\n\n', df)


    