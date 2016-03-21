# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd # Pandas use here for easy manipulation of CSV files
import numpy as np
# matplotlib is used to make the histogram plots
import matplotlib.pyplot as plt 
import glob # for filename parsing
from pylab import rcParams
rcParams['figure.figsize'] = 6, 10


def calcResult(dataf,assL,row):
    """
    calcResult takes a given row in a module marks file and calculates the overall module mark earned.
    Inputs: 
    dataf: file reference
    assL: list of component weights
    row: index of line being evaluated
    
    Output: 
    module mark earned
    """
    result=0.
    for i, val in enumerate(assL):
        #print i, val, dataf.iloc[row,i+4]
        result=result+float(dataf.iloc[row,i+4])*val/100.
    
    return result
    
def makeAssessList(df):
    """
    makeAssessList produces a list of assessment weightings for the file pointed to by df (a pandas datafile)
    
    Output: list of integer values
    """
    nAssess = int(df.iloc[4,2]) # number of assessments
    
    #make list of assessment values
    assList=[]
    for index in range(4,4+(nAssess)):
        cwkTxt=df.iloc[9,index]
        cwkVal=float(cwkTxt.strip("%"))
        assList.extend([cwkVal])
    return assList

def makeResultsList(df):
    """
    create a list of module results for the students in the file pointed to by df
    Assume that student registration numbers begin with either "A" (for historical comparisons) or "B"
    If this program is in use in a few years this may break

    Output:
        List of results suitable for plotting as histogram
    """
    # get list of assessment values
    assList=makeAssessList(df)
    #For each row of results, go through and calcualte the module mark
    ResultList=[]

    df.fillna('0',inplace=True) # cover up NA values with zeroes.
    #print df

    #first data row is row 11
    i=11
    while df.iloc[i,0].startswith("B") or df.iloc[i,0].startswith("A"):
    #print df.iloc[i,0]
    #for i in range(11,60) :
        ResultList.extend([calcResult(df,assList,i)])
        i=i+1
    return ResultList
    
def HistoFiles(criteria):
    """
    Function to produce histogram(s) of csv files with names matched by criteria
    """
    
    #files=glob.glob("15MPP*.csv") # get list of file names
    files=glob.glob(criteria) # get list of file names
    print len(files) 
    print files
#fig, axes = plt.subplots(nrows=4, ncols=4)
    if len(files)>1:
    #have found multiple files that meet the search citeria
        f, axarr = plt.subplots(nrows=len(files), sharex=True) # setup an array in which to put the plots
        for idx, val in enumerate(files):
    #print idx,val
        #for name in files:
 
            df=pd.read_csv(val,na_values=0) #read current file into the dataFrame df
            #nAssess = int(df.iloc[4,2]) # number of assessments
    
        #make list of assessment values
            #assList=makeAssessList(df)
    #print assList
    #For each row of results, go through and calcualte the module mark
            ResultList=makeResultsList(df) 
    # make histogram of the results 
    #ax1=subplot(len(files),1,idx)
            n,bins,patches=axarr[idx].hist(np.asarray(ResultList),100) 
    #plt.title(val[0:8])
            axarr[idx].set_title(val[0:8])
            axarr[idx].axis([0,100,0,6])
            axarr[len(files)-1].set_xlabel("module mark %")
            f.tight_layout()
        plt.show()
    elif len(files)==1:
    # some code for only one file to work on
        print 'One file found'
        df=pd.read_csv(files[0],na_values=0.)
        #nAssess = int(df.iloc[4,2]) # number of assessments
    
        #make list of assessment values
        #assList=makeAssessList(df)
    #print assList
    #For each row of results, go through and calcualte the module mark
        ResultList=makeResultsList(df) 
        n,bins,patches=plt.hist(ResultList,100)
        plt.show()  
    elif len(files)<=0:
        print 'No files that match the criteria found'

    return




   


