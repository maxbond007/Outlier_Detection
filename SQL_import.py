# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Tue May 22 10:25:04 2018

@author: Maxim Bondarenko
"""

def date_import(database, user, password, host, port):
    """
        This function imports "subject_id" "form_id", 
        "question_id" and "data_type" from the database
        It also imports questions from the database, filters, 
        transform data.
        
        Returns:
            dataframe of questions where the rows contain patient's id and 
            the columns are alone questions for each patient
        
    """
    
    import pandas as pd
    import numpy as np
    import psycopg2
    from transform import count_element, conver_to_date
    
    conn = psycopg2.connect(database=database, user=user, 
                        password=password, host=host, port=port)
    cursor = conn.cursor()

    # execute patient id from database
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

    # execute "form_id","question_id" and "data_type" from database
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
    
    for i,item in enumerate(Parameters_id.Form_id): 
        try: 
            # execute alone questions for each patient
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
            print("Caught InternalError:   iter:",i,
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
    conn.close() # to close the connection
    
    return Data
