# protein

## Overview

This document outlines the usage of the pairwise difference measure of internal reliability of time series according to pre-specified excel spreadsheet guidelines.

## Required Python Packages

You need the following packages to run this script:
* Numpy
* Pandas
* xlrd

Use standard python package installation tools such as pip or easy_install in order to obtain these packages. Error will result otherwise, identifying the name of the missing package(s). Ask me for help installing python modules/packages if you want a tutorial.

## Directory Structure

The directory structure of the end-user should look like the following:

yourproject/
--/func.py   (tells python which data and query files to grab, and other parameters)
--/query.xml (specifies the SQL-like query on the data)
--/data.xlsx (the Excel file of time series information)
--/pairdiff/[contents of this repository go here]

When you download this code, I recommend copying the sample func.py and query.xml files provided into the structure seen above.

## Running the script

Here is an example func.py file:

```python
from pairdiff.main import getPairDiff, pairdiff, getPairDiffdebug

diff = getPairDiff(
    filepath = 'data.xlsx',
    querypath = 'query.xml',
    numberrange = 0,
    dayrange = 0,
    firstcol = 1,
    lastcol = 11,
    excel = 0
    )
```

The following describes the meaning of the parameters:
* filepath: Specifies the relative path of the spreadsheet of interest.
* querypath: Specifies the relative path of the query of interest on the spreadsheet.
* numberrange: Specifies how to handle cells of the form "NUM to NUM":
  * 0 means average the range of numbers,
  * 1 means take the first number,
  * 2 means take the second number,
  * 3 means take the smaller number
  * 4 means take the larger number
* dayrange: Specifies how to handle multiple days. If -1, leave all days in the dataset as separate data points. If 0, average over the days and proceed. Other options are available in the process.py file for the interested reader.
* firstcol: Specifies the column number before the first column of data. In most spreadsheets, the first column is "day" which isn't actually "time to peak" (or similar) data. Usually, this value is 1.
* lastcol: Specifies the column number before the last column of data (e.g. the column number of the last column of data minus 1). If your output doesn't contain all of the data columns of interest, try increasing this number by 1. If the script fails, try decreasing this number by 1. 
* excel: This selects the spreadsheet in the xlsx file described by "filepath." It is "0-indexed" which means 0 is the first spreadsheet, 1 is the second spreadsheet, and so on. 


To run the script, open terminal. Then use the 
```shell
cd path/to/yourproject
```


Alternatively, you can run the script with
