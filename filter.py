from xml.dom import minidom
from itertools import izip

#main code for subsetting the dataset
class filterobj():
    """This object converts the xml file in the createQuery into a boolean vector
    of row inclusion."""
    def __init__(self, m, data):
        self.m = m
        self.include = [True] * self.m
        self.data = data
        pass
            
    def includeColFactors(self, col, argl, inclusion = True):
        """
        Here, col is the string of the column name of interest,
        argl is a list of strings of factors of interest.
        inclusion determines of the factors of interest are included or excluded
        from final row inclusion.
        """
        self.tmp = [False] * self.m
        for value in argl:
            #self.l = list(self.data[col] == value)
            try:
                #print [x for x in self.data[col]]
                self.l = list([value in x for x in self.data[col]])
            except:
                #sometimes this string comparison is needed
                self.l = list([str(value) in str(x) for x in self.data[col]])
            self.tmp = [max(a,b) for a,b in izip(self.l,self.tmp)]
        if not inclusion:
            self.tmp = [not x for x in self.tmp]
        self.add_to_list(self.tmp)

    def rawinclude(self, l, inclusion = True):
        """This method deals with user-defined inclusion / exclusion of rows based on row number.
        Here, the user-supplied rows are NOT python-indexed, that is, they start with 1 and not 0."""
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
        ## for i in range(self.m):
        ##     if self.include[i] and add[i]:
        ##         self.include[i] = True
        ##     else:
        ##         self.include[i] = False

        #consider this alternative syntactic sugar
        self.include = [x and y for x,y in izip(self.include,add)]
        
def createQuery(xmlfile, m, dataproc):
    #xml processing
    xmldoc = minidom.parse(xmlfile) #only user input is here
    rawexclusion = xmldoc.getElementsByTagName('rowMod')
    rawType = str(rawexclusion[0].attributes['type'].value)
    try:
        rawValue = [int(x) for x in (rawexclusion[0].firstChild.nodeValue).split(',')]
    except:
        print "No rows excluded or included explicitly."
        rawValue = []
    filters = xmldoc.getElementsByTagName('filter')

    #build query object
    query = filterobj(m,dataproc)
    
    #make sure there are row exclusions
    if rawValue:        
        if rawType == 'include':
            query.rawinclude(rawValue, inclusion = True)
        else:
            query.rawinclude(rawValue, inclusion = False)

    #make sure there are filters
    for filt in filters:
        incl = str(filt.attributes['type'].value)
        col = str(filt.attributes['col'].value)
        values = [str(x) for x in filt.firstChild.nodeValue.split(',')]
        if incl == "include":
            query.includeColFactors(col, values, True)
        else:
            query.includeColFactors(col, values, False)

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
