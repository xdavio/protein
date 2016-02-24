import click
from main import allxml
import pandas as pd
import xlsxwriter

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
