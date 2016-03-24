# lboroHistogram
Produces histograms of Loughborough University module results data

Requires: python (tested with 2.7.11), matplotlib, pandas, numpy

Update 24-3-2016 Added control of layout – can now set maximum number of plots in a single column. Function to allow plot size to be changed added.

to use:

I recommend running in an iPython session. It can be used outside of ipython, but you will need to work out how to deal with changing directory etc. yourself.

Basic usesage
```python
import Histogram as hgm
hgm.HistoFiles('filename_criteria')
```

The function HistoFiles will scan the current directory for files that match the criteria provided. These criteria follow usual wildcard rules e.g. '15MP\*.csv will pick out all the files with 15MP at the beginning of their names and .csv at the ends; 15MPC\*.csv will pick out all the 15MPC files.

HistoFiles is the main function in the Histogram suite:
    Call with 
    
```python 
HistoFiles(criteria,rowmax=6,debug=False)
```

where

```python 
criteria
``` 

is a python string that can include wildcards e.g. '15MPC*.csv'

```python 
rowmax
```

maximum number of rows in output figure (defaults to 6)

```python
debug
```

when set to true, prnts out diagnostics as function runs

Sometimes the default figure size will be too big/small/wrong aspect ratio...
This can be modified via the function plotSize:

```python
plotSize(width=10,height=10)
```

This function will change the size according to the parameters sent to it. You will need to re-run HistoFiles to generate the histograms using this new form factor.
Note 1: the units of the sizes are inches
Note 2: the figure size on the screen may be a scaled version of the dimensions set – when you open the plot in a separate program it will have the specified dimensions.
