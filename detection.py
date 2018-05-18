# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Thu May 17 23:19:12 2018

@author: panda
"""

'''          
#%%
import pandas as pd
import numpy as np
import scipy as sp
import scipy.spatial.distance as dist
from sklearn.metrics import confusion_matrix, accuracy_score
   
test = Data.copy(deep=True) 
'''

#%% 

def calculate_dist(data):
    """
        This function replace NaN values for median and scaling values to [0 1]
        calculate three vectors of Euclidean,Mahalanobis and Cosine distances 
        
    """ 
    import scipy.spatial.distance as dist
    import numpy as np
    import scipy as sp
    from ploting import boxplot, histogram
    
    # scaling
    del data['Patient_id']    
    for k in  data.columns:
        data[k] = data[k].fillna(round(data[k].median()))
        data[k] = (data[k] - data[k].min())
        data[k] = (data[k] - data[k].min())/data[k].max()
        if data[k].isnull().sum() >  len(data[k])*0.8 or len(set(data[k])) == 1:
            del data[k]


    centroid =  np.mean(data) 
    centroid = centroid.as_matrix()
    numpyMatrix = data.as_matrix()

    #Calculate covariance matrix
    covmx = data.cov()
    invcovmx = sp.linalg.pinv(covmx)
    
    #Calculate Euclidean,Mahalanobis and Cosine distance
    Mahaldist, Eucliddist, Cosinedist  = [],[],[]
    for h in range(len(numpyMatrix)):   
        Mahaldist.append(dist.mahalanobis(numpyMatrix[h], centroid, invcovmx))
        Eucliddist.append(dist.euclidean(numpyMatrix[h], centroid))
        Cosinedist.append(dist.cosine(numpyMatrix[h], centroid))
        
    # ploting
    boxplot(Eucliddist,Mahaldist,Cosinedist)
    histogram(Eucliddist,Mahaldist,Cosinedist, len(data))
        
    return Mahaldist, Eucliddist, Cosinedist

#%% 
    
def detector(Mahaldist, Eucliddist, Cosinedist):
    '''
        Outlier Detection by percentile
    '''
    import pandas as pd
    import numpy as np
    size = len(Eucliddist)

    outliers_euc, outliers_mah, outliers_cos = [],[],[]
    outliers_1, outliers_2, outliers_3, outliers_4 = [],[],[],[]
    
    euclid = pd.DataFrame([[0]*20 for i in range(size)])
    mahal = pd.DataFrame([[0]*20 for i in range(size)])
    cosin = pd.DataFrame([[0]*20 for i in range(size)])
    macos = pd.DataFrame([[0]*20 for i in range(size)])
    maeuc = pd.DataFrame([[0]*20 for i in range(size)])
    eucos = pd.DataFrame([[0]*20 for i in range(size)])
    maeuccos = pd.DataFrame([[0]*20 for i in range(size)])

    
    for k in range(20):
        P1=np.percentile(Eucliddist, 80+k)
        P2=np.percentile(Mahaldist, 80+k)
        P3=np.percentile(Cosinedist, 80+k)
      
        my_list1 = pd.DataFrame([[x,index] for index, x in enumerate(Eucliddist) 
            if x >= P1], columns=['parametr','id'])
        my_list2 = pd.DataFrame([[x,index] for index, x in enumerate(Mahaldist) 
            if x >= P2], columns=['parametr','id'])
        my_list3 = pd.DataFrame([[x,index] for index, x in enumerate(Cosinedist) 
            if x >= P3], columns=['parametr','id'])
    
        # search for similar anomalies
        outliers1 = pd.DataFrame(list(set(my_list2.id) & set(my_list3.id)))
        outliers2 = pd.DataFrame(list(set(my_list1.id) & set(my_list2.id)))
        outliers3 = pd.DataFrame(list(set(my_list1.id) & set(my_list3.id)))
        outliers4 = pd.DataFrame(list(set(my_list1.id) & set(my_list2.id) & set(my_list3.id)))
    
        outliers_4.append(list(set(my_list1.id) & set(my_list2.id) & set(my_list3.id)))
        outliers_3.append(list(set(my_list1.id) & set(my_list3.id)))
        outliers_2.append(list(set(my_list1.id) & set(my_list2.id)))
        outliers_1.append(list(set(my_list2.id) & set(my_list3.id)))
    
        outliers_euc.append(list(set(my_list1.id)))
        outliers_mah.append(list(set(my_list2.id)))
        outliers_cos.append(list(set(my_list3.id)))
    
        if not outliers1.empty:
            macos[k][outliers1[0]] = 1
        if not outliers2.empty:   
            maeuc[k][outliers2[0]] = 1
        if not outliers3.empty:
            eucos[k][outliers3[0]] = 1
        if not outliers4.empty:
            maeuccos[k][outliers4[0]] = 1
    
        euclid[k][my_list1.id] = 1
        mahal[k][my_list2.id] = 1
        cosin[k][my_list3.id] = 1

    outliers = {}
    #dictionary of dataframe of anomalies
    outliers['euclid'] = pd.DataFrame(outliers_euc).T
    outliers['mahal'] = pd.DataFrame(outliers_mah).T
    outliers['cosine'] = pd.DataFrame(outliers_cos).T
    outliers['mahal+cosine'] = pd.DataFrame(outliers_1).T
    outliers['mahal+euclid'] = pd.DataFrame(outliers_2).T
    outliers['euclid+cosine'] = pd.DataFrame(outliers_3).T
    outliers['mah+euc+cos'] = pd.DataFrame(outliers_4).T
    

    return euclid, mahal, cosin, macos, maeuc, eucos, maeuccos, outliers

      
#%%
def quality_of_classification(euclid, mahal, cosin, macos, maeuc, eucos, 
                              maeuccos, true_data):
    
    '''
        This function calculate accuracy, specificity and sensitivity
        in different combinations of distance
    
    '''
    import pandas as pd
    from sklearn.metrics import confusion_matrix, accuracy_score
    #true_data = np.zeros(len(euclid))
    accuracy_euclid, accuracy_mahal, accuracy_cosin = [],[],[]
    specificity_euclid, specificity_mahal, specificity_cosin = [],[],[]
    sensitivity_euclid, sensitivity_mahal, sensitivity_cosin = [],[],[]
    accuracy_macos, specificity_macos, sensitivity_macos = [],[],[]
    accuracy_maeuc, specificity_maeuc, sensitivity_maeuc = [],[],[]
    accuracy_eucos, specificity_eucos, sensitivity_eucos = [],[],[]
    accuracy_maeuccos, specificity_maeuccos, sensitivity_maeuccos = [],[],[]
    accuracy = []
    max_acc = []

    frame_dict = {k: pd.DataFrame(columns=['sensitivity','specificity','accuracy']) 
        for k in range(20)}

    for i in range(20):
    
        tn,fp,fn,tp = confusion_matrix(true_data, euclid[i]).ravel()
        accuracy_euclid.append(accuracy_score(true_data, euclid[i]))
        specificity_euclid.append(fp/(fp+tp))
        sensitivity_euclid.append(tp/(tp+fn))
    
        tn,fp,fn,tp = confusion_matrix(true_data, mahal[i]).ravel()
        accuracy_mahal.append(accuracy_score(true_data, mahal[i]))
        specificity_mahal.append(fp/(fp+tp))
        sensitivity_mahal.append(tp/(tp+fn))
    
        tn,fp,fn,tp = confusion_matrix(true_data, cosin[i]).ravel()
        accuracy_cosin.append(accuracy_score(true_data, cosin[i]))
        specificity_cosin.append(fp/(fp+tp))
        sensitivity_cosin.append(tp/(tp+fn))
        
        tn,fp,fn,tp = confusion_matrix(true_data, macos[i]).ravel()
        accuracy_macos.append(accuracy_score(true_data, macos[i]))
        specificity_macos.append(fp/(fp+tp))
        sensitivity_macos.append(tp/(tp+fn))
        
        tn,fp,fn,tp = confusion_matrix(true_data, eucos[i]).ravel()
        accuracy_eucos.append(accuracy_score(true_data, eucos[i]))
        specificity_eucos.append(fp/(fp+tp))
        sensitivity_eucos.append(tp/(tp+fn))
    
        tn,fp,fn,tp = confusion_matrix(true_data, maeuc[i]).ravel()
        accuracy_maeuc.append(accuracy_score(true_data, maeuc[i]))
        specificity_maeuc.append(fp/(fp+tp))
        sensitivity_maeuc.append(tp/(tp+fn))
    
        tn,fp,fn,tp = confusion_matrix(true_data, maeuccos[i]).ravel()
        accuracy_maeuccos.append(accuracy_score(true_data, maeuccos[i]))
        specificity_maeuccos.append(fp/(fp+tp))
        sensitivity_maeuccos.append(tp/(tp+fn))
  

        frame_dict[i].loc['euclid'] = [sensitivity_euclid[i],
                   specificity_euclid[i],accuracy_euclid[i]]
        frame_dict[i].loc['mahal'] = [sensitivity_mahal[i],
                   specificity_mahal[i],accuracy_mahal[i]]
        frame_dict[i].loc['cosin'] = [sensitivity_cosin[i],
                   specificity_cosin[i],accuracy_cosin[i]]
        frame_dict[i].loc['mahal+cosine'] = [sensitivity_macos[i],
                   specificity_macos[i],accuracy_macos[i]]
        frame_dict[i].loc['euclid+cosine'] = [sensitivity_eucos[i],
                   specificity_eucos[i],accuracy_eucos[i]]
        frame_dict[i].loc['mahal+euclid'] = [sensitivity_maeuc[i],
                   specificity_maeuc[i],accuracy_maeuc[i]]
        frame_dict[i].loc['mah+euc+cos'] = [sensitivity_maeuccos[i],
                   specificity_maeuccos[i],accuracy_maeuccos[i]]

        max_acc.append(frame_dict[i]['accuracy'].max())
        accuracy.append(frame_dict[i]['accuracy'][frame_dict[i]['accuracy'] == max_acc[i]].to_dict())
    
        #max_acc.index(max(max_acc))
    return max_acc, accuracy, frame_dict
    

