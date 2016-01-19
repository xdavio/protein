from xml.dom import minidom
from itertools import izip
import re

pattern = '^\d*' #only used in regex search of index

class filterobj():
    """
    This object converts the xml file in the createQuery into a boolean vector
    of row inclusion.
    """
    def __init__(self, m, data):
        self.m = m
        self.include = [True] * self.m
        self.data = data
        pass
            
    def includeColFactors(self, col, argl, inclusion = True):
        """
        col is the string of the column name of interest,
        argl is a list of strings of factors of interest.
        inclusion determines if the factors of interest are included or excluded
        from final row inclusion.
        """
        self.tmp = [False] * self.m
        for value in argl:
            try:
                self.l = list([value in x for x in self.data[col]])
            except:
                #sometimes this string comparison is needed
                self.l = list([str(value) in str(x) for x in self.data[col]])
            self.tmp = [max(a,b) for a,b in izip(self.l,self.tmp)]

        #flip for exclusion
        if not inclusion:
            self.tmp = [not x for x in self.tmp]

        #add this column
        self.add_to_list(self.tmp)

    def rawinclude(self, l, inclusion = True):
        """
        This method deals with user-defined inclusion / exclusion of rows based on row number.
        Here, the user-supplied rows are NOT python-indexed, that is, they start with 1 and not 0.
        """
        #l is list of inclusion indices plus 1
        self.tmp = [False] * self.m
        for i in l:
            self.tmp[i - 1] = True
        if not inclusion:
            self.tmp = [not x for x in self.tmp] #only difference between previous func and this one is this line
        self.add_to_list(self.tmp)

    def add_to_list(self, add):
        """
        Worker function that updates global inclusion boolean vector
        """
        self.include = [x and y for x,y in izip(self.include,add)]
        
def createQuery(xmlfile, m, dataproc):
    """
    Reads XML file and wraps the filterobj class above.
    """

    query = filterobj(m,dataproc) #build query object
    xmldoc = minidom.parse(xmlfile) #xml processing only user input is here

    #raw row exlusion / inclusion
    try:
        rawexclusion = xmldoc.getElementsByTagName('rowMod')
        rawType = str(rawexclusion[0].attributes['type'].value)
        rawValue = [int(x) for x in (rawexclusion[0].firstChild.nodeValue).split(',')]
        if rawType == 'include':
            query.rawinclude(rawValue, inclusion = True)
        else:
            query.rawinclude(rawValue, inclusion = False)
    except:
        print "No rows excluded or included explicitly."

    #index filters
    try:
        papers_ind = [int(re.findall(pattern, x)[0]) for x in dataproc.index]
        papers = xmldoc.getElementsByTagName('papers')[0]
        papers_incl = str(papers.attributes['type'].value)
        papers_values = [int(x) for x in papers.firstChild.nodeValue.split(',')] #from xml
        if papers_incl == 'include':
            foohook = True
        else:
            foohook = False
        for value in papers_values:
            query.rawinclude(
                [i+1 for i,x in enumerate(papers_ind) if value == x],
                inclusion = foohook
                )
    except:
        print "No papers explicitly included or excluded."
        

    #column filters
    filters = xmldoc.getElementsByTagName('filter')
    if filters:
        for filt in filters:
            incl = str(filt.attributes['type'].value)
            col = str(filt.attributes['col'].value)
            values = [str(x) for x in filt.firstChild.nodeValue.split(',')]
            if incl == "include":
                query.includeColFactors(col, values, True)
            else:
                query.includeColFactors(col, values, False)
    else:
        print "No filters specified in xml query."

    return(query.include)

if __name__ == "__main__":
    ########################
    #remove this later
    lastcol = 10
    firstcol = 1

    import pandas as pd
    from process import handle_range, handle_days
    from pairdiff import pairdiff
    data = pd.DataFrame.from_csv("../DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv")
    handle_range(data,1) #process range issue
    dataproc = handle_days(data,0) #processed data with dates

    m, n = dataproc.shape
    ########################

    
    #xml processing
    xmldoc = minidom.parse('query.xml') #only user input is here
    rawexclusion = xmldoc.getElementsByTagName('rowMod')
    rawType = str(rawexclusion[0].attributes['type'].value)
    rawValue = [int(x) for x in (rawexclusion[0].firstChild.nodeValue).split(',')]
    filters = xmldoc.getElementsByTagName('filter')

    #build query object
    query = filterobj(m,dataproc)
    if rawType == 'include':
        query.rawinclude(rawValue, inclusion = True)
    else:
        query.rawinclude(rawValue, inclusion = False)

    if filters:
        for filt in filters:
            incl = str(filt.attributes['type'].value)
            col = str(filt.attributes['col'].value)
            values = [str(x) for x in filt.firstChild.nodeValue.split(',')]
            if incl == "include":
                query.includeColFactors(col, values, True)
            else:
                query.excludeColFactors(col, values, False)
