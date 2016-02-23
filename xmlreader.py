from xml.dom import minidom as md


#filename = 'querynew.xml'
def xmlwrapper(filename):
    data = md.parse(filename)
    try:
        filepath = str(data.getElementsByTagName('filepath')[0].firstChild.nodeValue)
        numberrange = int(data.getElementsByTagName('numberrange')[0].firstChild.nodeValue)
        dayrange = int(data.getElementsByTagName('dayrange')[0].firstChild.nodeValue)
        firstcol = int(data.getElementsByTagName('firstcol')[0].firstChild.nodeValue)
        lastcol = int(data.getElementsByTagName('lastcol')[0].firstChild.nodeValue)
    except:
        print "A required input (filepath, numberrange, dayrange, firstcol, or lastcol) could not be read from the xml file."
    try:
        excel = int(data.getElementsByTagName('excel')[0].firstChild.nodeValue)
    except:
        excel = None
    return filepath, numberrange, dayrange, firstcol, lastcol, excel
