import numpy as np
import pandas as pd
from pairdiff import foo as pairdiff
from itertools import combinations
import xlrd

def get_diffs(mat):
    """
    Applies the given pairwise difference function "pairdiff" to all unique pairs and then returns a list of the results. The length of the list is equal to the length of non NA values choose 2.
    """
    diffs = {}
    for column in mat:
        a = np.array(mat[column], dtype = 'float64') #may need to play with this dtype argument
        b = a[~np.isnan(a)]
        diffs[column] = [pairdiff(*x) for x in combinations(b,2)]
    return diffs



## basename = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable_V4'
## foldername = '../' + basename + '/'

## firstcol = 2
## lastcol = 12

## book = xlrd.open_workbook(foldername + "debug.xlsx")
## df = pd.read_excel(io = book, engine = 'xlrd', sheetname = 'datadays')
## mat = df.iloc[1:,firstcol:lastcol]

