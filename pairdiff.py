import numpy as np
import pandas as pd
from itertools import starmap, combinations

def foo(a,b):
    """
    Currently the workhorse function for calculating the day-shifted pairwise difference
    """
    x1 = np.min([a,b])
    x2 = np.max([a,b])
    out1 = x2 - x1
    out2 = x1 - x2 + 24
    #return(np.absolute(a-b, dtype = np.float))
    return(np.min([out1,out2]))

def pairdiff(mat):
    """
    takes an m x n matrix, walks over the columns, and places a
    abs|1 - 2| function on the self-outer product of the
    selected column. it then takes the mean of the upper
    triangular matrix induced by this operation, removing
    nan cells from the size of the average. 
    """
    def vectorOperator(vec):
        """takes the outer product of a vector"""
        out = np.array(list(starmap(foo,combinations(vec,2))), dtype = np.float)
        out = out[~np.isnan(out)]
        n = len(out)
        return(np.sum(out,dtype=float)/n)

    return(np.apply_along_axis(vectorOperator, 0, mat))
    #return(np.apply_along_axis(vectorOperator, 0, np.array(mat).T))
    



def summaries(df, firstcol, lastcol):
    """
    make sure df has nothing extraneous -- in other words,
    limit it to just the reduced data frame on firstcol:lastcol;
    in fact, even remove the days column from the df
    """
    fc = firstcol
    lc = lastcol + 1
    ind = range(fc, lc)
    l = len(ind)
    outmean = np.zeros(l)
    outsd = np.zeros(l)
    outnan = [False] * l

    for i in ind:
        j = i - fc
        outmean[j] = np.mean(df.iloc[:,i])
        outsd[j] = np.std(df.iloc[:,i])
        outnan[j] = np.sum([np.isnan(x) for x in df.iloc[:,i]])
    
    n, m = df.shape
    return(
        outmean,
        outsd,
        outnan,
        [n] * l
        )

if __name__ == "__main__":
    import random
    random.seed(1)

    
    
    mat = np.random.rand(3,5)
    pass
