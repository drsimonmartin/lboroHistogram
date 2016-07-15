# -*- coding: utf-8 -*-
"""
Lbro Histogram
V2.0
MIT License

Copyright (c) 2016 Simon Martin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pandas as pd # Pandas use here for easy manipulation of CSV files
import numpy as np
# matplotlib is used to make the histogram plots
import matplotlib.pyplot as plt 
import glob # for filename parsing
from pylab import rcParams
rcParams['figure.figsize'] = 10, 10

def nAssessments(df):
    return int(df.iloc[4,2]) # number of assessments
    
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
    create a list of module results for the students in the file represented by df
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
    
def CalcResults(df):
    """
    Calc module results
    df contains data from a module CSV file
    Assume that student registration numbers begin with either "A" (for historical comparisons) or "B"
    If this program is in use in a few years this may break

    Output:
        List of results suitable for plotting as histogram
    """
    # get list of assessment values
    assList=makeAssessList(df)
    #For each row of results, go through and calcualte the module mark
    ResultList=[]

    #df.fillna('0',inplace=True) # cover up NA values with zeroes.
    #print df

    #first data row is row 11
    i=11
    while df.iloc[i,0].startswith("B") or df.iloc[i,0].startswith("A"):
    #print df.iloc[i,0]
    #for i in range(11,60) :
        #ResultList.extend([calcResult(df,assList,i)])
        #chaneg this so that it adds a colums to the dataframe
        df.iloc[i,]
        i=i+1
    return df
 
def makeListAssessN(df,n=0):
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
        #ResultList.extend([calcResult(df,assList,i)])
        ResultList.extend([int(df.iloc[i,n+4])])
        i=i+1
    return ResultList   
    
def Geometry(nfiles,rowmax=6):
    """
    calculates plot grid dimensions – limited to rowmax rows
    returns tuple of nrows,ncols needed to fit all histograms (there may be blank spaces)
    uses integer division to work out number of columns
    """
    if nfiles<=rowmax:
        return (nfiles,1)#rows,columns
    else:
        # aim to make a grid that looks as full as possible
        # 
        # number of columns will be (nfiles/rowmax)+1(if (nfiles%rowmax)>=1)
        # number of rows: (nfiles/ncolumns)+1(if (nfiles%rowmax)>=1)
        ncolumns=nfiles/rowmax
        if (nfiles%rowmax)>=1:
            ncolumns=ncolumns+1
        nrows=nfiles/ncolumns
        if (nfiles%ncolumns)>=1:
            nrows=nrows+1
        return (nrows,ncolumns) 
def plotSize(width=10,height=10):
    """
    Allows plot size to ne changed (default 10x10 inches)
    """
    rcParams['figure.figsize'] = width,height
    return

def HistoFiles(criteria,rowmax=6,debug=False,elements=False,transparency=0.25,rmin=0,rmax=100,binning=1):
    """
    Function to produce histogram(s) of csv files with names matched by criteria
    
    Call with HistoFiles(criteria,rowmax=6,debug=False,elements=False,
                         transparency=0.25,rmin=0,rmax=100,binning=1)
        
        criteria is a python string that can include wildcards e.g. '15MPC*.csv'
        
        rowmax: maximum number of rows in output figure (defaults to 6)
        
        debug: when set to true, prnts out diagnostics as function runs
        
        elements: when set to true will produce histograms of all the elements of the module
        
        transparency: set transparency of the elements (0=transparent through to 1 opaque)
        
        rmin, rmax: the ranges used for the x-axis (in percent)
        
        binning: the width of the bins used for the data in %
    """
    # work out number of bins required
    nbins=int(100/binning)
    #files=glob.glob("15MPP*.csv") # get list of file names
    files=glob.glob(criteria) # get list of file names
    print len(files) 
    #if debug: print files
    if len(files)>1:
    #have found multiple files that meet the search citeria
    #get dimensions (rows,cols) of grid needed to fit the plots
        rowCount=0
        nRows,nCols=Geometry(len(files),rowmax)
        #f, axarr = plt.subplots(nrows=nRows,ncols=nCols, sharex=True) # setup an array in which to put the plots
        f, axarr = plt.subplots(nrows=nRows,ncols=nCols, sharex=True) # setup an array in which to put the plots
        print nRows,nCols
        for idx, val in enumerate(files):
            ymax=0
            df=pd.read_csv(val,na_values=0) #read current file into series
            
    #For each row of results, go through and calculate the module mark
            ResultList=makeResultsList(df)
            if nCols>1:
                #if debug: print ResultList
            #dataSet.append(ResultList)
                if idx>0 and (idx%nCols)==0:
                    if debug: print 'hello'
                    rowCount=rowCount+1
                    if debug: print 'rowCount=',rowCount,'idx=',idx,'idx-2*rowCount=',idx-2*rowCount
                    ymax=0                    
                    n,bins,patches=axarr[rowCount,idx-nCols*rowCount].hist(np.asarray(ResultList),nbins,range=(0,100))
                    if max(n)>ymax: ymax=max(n)# keep track of maximum y value
                    if elements==True:
                        # Need to produce plots of the elements as well
                        
                        for i in xrange(0,nAssessments(df)):
                            ResultList=makeListAssessN(df,i)
                            n,bins,patches=axarr[rowCount,idx-nCols*rowCount].hist(ResultList,nbins,range=(0,100),alpha=transparency)
                            if max(n)>ymax: ymax=max(n)
                    axarr[rowCount,idx-nCols*rowCount].set_title(val[0:8])
                    axarr[rowCount,idx-nCols*rowCount].axis([rmin,rmax,0,ymax*1.1])
            #axarr[len(files)-1].set_xlabel("module mark %")
                    f.tight_layout()
                    if debug: print idx, 'idx%2',idx%2
                else:
                    n,bins,patches=axarr[rowCount,idx-nCols*rowCount].hist(np.asarray(ResultList),nbins,range=(0,100))
                    if max(n)>ymax: ymax=max(n)
                    if elements==True:
                        # Need to produce plots of the elements as well
                        for i in xrange(0,nAssessments(df)):
                            ResultList=makeListAssessN(df,i)
                            n,bins,patches=axarr[rowCount,idx-nCols*rowCount].hist(ResultList,nbins,range=(0,100),alpha=transparency)
                            if max(n)>ymax: ymax=max(n)
                                
                    axarr[rowCount,idx-nCols*rowCount].set_title(val[0:8])
                    axarr[rowCount,idx-nCols*rowCount].axis([rmin,rmax,0,ymax*1.1])
            else:
                if debug: print ResultList
            #dataSet.append(ResultList)
                
                n,bins,patches=axarr[idx].hist(np.asarray(ResultList),nbins,range=(0,100))
                if max(n)>ymax: ymax=max(n)
                if elements==True:
                        # Need to produce plots of the elements as well
                        for i in xrange(0,nAssessments(df)):
                            ResultList=makeListAssessN(df,i)
                            n,bins,patches=axarr[idx].hist(ResultList,nbins,range=(0,100),alpha=transparency)
                            if max(n)>ymax: ymax=max(n)
                axarr[idx].set_title(val[0:8])
                axarr[idx].axis([rmin,rmax,0,ymax*1.1])
            #axarr[len(files)-1].set_xlabel("module mark %")
                f.tight_layout()
                
        #print dataSet
        #plt.hist(dataSet,bins=100,stacked=True,sharex=True)
        #dataSet.plot(kind='hist', alpha=0.5)
        
        plt.show()
        
    elif len(files)==1:
    # some code for only one file to work on
        print 'One file found'
        df=pd.read_csv(files[0],na_values=0.)
        ymax=0
        #nAssess = int(df.iloc[4,2]) # number of assessments
    
        #make list of assessment values
        #assList=makeAssessList(df)
    #print assList
    #For each row of results, go through and calcualte the module mark
        if elements == False:
            ResultList=makeResultsList(df) 
            n,bins,patches=plt.hist(ResultList,bins=100,range=(0,100))
            if max(n)>ymax: ymax=max(n)
            plt.xlim(rmin,rmax)
            plt.ylim(0,ymax*1.1)    
            plt.show() 
            print ymax
        elif elements == True:
            # Need to produce histograms of each element
            # Draw overall results first
            ResultList=makeResultsList(df) 
            n,bins,patches=plt.hist(ResultList,bins=nbins,range=(0,100))
            if max(n)>ymax: ymax=max(n)
            #now draw the components, use alpha channel to set opacity
            for i in xrange(0,nAssessments(df)):
                ResultList=makeListAssessN(df,i)
                if debug: print ResultList
                n,bins,patches=plt.hist(ResultList,bins=nbins,range=(0,100),alpha=transparency)
                if max(n)>ymax: ymax=max(n)
            plt.xlim(rmin,rmax)
            plt.ylim(0,ymax*1.1)
            plt.show()
            #plt.show
            print ymax
            
    elif len(files)<=0:
        print 'No files that match the criteria found'

    return

def moduleStats(module,debug=False):
    """ 
    returns basic statistics on module(s) given by "module". Expects Lboro module results file.

    module is a python string that can include wildcards e.g. '15MPC*.csv'
    
    gives results for one file per line of output

    debug optin gives extra output
    """
    
    files=glob.glob(module) # get list of file names
    print 'Output for ',len(files),' files'
    for idx,val in enumerate(files):
        df=pd.read_csv(val) #read current file into series
        #replace zeros with NaN
        df=df.replace(0,np.NaN)   
    #For each row of results, go through and calculate the module mark
        ResultList=makeResultsList(df)
        ResultSeries=pd.Series(ResultList)
        if debug:print ResultSeries
        #print val,' mean=',ResultSeries.mean()
        print '{0} mean={1:.1f}'.format(val,ResultSeries.mean())
         
    return



   


