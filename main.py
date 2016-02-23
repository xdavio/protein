import pandas as pd
from process import handle_range, handle_days
from pairdiff import pairdiff, summaries
from filter import filterobj, createQuery
from copy import copy
import os.path
from os import makedirs
import xlsxwriter
from blockaverage import get_diffs
import json
from xmlreader import xmlwrapper

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
        excel
        ):
    
        #import data
        #determine type of import: csv of excel
        filetype = os.path.basename(filepath).split(".")[1]
        if filetype == "csv":
            data = pd.DataFrame.from_csv(filepath)
        elif filetype == "xlsx" or filetype == "xls":
            data = pd.read_excel(filepath, sheetname = excel, index_col = 0) #reads the sheet indexed by "excel" - it's python indexed.

        self.data = copy(data) #original data

        handle_range(data, numberrange, firstcol, lastcol) #process range issue, i.e. [number] to [number]
        self.datarange = copy(data) #save the range dataset

        #process subset selection from query.xml     take data, give datadrop
        inclusion = createQuery(querypath, data.shape[0], data)
        datadrop = data.ix[[x[0] for x in enumerate(inclusion) if x[1]]] #0 is row, 1 is true if the row should be included
        self.dataquery = datadrop #save the query inclusion

        #process data with multiple days. 0 is average, 1 is first, 2 is second, -1 is keep all rows    #take datadrop, give dataproc
        dataproc = handle_days(datadrop, dayrange, firstcol, lastcol)
        m, n = dataproc.shape
        self.datadays = dataproc

        #create difference     take dataproc
        datamat = dataproc.iloc[:,range(firstcol,lastcol + 1)]
        self.datamat = datamat
        diff = pairdiff(datamat)
        diffmeas = pd.DataFrame(data = diff,
                                index = dataproc.columns[firstcol:lastcol+1],
                                columns = ["diff"])

        #add summary information to output
        outmean, outsd, outnan, outsamplesize = summaries(dataproc, firstcol, lastcol)
        diffmeas['mean'] = pd.Series(outmean, index = diffmeas.index)
        diffmeas['sd'] = pd.Series(outsd, index = diffmeas.index)
        diffmeas['count_nan'] = pd.Series(outnan, index = diffmeas.index)
        diffmeas['sample_size'] = pd.Series(outsamplesize, index = diffmeas.index)

        self.pairdiff = diffmeas
        self.debugger(filepath)
            
        return(diffmeas)

    def debugger(self,filepath):
        """
        Writes XLSX files for each step of the data filter process
        """
        directory = os.path.basename(filepath).split(".")[0]
        self.dirname = str(directory)
        if not os.path.exists(directory):
            makedirs(directory)

        def filexlsx(foo):
            """
            Creates xlsx filepath/name
            """
            filepath = directory + "/" + foo + ".xlsx"
            return(filepath)

        def filejson(foo):
            """
            Creates xlsx filepath/name
            """
            filepath = directory + "/" + foo + ".json"
            return(filepath)


        writer = pd.ExcelWriter(filexlsx('debug'), engine='xlsxwriter')
        self.data.to_excel(writer, sheet_name = 'data')
        self.datarange.to_excel(writer, sheet_name = 'datarange')
        self.datadays.to_excel(writer, sheet_name = 'datadays')
        self.dataquery.to_excel(writer, sheet_name = 'dataquery')
        self.pairdiff.to_excel(writer, sheet_name = 'pairdiff')
        writer.save()

        with(open(filejson('pairs'), 'w')) as f:
            f.write(json.dumps(get_diffs(self.datamat)))

def allxml(querypath = 'query.xml'):
    filepath, numberrange, dayrange, firstcol, lastcol, excel = xmlwrapper(querypath)
    foo = pairDiff()
    foo.getPairDiff(
        filepath,
        querypath,
        numberrange,
        dayrange,
        firstcol,
        lastcol,
        excel
        )
    return(foo)


def getPairDiff(
        filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
        querypath = 'query.xml',
        numberrange = 0,
        dayrange = 0,
        firstcol = 1,
        lastcol = 10,
        excel = 0
        ):
    foo = pairDiff()
    foo.getPairDiff(
        filepath,
        querypath,
        numberrange,
        dayrange,
        firstcol,
        lastcol,
        excel
        )
    return(foo)

if __name__ == "__main__":
    #globals
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv'
    querypath = 'pairdiff/query.xml'
    numberrange = 0
    dayrange = 0
    excel = 0
    firstcol = 1 #python indexed
    lastcol = 10 #python indexed

