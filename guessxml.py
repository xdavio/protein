import pandas as pd


filepath = '../DmelClockTimeSeriesSearch-2015-03-26--DataTable_V4.xlsx'
excel = 0

data = pd.read_excel(filepath, sheetname = excel, index_col = 0)

print "Setting handling of range to method: average."
numberrange = 0

print "Setting handling of range of days to method: average."
dayrange = 0

print "Setting first data column to 2"
firstcol = 2

try:
    print "Inferring last data column..."
    lastcol = [y for y,x in enumerate(data.columns.values) if 'Unnamed' in x][0]
    print "Setting last data column equal to " + lastcol
except:
    print "last column of time series data could not be inferred."
    lastcol = 'unknown'


rowMod type = "exclude">2</rowMod>
papers type = "exclude">17,27</papers>
colFilters>
filter type = "include" col = "measured_material">whole_head</filter>
colFilters>
