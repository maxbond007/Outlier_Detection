# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Thu May 17 2018

@author: Bondarenko M.
"""

import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
from detection import calculate_dist, detector, quality_of_classification
from generator_anomalies import generator

#%%
def count_element(count_in, element):
    """
    How often does 'element' appear in 'count_in'. 
    
    """
    count = 0
    for x in count_in:
        if x[0] == element:
            count += 1
    return count

#%%
def conver_to_date(list_of_strings):
    """
        Converter string of date to datetime format
    """
    first_date = datetime.strptime('0001-01-01', '%Y-%m-%d')
    list_of_date = []
    for x in list_of_strings:
        if type(x) == str:
            days = datetime.strptime(x, '%Y-%m-%d') - first_date
            list_of_date.append(days.days)
        else:
            list_of_date.append(np.nan)
    list_of_date = pd.DataFrame(list_of_date)
    return list_of_date

#%%
def date_import(cursor):
    """
        This function imports "subject_id" "form_id", 
        "question_id" and "data_type" from the database
        
    """

    cursor.execute(''' 
               select Q1."Patient's ID" from
                   (select s.id as "Patient's ID"
                        from cls_form_study_phase f join 
                        cls_subject s on s.id = f.subject_id
                        where f.form_structure_id = 1 
                        and f.soft_delete = false
                        and s.soft_delete = false
                        and s.test_subject = false
                        order by "Patient's ID") as Q1 
                    ''')
    
    Data = cursor.fetchall()
    Data = pd.DataFrame(Data, columns=["Patient_id"])

    cursor.execute(''' 
               select f.form_structure_id as form_id, 
                   q.question_id as question_id,
                   qq.question_datatype_id as data_type
                   from cls_question_group_form_structure f 
                   inner join cls_question_group_question q on 
                   f.question_group_id = q.question_group_id
                   inner join cls_question qq on q.question_id = qq.id
                   order by f.form_structure_id ASC, q.question_id ASC
                   ''')
        
    Parameters_id = cursor.fetchall()
    Parameters_id = pd.DataFrame(Parameters_id,  
                             columns=["Form_id", "Question_id", "Data_type"])
    Parameters_id.Form_id[Parameters_id.Form_id == 3] = 2

    """
        This part of function imports questions from the database, filters and 
        transform data and create dataframe of questions
        
    """
    
    for i,item in enumerate(Parameters_id.Form_id): 
        try: # import questions 
            cursor.execute('''
                select "Q1" from
                (select s.secondary_id as "Patient's ID",
                cls_get_question_value_for_validation(f.form_data-> %s) as "Q1"
                from cls_form_study_phase f join 
                cls_subject s on s.id = f.subject_id
                where f.form_structure_id = %s 
                and f.soft_delete = false
                and s.soft_delete = false
                and s.test_subject = false
                order by "Patient's ID") as Q1 
                ''',('Q' + str(Parameters_id.Question_id[i]), 
                int(Parameters_id.Form_id[i])))
        except psycopg2.InternalError:
            print("Caught error:   iter:",i,
                  ' Form_id:',Parameters_id.Form_id[i],
                  ' Question_id:', Parameters_id.Question_id[i])
            continue
        
        # filtering and transformation of data
        list_of_questions = cursor.fetchall()   
        if (list_of_questions == [] or len(set(list_of_questions)) == 1 or 
            count_element(list_of_questions,None)>len(list_of_questions)*0.8 or
            count_element(list_of_questions,np.nan)>len(list_of_questions)*0.8 or 
            Parameters_id.Data_type[i] == "string" or 
            Parameters_id.Data_type[i] == "heading" or 
            Parameters_id.Data_type[i] == "text"):
            continue 
        
        if Parameters_id.Data_type[i] == "boolean":
            list_of_questions = pd.DataFrame(list_of_questions)
            list_of_questions[list_of_questions == 'true'] = 1
            list_of_questions[list_of_questions == 'false'] = 0 
      
        if Parameters_id.Data_type[i] == "date": 
            list_of_questions = pd.DataFrame(list_of_questions)
            list_of_questions = conver_to_date(list_of_questions) 
          
        if (Parameters_id.Data_type[i] == "real" or 
            Parameters_id.Data_type[i] == "int" or 
            Parameters_id.Data_type[i] == "discrete_value"):
            list_of_questions = [float(np.nan if i[0] is None else i[0]) 
                for i in list_of_questions]
            list_of_questions = pd.DataFrame(list_of_questions)
            
        if list_of_questions.isnull().sum()[0] >= len(list_of_questions)*0.8:
            continue
        
        # add list of questions to the dataframe
        Data['Q' + str(Parameters_id.Question_id[i])] = list_of_questions
        
    cursor.close()
    
    return Data


def main():
    
    conn = psycopg2.connect(database="*******", user="******", 
                        password="********", host="******", port="*****")
    cursor = conn.cursor()
    Data = date_import(cursor)
    
    conn.close() # to close the connection
    
    # create anomalies
    percent = 10
    Data, true_data, anom_patients = generator(Data,percent)
    
    # calculate distances
    Mahaldist, Eucliddist, Cosinedist = calculate_dist(Data)
    # detection of anomalies
    (euclid, mahal, cosin, macos, maeuc, 
     eucos, maeuccos, outliers) = detector(Mahaldist, Eucliddist, Cosinedist)
    #true_data = np.zeros(len(euclid))
    # quality control
    max_acc, accuracy, frame_dict = quality_of_classification(euclid, mahal,
            cosin, macos, maeuc, eucos, maeuccos, true_data)
    
    return Data, max_acc, accuracy, frame_dict, outliers, anom_patients
    

if __name__ == "__main__":
    Data, max_acc, accuracy, frame_dict, outliers, anom_patients = main()
    combinations = accuracy[max_acc.index(max(max_acc))]
    print('\n\nthe best combinations are: ', combinations)
    print('\n\nthe best percentile is: ', max_acc.index(max(max_acc)))
    combination = list(accuracy[max_acc.index(max(max_acc))].keys())[0]
    output = outliers[combination].loc[:,max_acc.index(max(max_acc))]
    anom_patients = pd.Series(anom_patients)
    list_of_series = [output,anom_patients]
    df = pd.DataFrame(list_of_series).T
    df.columns = ['detected','true_anomalies']
    print('subject id which are anomalies:\n\n', df)


    