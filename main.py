#import phase
import pandas as pd
from process import handle_range, handle_days
from pairdiff import pairdiff, summaries
from filter import filterobj, createQuery
from copy import copy
import os.path
from os import makedirs

class pairDiff(object): 
    def __init__(self):
        self.data = None        #original data import
        self.datarange = None   #data after [number] to [number] modification
        self.datadays = None    #data after days cleanup
        self.dataquery = None   #data after XML subset selection (query)
        self.pairdiff = None    #pairdiff output

    def getPairDiff(
        self,
        filepath,
        querypath,
        numberrange,
        dayrange,
        firstcol,
        lastcol,
        local_hijack
        ):
    
        #import data
        #determine type of import: csv of excel
        filetype = os.path.basename(filepath).split(".")[1]
        if filetype == "csv":
            data = pd.DataFrame.from_csv(filepath)
        elif filetype == "xlsx" or filetype == "xls":
            data = pd.read_excel(filepath, sheetname = 0, index_col = 0) #right now just reads first sheet
        if local_hijack:
            self.data = copy(data)

        #process range issue, i.e. [number] to [number]
        handle_range(data, numberrange, firstcol, lastcol)
        if local_hijack:
            self.datarange = copy(data)

        #process subset selection from query.xml     take data, give datadrop
        inclusion = createQuery(querypath, data.shape[0], data)
        datadrop = data.ix[[x[0] for x in enumerate(inclusion) if x[1]]]
        if local_hijack:
            self.dataquery = datadrop

        #process data with multiple days. 0 is average, 1 is first, 2 is second, -1 is keep all rows    #take datadrop, give dataproc
        dataproc = handle_days(datadrop, dayrange, firstcol, lastcol)
        m, n = dataproc.shape
        if local_hijack:
            self.datadays = dataproc

        #create difference     take dataproc
        diff = pairdiff(dataproc.iloc[:,range(firstcol,lastcol + 1)])
        diffmeas = pd.DataFrame(data = diff,
                                index = dataproc.columns[firstcol:lastcol+1],
                                columns = ["diff"])

        #add summary information to output
        outmean, outsd, outnan, outsamplesize = summaries(dataproc, firstcol, lastcol)
        diffmeas['mean'] = pd.Series(outmean, index = diffmeas.index)
        diffmeas['sd'] = pd.Series(outsd, index = diffmeas.index)
        diffmeas['count_nan'] = pd.Series(outnan, index = diffmeas.index)
        diffmeas['sample_size'] = pd.Series(outsamplesize, index = diffmeas.index)

        if local_hijack:
            self.pairdiff = diffmeas
            self.debugger(filepath)
            
        return(diffmeas)

    def debugger(self,filepath):
        directory = os.path.basename(filepath).split(".")[0]
        if not os.path.exists(directory):
            makedirs(directory)

        #output everything
        #####PROBLEM THESE OUTPUT CSVS DON'T HANDLE MULTIPLE FACTORS!!
        def filecsv(foo):
            filepath = directory + "/" + foo + ".csv"
            return(filepath)
        self.data.to_csv(filecsv('data'))
        self.datarange.to_csv(filecsv('datarange'))
        self.datadays.to_csv(filecsv('datadays'))
        self.dataquery.to_csv(filecsv('dataquery'))
        self.pairdiff.to_csv(filecsv('pairdiff'))


def getPairDiff(
        filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
        querypath = 'query.xml',
        numberrange = 0,
        dayrange = 0,
        firstcol = 1,
        lastcol = 10
        ):

    foo = pairDiff()
    return(
        foo.getPairDiff(
            filepath,
            querypath,
            numberrange,
            dayrange,
            firstcol,
            lastcol,
            local_hijack = False
            )
        )

def getPairDiffdebug(
        filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
        querypath = 'query.xml',
        numberrange = 0,
        dayrange = 0,
        firstcol = 1,
        lastcol = 10
        ):
    foo = pairDiff()
    foo.getPairDiff(
        filepath,
        querypath,
        numberrange,
        dayrange,
        firstcol,
        lastcol,
        local_hijack = True
        )
    return(foo)

if __name__ == "__main__":
    #globals
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv'
    querypath = 'pairdiff/query.xml'
    numberrange = 0
    dayrange = 0
    firstcol = 1 #python indexed
    lastcol = 10 #python indexed
