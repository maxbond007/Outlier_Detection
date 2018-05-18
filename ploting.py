# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Fri May 18 03:02:31 2018

@author: panda
"""

def boxplot(Euclideandist,Mahalanobisdist,Cosinedist): 
    '''
        Ploting boxplot
        
    '''
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    fig.suptitle('Metriky vzdálenosti', fontsize=16)
    ax = fig.add_subplot(131)
    ax.boxplot(Euclideandist, labels=['Euclidean'], showmeans=True, 
           showfliers=True)
    ax.set_ylabel('Vzdálenost', fontsize=10)
    ax = fig.add_subplot(132)
    ax.boxplot(Mahalanobisdist, labels = ['Mahalanobis'], showmeans=True, 
           showfliers=True)
    ax = fig.add_subplot(133)
    ax.boxplot(Cosinedist, labels = ['Cosine'], showmeans=True, 
           showfliers=True)
    fig.show()
    return 0


def histogram(Euclideandist,Mahalanobisdist, Cosinedist, length):
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    # hist of Euclidean
    x = np.arange(1,length+1)
    plt.figure()
    plt.hist(x, weights = Euclideandist, bins=length, 
             histtype='bar', ec='k', linewidth=0.1)
    plt.title ("Euklidovská vzdálenost",  {'fontname':'Times New Roman'}, 
               fontsize=16)
    plt.xlim(0, length)
    plt.ylim(0, max(Euclideandist))
    plt.ylabel('Vzdálenost',  {'fontname':'Times New Roman'}, fontsize=14)
    plt.xlabel('Id pacienta',  {'fontname':'Times New Roman'}, fontsize=14)
    plt.axhline(y= np.mean(Euclideandist), color='r', linestyle='-', 
                label = 'střední hodnota')
    plt.axhline(y= np.median(Euclideandist), color='k', linestyle='-', 
                label = 'medián')
    plt.legend(loc='left right', frameon = False)
    plt.show()

    # hist of Mahalanobis
    x = np.arange(1,length+1)
    plt.figure()
    plt.hist(x, weights = Mahalanobisdist, bins=length, 
             histtype='bar', ec='k', linewidth=0.1)
    plt.title ("Mahalanobisová vzdálenost", {'fontname':'Times New Roman'}, 
               fontsize=16)
    plt.xlim(0, length)
    plt.ylim(0, max(Mahalanobisdist)+5)
    plt.ylabel('Vzdálenost', {'fontname':'Times New Roman'}, fontsize=14)
    plt.xlabel('Id pacienta', {'fontname':'Times New Roman'}, fontsize=14)
    plt.axhline(y= np.mean(Mahalanobisdist), color='r', linestyle='-', 
                label = 'střední hodnota ')
    plt.axhline(y= np.median(Mahalanobisdist), color='k', linestyle='-', 
                label = 'medián')
    plt.legend(loc='left right', frameon = False)
    plt.show()

    # hist of Cosine
    x = np.arange(1,length+1)
    plt.figure()
    plt.hist(x, weights = Cosinedist, bins=length, 
             histtype='bar', ec='k', linewidth=0.1)
    plt.title ("Kosinová podobnost", {'fontname':'Times New Roman'}, 
               fontsize=16)
    plt.xlim(0, length)
    plt.ylim(0, max(Cosinedist))
    plt.ylabel('Vzdálenost', {'fontname':'Times New Roman'}, fontsize=14)
    plt.xlabel('Id pacienta', {'fontname':'Times New Roman'}, fontsize=14)
    plt.axhline(y= np.mean(Cosinedist), color='r', linestyle='-', 
                label = 'střední hodnota ')
    plt.axhline(y= np.median(Cosinedist), color='k', linestyle='-', 
                label = 'medián')
    plt.legend(loc='left right', frameon = False)
    plt.show()
    
    return 0
