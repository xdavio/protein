from lxml import etree

class query(object):
    def __init__(self):
        self.buildbase()

    def buildbase(self):
        self.query = etree.Element("query")
        self.query.append( etree.Element("filepath") )
        self.query.append( etree.Element("numberrange") )
        self.query.append( etree.Element("dayrange") )
        self.query.append( etree.Element("firstcol") )
        self.query.append( etree.Element("lastcol") )
        self.query.append( etree.Element("excel") )
        self.query.append( etree.Element("colFilters") )
        self.colFilters = self.query.find("colFilters")
        self.filters = -1 #current index of filters
        

    def sn(self, nodename, value):
        """
        (S)ets (N)ode 'nodename' to value 'value'
        """
        #etree.SubElement(self.query, nodename).text = value
        self.query.find(nodename).text = value

    def addchild(self, childname):
        self.query.append( etree.Element( childname ) )

    def inclusion(self, nodename, val):
        """
        val is either 'include' or 'exclude'
        """
        if 'include' not in val and 'exclude' not in val:
            print 'Val must take either the value include or exclude.'
        self.query.find(nodename).attrib['type'] = val

    def addfilter(self, inclusion = 'include', col = 'unknown'):
        self.filters = self.filters + 1
        self.colFilters.append( etree.Element('filter', type = inclusion, col = col) )

    def addfilterfactors(self, factors):
        self.colFilters[self.filters].text = factors

    
    def dump(self):
        print etree.tostring(self.query, pretty_print = True)
        
