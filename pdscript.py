import click
from main import allxml

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

    
    
