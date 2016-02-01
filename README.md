# protein

## Overview

This document outlines the usage of the pairwise difference measure of internal reliability of time series according to pre-specified excel spreadsheet guidelines.

## Required Python Packages

You need the following packages to run this script:
* Numpy
* Pandas
* xlsxwriter
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

### func.py

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

### query.xml

Here is an example of a query.xml file:
```xml
<?xml version="1.0"?>
<query>
  <!-- Takes type = "include" for row inclusion, "exclude" for row exclusion -->
  <rowMod type = "exclude">1,2</rowMod>
  <papers type = "include">15,71</papers>
  <colFilters>
    <filter type = "include" col = "measured_material">whole_head</filter>
  </colFilters>
</query>
```

Each such query.xml file can only have one query in it. If you wish to enumerate with commas rows of the spreadsheet to exclude, modify the "rowMod" line. If you wish to specify the rows to include instead of the ones to remove, change "exclude" to "include." The same logic applies to each subsequent place in the file where you see "include" and "exclude."

Each row of the form
```xml
    <filter type = "include" col = "measured_material">whole_head</filter>
```
can be used specify your query. The variable "col" (which here has the value "measured\_material") selects the column you wish to restrict the pairwise difference algorithm on. It must match exactly the column name in the xlsx file. Where "whole\_head" is written, write whichever factors you're interested in selecting. If there is more than one, separate them with commas. So you may instead write "whole\_head,northern\_blot" which would include all rows with either of these tags under the "measured\_material" column and throw out the rest. If you wanted to keep the rest, change "incldue" to "exclude". If you want to extend your query to other columns in the spreadsheet, simply duplicate the filter row:
```xml
  <colFilters>
    <filter type = "include" col = "measured_material">whole_head</filter>
    <filter type = "exclude" col = "another_column">something,something_else</filter>
  </colFilters>
```
You can perform this row duplication an arbitrary number of times. Make sure you save the query.xml file when you're done modifying it.

### Actually running the script

To run the script, open terminal. Then write in the terminal window
```shell
cd path/to/yourproject
python
```

The terminal window will turn into a python interpreter. You can then copy-paste the contents of func.py into the interpreter and press enter. The pairwise differences should appear on the screen after writing "diff" and pressing enter. This is the same diff as the 3rd line of func.py above. If it were instead 
```python
diff3 = getPairDiff(...)
```
then writing "diff3" and pressing enter would display the pairwise differences.


### Debugging

You may wish to see how the filters you're specifying are affecting the spreadsheet. To do this, use "getPairDiffdebug" instead of "getPairDiff" in line 3 of func.py. This will create a directory with the same name as the xlsx file in the filepath variable. Inside the directory will a single xlsx file called "debug.xlsx" with several sheets. The sheets are named and described here:

* data: This is just the imported spreadsheet.
* datarange: This is after cells with 'NUM to NUM' are fixed.
* datadays: This is after multiple days are handled.
* dataquery: This is after the query.xml file is applied.
* pairdiff: This is the pairwise difference measure.
