from pairdiff.main import getPairDiff, pairdiff, getPairDiffdebug

diff = getPairDiff(
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
    querypath = 'query.xml',
    numberrange = 0,
    dayrange = 0,
    firstcol = 1,
    lastcol = 11
    )

diff2 = getPairDiffdebug(
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable3.csv',
    querypath = 'query.xml',
    numberrange = 0,
    dayrange = 0,
    firstcol = 1,
    lastcol = 11
    )


diffnew = getPairDiffdebug(
    filepath = 'DmelClockTimeSeriesSearch-2015-03-26--DataTable_V11_RNA_per.xlsx'
    querypath = 'query.xml',
    numberrange = 0,
    dayrange = 0,
    firstcol = 1,
    lastcol = 11
    )

