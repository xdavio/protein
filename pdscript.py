import click
from main import allxml
import pandas as pd
import xlsxwriter
import numpy as np
from guessxml import query as xmlquery

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


#@click.argument('filepath', type = click.File('rb'))

@click.command()
@click.option('-e', '--excel', default = 0)
@click.option('-f', '--firstcol', default = 2)
@click.option('-l', '--lastcol', default = 'guess')
@click.option('-r', '--numberrange', default = 0)
@click.option('-d', '--dayrange', default = 0)
@click.argument('filepath')
def guessxml(filepath, excel, firstcol, lastcol, numberrange, dayrange):
    data = pd.read_excel(filepath, sheetname = excel, index_col = 0) #import the data

    q = xmlquery() #xml object
    q.sn('filepath', str(filepath))
    q.sn('numberrange', str(numberrange))
    q.sn('dayrange', str(dayrange))
    q.sn('firstcol', str(firstcol))
    q.sn('excel', str(excel))

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
    q.sn('lastcol', str(lastcol)) #set lastcol

    rowmod = click.confirm("Do you want to exclude/include any rows?")
    if rowmod:
        q.addchild('rowMod')
        rowinclude = click.prompt("Specify if you want to include or exclude rows? (1 = include, 2 = exclude)")
        if rowinclude == 1:
            click.echo("Row inclusion specified.")
            q.inclusion('rowMod', 'include')
        else:
            click.echo("Row exclusion specified.")
            q.inclusion('rowMod', 'exclude')            


        click.echo("Here are the rows:")
        click.echo([x+1 for x,y in enumerate(data.index)])
        rownumbers = click.prompt("Enter the numbers, separated by commas; then press enter. The rows you select will be included or excluded, depending on which operation you're performing:")
        q.sn('rowMod', rownumbers)

    papers = click.confirm("Do you want to exclude/include any papers?")
    if papers:
        q.addchild('papers')
        paperinclude = click.prompt("Specify if you want to include or exclude papers? (1 = include, 2 = exclude)")
        if paperinclude == 1:
            click.echo("Paper inclusion specified.")
            q.inclusion('papers', 'include')            
        else:
            click.echo("Paper exclusion specified.")            
            q.inclusion('papers', 'exclude')            

        click.echo("Here are the unique papers in the data frame:")
        click.echo(np.unique([int(x.split('.')[0]) for x in data.index]))
        papernumbers = click.prompt("Enter the numbers, separated by commas; then press enter. The papers you select will be included or excluded, depending on which operation you're performing:")
        q.sn('papers', papernumbers)

    click.echo("----")
    click.echo("Specify query.")
    click.echo("----")
    
    def specifyquery():
        click.echo("Here are the column names of interest:")
        click.echo([str(x) for x in data.columns.values[lastcol:] if 'Unnamed' not in x])
        
        col = click.prompt("Write the name of column on which to search")
        inclusion = click.prompt("Specify if you want to include or exclude on this column? (1 = include, 2 = exclude)")
        if inclusion == 1:
            q.addfilter('include', col)
        else:
            q.addfilter('exclude', col)

        click.echo("Here are the values of this column of the dataset:")
        click.echo("----------------------------------------------")
        click.echo(data[col])
        click.echo("----------------------------------------------")        
        q.addfilterfactors(
            click.prompt("Specify in a comma-separated list the factors to include or exclude.")
            )

    #if click.confirm("Do you wish to specify a query?"):
    #    specifyquery()

    while click.confirm("Do you wish to specify a query?"):
        specifyquery()
    


    q.dump()
    #[str(x) for x in data.columns.values[lastcol:] if 'Unnamed' not in x]
    #rowMod type = "exclude">2</rowMod>
    #papers type = "exclude">17,27</papers>
    #colFilters>
    #filter type = "include" col = "measured_material">whole_head</filter>
    #colFilters>

cli.add_command(guessxml)
