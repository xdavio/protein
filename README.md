# protein

## Overview

This document outlines the usage of the pairwise difference measure of internal reliability of time series according to pre-specified excel spreadsheet guidelines.

## Required Python Packages

You need the following packages to run this script:
* Numpy
* Pandas
* xlrd

Use standard python package installation tools such as pip or easy_install in order to obtain these packages. Error will result otherwise, identifying the name of the missing package(s).

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
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
    querypath = 'query.xml',
    numberrange = 0,
    dayrange = 0,
    firstcol = 1,
    lastcol = 11,
    excel = 0
    )
```
