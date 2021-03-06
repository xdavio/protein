import pandas as pd
import numpy as np
import re


def handle_range(data, method, firstcol, lastcol):
    """Method takes the following 3 values:

    0 means average the range of numbers,
    1 means take the first number,
    2 means take the second number,
    3 means take the smaller number
    4 means take the larger number
    
    This method has to do with how data of the form '# to #' is handled."""

    for j in range(1,lastcol+1):
        for i in range(data.shape[0]):
            #i is row, j is column
            
            d = data.iloc[i,j]
            if d == 'not_shown' or d == 'not_given':
                data.iloc[i,j] = np.nan
                continue

            try:
                noD = False
                dd = str(d)
            except:
                noD = True
                dd = ""
            if (type(d) == str and " to " in d) or (" to " in dd):
                if noD:
                    d = dd
                mat = re.search("^([^ ]*) to ([^ ]*)$", d)
                a = float(mat.group(1))
                b = float(mat.group(2))

                if method == 0:
                    data.iloc[i,j] = np.mean((a,b),dtype = np.float)
                elif method == 1:
                    data.iloc[i,j] = a
                elif method == 2:
                    data.iloc[i,j] = b
                elif method == 3:
                    data.iloc[i,j] = np.min((a,b))
                elif method == 4:
                    data.iloc[i,j] = np.max((a,b))
                    
                continue

            data.iloc[i,j] = float(d)

def handle_days(data, method, firstcol, lastcol):
    """MDethod takes 4 values:-1, 0, 1, and 2.

    if method == 0, average over days.
    -1 means do nothing and leave the 2nd days in the data frame and treat them as usual rows.
    """

    r = range(firstcol, lastcol + 1) #range of interest
    
    def process_day(data):
        m = data.shape[0]
        if m == 1:
            return(data)

        def protected_average(col):
            if sum(~np.isnan(col.astype(np.float))) == 0:
                return(np.nan)
            out = np.mean(col[~np.isnan(col.astype(np.float))])
            return(out)

        dataout = data.iloc[[0]].copy()
        dat = data.iloc[:,r]
        dataout.iloc[[0],r] = np.apply_along_axis(protected_average, 0, dat).astype(float)

        return(dataout)

    
    #main function body
    if method == -1:
        return(data)
    else:
        grouped = data.groupby(data.index)
        datanew = grouped.apply(process_day)
        datanew.reset_index(level = 1, inplace = True)

        
        #deep copy dataset
        #datanew = data.copy()
        #day = data['Day_x_Index']
        #m = data.shape[0]
        #datawhich = [False] * m #set to True those days which need modification
        
        #for i in range(m):
        #    if i > 0 and data.index[i] is data.index[i-1] and day[i] is not day[i-1]:
        #        datawhich[i] = True
        #        datanew.ix[i-1,range(firstcol,lastcol + 1)] = np.apply_along_axis(process_day, 0, datanew.ix[[i-1,i],range(firstcol,lastcol + 1)], method).astype(float)

        #grouped = data.groupbydata.index)
        
        #drop second days
        #datanew = datanew.ix[[x[0] for x in enumerate(datawhich) if not x[1]]]
        return(datanew)


if __name__ == "__main__":
    data = pd.DataFrame.from_csv("../DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv")
    handle_range(data)
    dataproc = handle_days(data) #processed data

    #globals: these are the first and last columns of time series data, not auxiliary data!!
    #update: these are passed by the wrapper functions and only declared in the main namespace as globals now
    lastcol = 10
    firstcol = 1

