# lboroHistogram
Produces histograms of Loughborough University module results data

Requires: python (tested with 2.7.11), matplotlib, pandas, numpy

to use:

I recommend running in an iPython session. It can be used outside of ipython, but you will need to work out how to deal with changing directory etc. yourself.

```python
import Histogram as hgm
hgm.HistoFiles('filename_criteria')
```

The function HistoFiles will scan the current directory for files that match the criteria provided. These criteria follow usual wildcard rules e.g. '15MP\*.csv will pick out all the files with 15MP at the beginning of their names and .csv at the ends; 15MPC\*.csv will pick out all the 15MPC files.

