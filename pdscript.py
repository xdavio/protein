import click
from main import allxml
import pandas as pd
import xlsxwriter
import numpy as np
from lxml import etree

class query(object):
    def __init__(self):
        self.inclusion = []
        self.name = []
        self.factors = []
        self.query = etree.Element("query")
        self.buildbase()

    def addinclusion(self, s):
        self.inclusion.append(s)
        
    def addname(self, s):
        self.name.append(s)
        
    def addfactors(self, s):
        self.factors.append(s)
        
    def addblock(self, sinclude, sname, sfactor):
        self.addinclusion(sinclude)
        self.addname(sname)
        self.addfactors(sfactor)

    def buildbase(self):
        self.query.append( etree.Element("filepath") )
        self.query.append( etree.Element("numberrange") )
        self.query.append( etree.Element("dayrange") )
        self.query.append( etree.Element("firstcol") )
        self.query.append( etree.Element("lastcol") )
        self.query.append( etree.Element("excel") )
        self.query.append( etree.Element("colFilters") )
        

@click.group()
def cli():
    pass

@click.command()
@click.option('--hush', default = False, is_flag = True)
@click.argument('filename')
def diffmeas(filename, hush):
    """
    Command-line tool for executing pairdiff script. The argument [filename] is the xml file which determines the parameters for the script.
    """
    click.echo('Reading ' + str(filename) + '...')
    try:
        diff = allxml(filename)
    except:
        click.echo('Script execution failed.')

    click.echo('Directory ' + diff.dirname + ' was created with output.')
    if not hush:
        click.echo('The diffmeas follows:')
        click.echo(diff.pairdiff)
    
cli.add_command(diffmeas)


@click.command()
@click.option('--hush', default = False, is_flag = True)
@click.argument('filename')
def explodesheets(filename):
    """
    Explodes an excel spreadsheets' many sheets into new excel spreadsheets, each in its own xlsx file. This will use the original spreadsheet name and append the sheet number to the end. 
    """
    data = pd.read_excel(filename, sheetname = None)
    foo = filename.split('.')
    base = foo[0]
    ext = foo[1]
    
    for key, val in data.iteritems():
        name = base + '_' + str(key) + '.' + ext
        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        val.to_excel(writer)
        writer.save()

cli.add_command(explodesheets)



@click.command()
@click.option('-e', '--excel', default = 0)
@click.option('-f', '--firstcol', default = 2)
@click.option('-l', '--lastcol', default = 'guess')
@click.option('-r', '--numberrange', default = 0)
@click.option('-d', '--dayrange', default = 0)
@click.argument('filepath', type = click.File('rb'))
def guessxml(filepath, excel, firstcol, lastcol, numberrange, dayrange):

    #filepath = '../DmelClockTimeSeriesSearch-2015-03-26--DataTable_V4.xlsx'
    #excel = 0
    
    data = pd.read_excel(filepath, sheetname = excel, index_col = 0)

    #guess the last column of data
    if lastcol == 'guess':
        try:
            click.echo("Inferring last data column...")
            lastcol = [y for y,x in enumerate(data.columns.values) if 'Unnamed' in x][0] #inspect data.columns.values -- it turns out that the first 'Unnamed' column name is a good guess for the proper value of lastcol
            click.echo("Setting last data column equal to " + str(lastcol))
        except:
            click.echo("last column of time series data could not be inferred.")
            lastcol = 'unknown'
    else:
        try:
            lastcol = int(lastcol)
        except:
            click.echo("lastcol is not an integer. Setting to unknown.")
            lastcol = 'unknown'

    rowmod = click.confirm("Do you want to exclude/include any rows?")
    if rowmod:
        rowinclude = click.prompt("Specify if you want to include or exclude rows? (1 = include, 2 = exclude)")
        if rowinclude == 1:
            click.echo("Row inclusion specified.")
            rowinclude = 'include'
        else:
            click.echo("Row exclusion specified.")            
            rowinclude = 'exclude'

        click.echo("Here are the rows:")
        click.echo([x+1 for x,y in enumerate(data.index)])
        rownumbers = click.prompt("Enter the numbers, separated by commas; then press enter. The rows you select will be included or excluded, depending on which operation you're performing:")

    papers = click.confirm("Do you want to exclude/include any papers?")
    if papers:
        paperinclude = click.prompt("Specify if you want to include or exclude papers? (1 = include, 2 = exclude)")
        if paperinclude == 1:
            click.echo("Paper inclusion specified.")
            paperinclude = 'include'
        else:
            click.echo("Paper exclusion specified.")            
            paperinclude = 'exclude'

        click.echo("Here are the unique papers in the data frame:")
        click.echo(np.unique([int(x.split('.')[0]) for x in data.index]))
        papernumbers = click.prompt("Enter the numbers, separated by commas; then press enter. The papers you select will be included or excluded, depending on which operation you're performing:")

    click.echo("----")
    click.echo("Specify query.")
    click.echo("----")
    
    if click.confirm("Do you wish to specify a query row?"):
        click.echo("Here are the rows of interest:")
        click.echo([str(x) for x in data.columns.values[lastcol:] if 'Unnamed' not in x])
        query['name'].append(click.prompt("Write the name of the row of interest"))
        tmp = click.prompt("Specify if you want to include or exclude papers? (1 = include, 2 = exclude)")
        if tmp == 1:
            query['inclusion'].append('include')
        else:
            query['inclusion'].append('exclude')
        
    #[str(x) for x in data.columns.values[lastcol:] if 'Unnamed' not in x]
    #rowMod type = "exclude">2</rowMod>
    #papers type = "exclude">17,27</papers>
    #colFilters>
    #filter type = "include" col = "measured_material">whole_head</filter>
    #colFilters>

cli.add_command(guessxml)
